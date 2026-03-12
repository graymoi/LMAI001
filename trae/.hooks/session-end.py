#!/usr/bin/env python3
"""
Session End Hook
会话结束时自动保存上下文和状态
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

class SessionEndHandler:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.session_dir = self.project_root / ".sessions"
        self.context_dir = self.session_dir / "context"
        self.state_dir = self.session_dir / "state"
        self.cache_dir = self.session_dir / "cache"
        
        # 加载配置
        self.config = self.load_config()
        
        # 当前会话信息
        self.session_id = self.get_current_session_id()
        self.session_end_time = datetime.now()
        
        # 会话统计
        self.session_stats = {
            "commands_executed": 0,
            "files_modified": 0,
            "documents_created": 0,
            "errors_encountered": 0
        }
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        config_file = self.project_root / "trae" / ".hooks" / "config.json"
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "session": {
                    "enabled": True,
                    "auto_save": True,
                    "save_interval": 300
                }
            }
    
    def get_current_session_id(self) -> str:
        """获取当前会话ID"""
        last_session_file = self.state_dir / "last_session.json"
        try:
            with open(last_session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("last_session_id", "unknown")
        except FileNotFoundError:
            return "unknown"
    
    def load_session_record(self) -> Dict[str, Any]:
        """加载会话记录"""
        session_file = self.session_dir / f"session_{self.session_id}.json"
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_context(self, context_type: str, context_data: Dict[str, Any]):
        """保存特定类型的上下文"""
        context_file = self.context_dir / f"{context_type}.json"
        with open(context_file, 'w', encoding='utf-8') as f:
            json.dump(context_data, f, indent=2, ensure_ascii=False)
    
    def save_project_context(self, context: Dict[str, Any]):
        """保存项目上下文"""
        self.save_context("project_context", context)
    
    def save_document_context(self, context: Dict[str, Any]):
        """保存文档上下文"""
        self.save_context("document_context", context)
    
    def save_user_preferences(self, preferences: Dict[str, Any]):
        """保存用户偏好"""
        self.save_context("user_preferences", preferences)
    
    def save_workflow_state(self, state: Dict[str, Any]):
        """保存工作流状态"""
        self.save_context("workflow_state", state)
    
    def save_cache(self, cache_key: str, cache_data: Any, ttl: int = 3600):
        """保存缓存"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        cache_entry = {
            "timestamp": datetime.now().isoformat(),
            "ttl": ttl,  # 生存时间（秒）
            "data": cache_data
        }
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_entry, f, indent=2, ensure_ascii=False)
    
    def update_session_record(self, session_record: Dict[str, Any]):
        """更新会话记录"""
        session_file = self.session_dir / f"session_{self.session_id}.json"
        
        # 更新结束时间和统计
        session_record["end_time"] = self.session_end_time.isoformat()
        session_record["duration_seconds"] = (
            self.session_end_time - datetime.fromisoformat(session_record["start_time"])
        ).total_seconds()
        session_record["stats"] = self.session_stats
        
        # 保存更新后的记录
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_record, f, indent=2, ensure_ascii=False)
    
    def clean_old_sessions(self, max_sessions: int = 10):
        """清理旧的会话记录"""
        session_files = sorted(
            self.session_dir.glob("session_*.json"),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )
        
        # 保留最新的max_sessions个会话
        if len(session_files) > max_sessions:
            for old_file in session_files[max_sessions:]:
                old_file.unlink()
                print(f"  🗑️  删除旧会话: {old_file.name}")
    
    def clean_expired_cache(self):
        """清理过期的缓存"""
        cache_files = self.cache_dir.glob("*.json")
        current_time = datetime.now()
        
        for cache_file in cache_files:
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                cache_time = datetime.fromisoformat(cache_data.get("timestamp", ""))
                cache_age = (current_time - cache_time).total_seconds()
                ttl = cache_data.get("ttl", 3600)
                
                if cache_age > ttl:
                    cache_file.unlink()
                    print(f"  🗑️  删除过期缓存: {cache_file.name}")
            except (json.JSONDecodeError, ValueError, KeyError):
                # 删除损坏的缓存文件
                cache_file.unlink()
                print(f"  🗑️  删除损坏缓存: {cache_file.name}")
    
    def generate_session_summary(self) -> Dict[str, Any]:
        """生成会话摘要"""
        session_record = self.load_session_record()
        
        if not session_record:
            return {
                "session_id": self.session_id,
                "status": "incomplete",
                "message": "会话记录未找到"
            }
        
        duration = session_record.get("duration_seconds", 0)
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        
        return {
            "session_id": session_record.get("session_id"),
            "start_time": session_record.get("start_time"),
            "end_time": session_record.get("end_time"),
            "duration": f"{hours:02d}:{minutes:02d}:{seconds:02d}",
            "stats": session_record.get("stats", {}),
            "contexts_saved": len(session_record.get("loaded_contexts", {})),
            "status": "completed"
        }
    
    def print_session_summary(self, summary: Dict[str, Any]):
        """打印会话摘要"""
        print("=" * 60)
        print("📋 会话结束")
        print("=" * 60)
        print(f"会话ID: {summary['session_id']}")
        print(f"状态: {summary['status']}")
        print(f"持续时间: {summary['duration']}")
        print()
        
        if summary['status'] == "completed":
            print("📊 会话统计:")
            print("-" * 60)
            stats = summary.get("stats", {})
            print(f"  执行命令: {stats.get('commands_executed', 0)}")
            print(f"  修改文件: {stats.get('files_modified', 0)}")
            print(f"  创建文档: {stats.get('documents_created', 0)}")
            print(f"  遇到错误: {stats.get('errors_encountered', 0)}")
            print()
            print(f"💾 保存的上下文: {summary['contexts_saved']}个")
            print()
        
        print("🧹 清理操作:")
        print("-" * 60)
        print("  ✓ 清理旧会话记录")
        print("  ✓ 清理过期缓存")
        print()
        print("=" * 60)
        print("✅ 会话状态已保存")
        print("=" * 60)
    
    def run(self):
        """运行会话结束钩子"""
        if not self.config.get("session", {}).get("enabled", True):
            print("⚠️  Session钩子已禁用")
            return False
        
        # 加载会话记录
        session_record = self.load_session_record()
        
        if not session_record:
            print("⚠️  未找到会话记录，跳过保存")
            return False
        
        # 保存所有上下文（这里可以添加实际的上下文数据）
        # self.save_project_context({...})
        # self.save_document_context({...})
        # self.save_user_preferences({...})
        # self.save_workflow_state({...})
        
        # 更新会话记录
        self.update_session_record(session_record)
        
        # 清理旧数据
        max_sessions = self.config.get("session", {}).get("max_sessions", 10)
        self.clean_old_sessions(max_sessions)
        self.clean_expired_cache()
        
        # 生成摘要
        summary = self.generate_session_summary()
        
        # 打印摘要
        self.print_session_summary(summary)
        
        return True

def main():
    handler = SessionEndHandler()
    success = handler.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
