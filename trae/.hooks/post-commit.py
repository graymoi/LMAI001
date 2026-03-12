#!/usr/bin/env python3
"""
Post-commit Hook
提交后执行脚本
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

class PostCommitHandler:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.config_file = self.project_root / ".hooks" / "config.json"
        self.config = self.load_config()
        self.commit_hash = self.get_commit_hash()
        self.commit_message = self.get_commit_message()

    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "actions": {
                    "log_commit": True,
                    "update_stats": True,
                    "notify_team": False,
                    "trigger_automation": True
                },
                "log_file": ".hooks/commit_log.json"
            }

    def get_commit_hash(self):
        """获取提交哈希"""
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()

    def get_commit_message(self):
        """获取提交信息"""
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=%B'],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()

    def get_changed_files(self):
        """获取变更的文件"""
        result = subprocess.run(
            ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'],
            capture_output=True,
            text=True
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []

    def log_commit(self):
        """记录提交日志"""
        if not self.config['actions']['log_commit']:
            return
        
        log_file = self.project_root / self.config['log_file']
        log_data = {
            "commit_hash": self.commit_hash,
            "commit_message": self.commit_message,
            "timestamp": datetime.now().isoformat(),
            "changed_files": self.get_changed_files()
        }
        
        # 读取现有日志
        logs = []
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        
        # 添加新日志
        logs.append(log_data)
        
        # 保存日志
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 已记录提交日志: {self.commit_hash[:8]}")

    def update_stats(self):
        """更新统计信息"""
        if not self.config['actions']['update_stats']:
            return
        
        stats_file = self.project_root / ".hooks" / "stats.json"
        
        # 读取现有统计
        stats = {}
        if stats_file.exists():
            with open(stats_file, 'r', encoding='utf-8') as f:
                stats = json.load(f)
        
        # 更新统计
        stats["total_commits"] = stats.get("total_commits", 0) + 1
        stats["last_commit"] = {
            "hash": self.commit_hash,
            "message": self.commit_message,
            "timestamp": datetime.now().isoformat()
        }
        
        # 按文件类型统计
        changed_files = self.get_changed_files()
        for file_path in changed_files:
            file_ext = Path(file_path).suffix.lower()
            stats["file_types"] = stats.get("file_types", {})
            stats["file_types"][file_ext] = stats["file_types"].get(file_ext, 0) + 1
        
        # 保存统计
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 已更新统计信息: 总提交 {stats['total_commits']} 次")

    def notify_team(self):
        """通知团队"""
        if not self.config['actions']['notify_team']:
            return
        
        # 这里可以集成邮件、Slack、钉钉等通知方式
        print(f"📧 提交通知: {self.commit_message[:50]}...")

    def trigger_automation(self):
        """触发自动化任务"""
        if not self.config['actions']['trigger_automation']:
            return
        
        changed_files = self.get_changed_files()
        
        # 检查是否有文档变更
        doc_changed = any(f.endswith('.md') for f in changed_files)
        if doc_changed:
            print("📄 检测到文档变更，触发文档自动化...")
            # 这里可以调用文档自动化技能
        
        # 检查是否有代码变更
        code_changed = any(f.endswith('.py') for f in changed_files)
        if code_changed:
            print("💻 检测到代码变更，触发代码自动化...")
            # 这里可以调用代码自动化技能
        
        # 检查是否有配置变更
        config_changed = any(f.endswith('.json') for f in changed_files)
        if config_changed:
            print("⚙️  检测到配置变更，触发配置自动化...")
            # 这里可以调用配置自动化技能

    def run_actions(self):
        """运行所有操作"""
        print(f"\n📝 提交信息: {self.commit_message[:100]}...")
        print(f"🔗 提交哈希: {self.commit_hash}")
        
        # 记录提交日志
        self.log_commit()
        
        # 更新统计信息
        self.update_stats()
        
        # 通知团队
        self.notify_team()
        
        # 触发自动化
        self.trigger_automation()
        
        print("\n✅ Post-commit 操作完成")

def main():
    handler = PostCommitHandler()
    handler.run_actions()

if __name__ == "__main__":
    main()
