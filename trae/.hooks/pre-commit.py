#!/usr/bin/env python3
"""
Pre-commit Hook
提交前检查脚本
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class PreCommitChecker:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.config_file = self.project_root / ".hooks" / "config.json"
        self.config = self.load_config()
        self.errors = []
        self.warnings = []

    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "checks": {
                    "file_format": True,
                    "file_size": True,
                    "file_encoding": True,
                    "document_quality": True,
                    "code_quality": True
                },
                "limits": {
                    "max_file_size": 10485760,  # 10MB
                    "max_line_length": 120,
                    "allowed_encodings": ["utf-8"]
                }
            }

    def get_staged_files(self):
        """获取暂存的文件"""
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True,
            text=True
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []

    def check_file_format(self, file_path):
        """检查文件格式"""
        file_ext = file_path.suffix.lower()
        
        # 检查Markdown文件
        if file_ext == '.md':
            self.check_markdown_file(file_path)
        
        # 检查Python文件
        elif file_ext == '.py':
            self.check_python_file(file_path)
        
        # 检查JSON文件
        elif file_ext == '.json':
            self.check_json_file(file_path)

    def check_markdown_file(self, file_path):
        """检查Markdown文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查文件是否为空
            if not content.strip():
                self.errors.append(f"文件 {file_path} 为空")
                return
            
            # 检查标题格式
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if line.startswith('#'):
                    # 检查标题后是否有空格
                    if len(line) > 1 and line[1] != ' ':
                        self.warnings.append(f"{file_path}:{i} 标题格式不规范，标题后应有空格")
                    
                    # 检查标题是否为空
                    if line.strip('#').strip() == '':
                        self.errors.append(f"{file_path}:{i} 标题为空")
        
        except Exception as e:
            self.errors.append(f"检查文件 {file_path} 失败: {str(e)}")

    def check_python_file(self, file_path):
        """检查Python文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 检查行长度
            for i, line in enumerate(lines, 1):
                if len(line.rstrip()) > self.config['limits']['max_line_length']:
                    self.warnings.append(f"{file_path}:{i} 行长度超过限制 ({len(line.rstrip())} > {self.config['limits']['max_line_length']})")
            
            # 检查是否有TODO注释
            for i, line in enumerate(lines, 1):
                if 'TODO' in line or 'FIXME' in line:
                    self.warnings.append(f"{file_path}:{i} 包含TODO/FIXME注释")
        
        except Exception as e:
            self.errors.append(f"检查文件 {file_path} 失败: {str(e)}")

    def check_json_file(self, file_path):
        """检查JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"文件 {file_path} JSON格式错误: {str(e)}")
        except Exception as e:
            self.errors.append(f"检查文件 {file_path} 失败: {str(e)}")

    def check_file_size(self, file_path):
        """检查文件大小"""
        try:
            file_size = file_path.stat().st_size
            max_size = self.config['limits']['max_file_size']
            
            if file_size > max_size:
                self.warnings.append(f"文件 {file_path} 大小超过限制 ({file_size} > {max_size} bytes)")
        except Exception as e:
            self.errors.append(f"检查文件 {file_path} 大小失败: {str(e)}")

    def check_file_encoding(self, file_path):
        """检查文件编码"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # 尝试UTF-8解码
            try:
                content.decode('utf-8')
            except UnicodeDecodeError:
                self.errors.append(f"文件 {file_path} 不是UTF-8编码")
        
        except Exception as e:
            self.errors.append(f"检查文件 {file_path} 编码失败: {str(e)}")

    def check_document_quality(self, file_path):
        """检查文档质量"""
        if file_path.suffix.lower() != '.md':
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查文档结构
            if not content.startswith('#'):
                self.warnings.append(f"文件 {file_path} 缺少标题")
            
            # 检查文档长度
            if len(content) < 100:
                self.warnings.append(f"文件 {file_path} 内容过短")
        
        except Exception as e:
            self.errors.append(f"检查文件 {file_path} 质量失败: {str(e)}")

    def check_code_quality(self, file_path):
        """检查代码质量"""
        if file_path.suffix.lower() != '.py':
            return
        
        try:
            # 运行flake8检查
            result = subprocess.run(
                ['flake8', str(file_path)],
                capture_output=True,
                text=True
            )
            
            if result.stdout:
                self.warnings.append(f"文件 {file_path} flake8检查:\n{result.stdout}")
        
        except FileNotFoundError:
            # flake8未安装，跳过检查
            pass
        except Exception as e:
            self.warnings.append(f"检查文件 {file_path} 代码质量失败: {str(e)}")

    def run_checks(self):
        """运行所有检查"""
        staged_files = self.get_staged_files()
        
        if not staged_files:
            print("没有暂存的文件")
            return True
        
        print(f"检查 {len(staged_files)} 个暂存文件...")
        
        for file_str in staged_files:
            file_path = self.project_root / file_str
            
            if not file_path.exists():
                continue
            
            # 文件格式检查
            if self.config['checks']['file_format']:
                self.check_file_format(file_path)
            
            # 文件大小检查
            if self.config['checks']['file_size']:
                self.check_file_size(file_path)
            
            # 文件编码检查
            if self.config['checks']['file_encoding']:
                self.check_file_encoding(file_path)
            
            # 文档质量检查
            if self.config['checks']['document_quality']:
                self.check_document_quality(file_path)
            
            # 代码质量检查
            if self.config['checks']['code_quality']:
                self.check_code_quality(file_path)
        
        # 输出结果
        if self.errors:
            print("\n❌ 发现错误:")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print("\n⚠️  发现警告:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ 所有检查通过")
        
        return len(self.errors) == 0

def main():
    checker = PreCommitChecker()
    success = checker.run_checks()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
