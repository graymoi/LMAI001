#!/usr/bin/env python3
"""
Session Start Hook
会话开始时自动加载上下文和状态
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

class SessionStartHandler:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.session_dir = self.project_root / ".sessions"
        self.context_dir = self.session_dir / "context"
        self.state_dir = self.session_dir / "state"
        self.cache_dir = self.session_dir / "cache"
        
        # 确保目录存在
        self.ensure_directories()
        
        # 加载配置
        self.config = self.load_config()
        
        # 当前会话信息
        self.session_id = self.generate_session_id()
        self.session_start_time = datetime.now()
        
    def ensure_directories(self):
        """确保所需目录存在"""
        self.session_dir.mkdir(exist_ok=True)
        self.context_dir.mkdir(exist_ok=True)
        self.state_dir.mkdir(exist_ok=True)
        self.cache_dir.mkdir(exist_ok=True)
        
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
                    "save_interval": 300,  # 5分钟
                    "max_sessions": 10
                },
                "context": {
                    "enabled": True,
                    "max_context_size": 100000,  # 100KB
                    "context_types": [
                        "project_context",
                        "document_context",
                        "user_preferences",
                        "workflow_state"
                    ]
                }
            }
    
    def generate_session_id(self) -> str:
        """生成会话ID"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def load_last_session(self) -> Optional[Dict[str, Any]]:
        """加载上一次会话的状态"""
        last_session_file = self.state_dir / "last_session.json"
        try:
            with open(last_session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def load_context(self, context_type: str) -> Optional[Dict[str, Any]]:
        """加载特定类型的上下文"""
        context_file = self.context_dir / f"{context_type}.json"
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def load_project_context(self) -> Dict[str, Any]:
        """加载项目上下文"""
        context = self.load_context("project_context")
        if context is None:
            context = {
                "project_name": "项目管理",
                "project_type": "标书编写",
                "current_phase": "需求分析",
                "current_document": None,
                "recent_files": [],
                "preferences": {
                    "tone": "professional",
                    "language": "zh-CN",
                    "format": "markdown"
                }
            }
        return context
    
    def load_document_context(self) -> Dict[str, Any]:
        """加载文档上下文"""
        context = self.load_context("document_context")
        if context is None:
            context = {
                "current_document": None,
                "document_history": [],
                "document_templates": [],
                "recent_sections": []
            }
        return context
    
    def load_user_preferences(self) -> Dict[str, Any]:
        """加载用户偏好"""
        context = self.load_context("user_preferences")
        if context is None:
            context = {
                "preferred_tone": "professional",
                "preferred_language": "zh-CN",
                "auto_save": True,
                "quality_check": True,
                "compliance_check": True
            }
        return context
    
    def load_workflow_state(self) -> Dict[str, Any]:
        """加载工作流状态"""
        context = self.load_context("workflow_state")
        if context is None:
            context = {
                "current_task": None,
                "task_queue": [],
                "completed_tasks": [],
                "blocked_tasks": []
            }
        return context
    
    def load_cache(self, cache_key: str) -> Optional[Any]:
        """加载缓存"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                # 检查缓存是否过期
                cache_time = datetime.fromisoformat(cache_data.get("timestamp", ""))
                cache_age = (datetime.now() - cache_time).total_seconds()
                max_age = self.config.get("cache", {}).get("max_age", 3600)  # 1小时
                
                if cache_age > max_age:
                    return None
                    
                return cache_data.get("data")
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return None
    
    def create_session_record(self) -> Dict[str, Any]:
        """创建会话记录"""
        return {
            "session_id": self.session_id,
            "start_time": self.session_start_time.isoformat(),
            "project_root": str(self.project_root),
            "config": self.config,
            "loaded_contexts": {
                "project_context": self.load_project_context(),
                "document_context": self.load_document_context(),
                "user_preferences": self.load_user_preferences(),
                "workflow_state": self.load_workflow_state()
            },
            "cache_stats": self.get_cache_stats()
        }
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        cache_files = list(self.cache_dir.glob("*.json"))
        return {
            "total_cache_files": len(cache_files),
            "cache_size_mb": sum(f.stat().st_size for f in cache_files) / (1024 * 1024),
            "oldest_cache": min([f.stat().st_mtime for f in cache_files]) if cache_files else None,
            "newest_cache": max([f.stat().st_mtime for f in cache_files]) if cache_files else None
        }
    
    def save_session_record(self):
        """保存会话记录"""
        session_file = self.session_dir / f"session_{self.session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(self.create_session_record(), f, indent=2, ensure_ascii=False)
        
        # 更新最后会话记录
        last_session_file = self.state_dir / "last_session.json"
        with open(last_session_file, 'w', encoding='utf-8') as f:
            json.dump({
                "last_session_id": self.session_id,
                "last_session_time": self.session_start_time.isoformat()
            }, f, indent=2, ensure_ascii=False)
    
    def print_session_summary(self):
        """打印会话摘要"""
        record = self.create_session_record()
        
        print("=" * 60)
        print("📋 会话开始")
        print("=" * 60)
        print(f"会话ID: {record['session_id']}")
        print(f"开始时间: {record['start_time']}")
        print(f"项目根目录: {record['project_root']}")
        print()
        print("📂 已加载的上下文:")
        print("-" * 60)
        
        for context_name, context_data in record['loaded_contexts'].items():
            print(f"  ✓ {context_name}")
            if isinstance(context_data, dict):
                for key, value in context_data.items():
                    if not isinstance(value, (dict, list)):
                        print(f"    - {key}: {value}")
        
        print()
        print("💾 缓存统计:")
        print("-" * 60)
        cache_stats = record['cache_stats']
        print(f"  总缓存文件: {cache_stats['total_cache_files']}")
        print(f"  缓存大小: {cache_stats['cache_size_mb']:.2f} MB")
        print()
        print("=" * 60)
        print("✅ 会话上下文加载完成")
        print("=" * 60)
    
    def run(self):
        """运行会话开始钩子"""
        if not self.config.get("session", {}).get("enabled", True):
            print("⚠️  Session钩子已禁用")
            return
        
        # 加载所有上下文
        self.load_project_context()
        self.load_document_context()
        self.load_user_preferences()
        self.load_workflow_state()
        
        # 保存会话记录
        self.save_session_record()
        
        # 打印会话摘要
        self.print_session_summary()
        
        return True

def main():
    handler = SessionStartHandler()
    success = handler.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
