#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
迁移功能测试脚本
测试所有从everything-claude-code、claudeception、deer-flow迁移的功能
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class MigrationTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.trae_dir = self.project_root / "trae"
        self.skills_dir = self.trae_dir / ".skills"
        self.hooks_dir = self.trae_dir / ".hooks"
        self.sessions_dir = self.trae_dir / ".sessions"
        self.memory_dir = self.trae_dir / ".memory"
        
        self.test_results = []
        self.start_time = datetime.now()
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 80)
        print("迁移功能测试")
        print("=" * 80)
        print(f"开始时间: {self.start_time}")
        print(f"项目根目录: {self.project_root}")
        print()
        
        # 测试技能
        self.test_skills()
        
        # 测试hooks
        self.test_hooks()
        
        # 测试会话管理
        self.test_session_management()
        
        # 测试记忆系统
        self.test_memory_system()
        
        # 测试配置
        self.test_configuration()
        
        # 生成测试报告
        self.generate_report()
    
    def test_skills(self):
        """测试技能"""
        print("-" * 80)
        print("测试技能")
        print("-" * 80)
        
        # 测试技能列表
        expected_skills = [
            "bidding-automation",
            "folder-automation",
            "content-engineering",
            "verification-loop",
            "continuous-learning",
            "token-optimization",
            "security-review",
            "subagent-orchestration",
            "project-automation",
            "claudeception-adapter",
            "deerflow-adapter"
        ]
        
        for skill_name in expected_skills:
            self.test_skill(skill_name)
        
        print()
    
    def test_skill(self, skill_name: str):
        """测试单个技能"""
        skill_dir = self.skills_dir / skill_name
        skill_file = skill_dir / "SKILL.md"
        
        result = {
            "type": "skill",
            "name": skill_name,
            "tests": []
        }
        
        # 测试1: 技能目录存在
        test1 = {
            "name": "技能目录存在",
            "passed": skill_dir.exists(),
            "message": "技能目录存在" if skill_dir.exists() else "技能目录不存在"
        }
        result["tests"].append(test1)
        
        # 测试2: SKILL.md文件存在
        test2 = {
            "name": "SKILL.md文件存在",
            "passed": skill_file.exists(),
            "message": "SKILL.md文件存在" if skill_file.exists() else "SKILL.md文件不存在"
        }
        result["tests"].append(test2)
        
        # 测试3: SKILL.md文件可读
        test3 = {
            "name": "SKILL.md文件可读",
            "passed": False,
            "message": ""
        }
        
        if skill_file.exists():
            try:
                with open(skill_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                test3["passed"] = len(content) > 0
                test3["message"] = f"SKILL.md文件可读，内容长度: {len(content)}字符"
            except Exception as e:
                test3["message"] = f"SKILL.md文件读取失败: {str(e)}"
        else:
            test3["message"] = "SKILL.md文件不存在，无法读取"
        
        result["tests"].append(test3)
        
        # 测试4: SKILL.md包含必要章节
        test4 = {
            "name": "SKILL.md包含必要章节",
            "passed": False,
            "message": ""
        }
        
        if skill_file.exists():
            try:
                with open(skill_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                required_sections = ["技能概述", "核心功能", "工作流程", "配置参数"]
                found_sections = [s for s in required_sections if s in content]
                
                test4["passed"] = len(found_sections) >= 3
                test4["message"] = f"找到{len(found_sections)}/{len(required_sections)}个必要章节"
            except Exception as e:
                test4["message"] = f"检查章节失败: {str(e)}"
        else:
            test4["message"] = "SKILL.md文件不存在，无法检查章节"
        
        result["tests"].append(test4)
        
        # 计算通过率
        passed_tests = sum(1 for t in result["tests"] if t["passed"])
        total_tests = len(result["tests"])
        result["pass_rate"] = passed_tests / total_tests if total_tests > 0 else 0
        result["status"] = "PASS" if result["pass_rate"] >= 0.75 else "FAIL"
        
        # 打印结果
        status_icon = "✓" if result["status"] == "PASS" else "✗"
        print(f"{status_icon} {skill_name}: {passed_tests}/{total_tests}测试通过 ({result['pass_rate']*100:.0f}%)")
        
        self.test_results.append(result)
    
    def test_hooks(self):
        """测试hooks"""
        print("-" * 80)
        print("测试Hooks")
        print("-" * 80)
        
        expected_hooks = [
            "pre-commit",
            "post-commit",
            "session-start",
            "session-end"
        ]
        
        for hook_name in expected_hooks:
            self.test_hook(hook_name)
        
        print()
    
    def test_hook(self, hook_name: str):
        """测试单个hook"""
        hook_file = self.hooks_dir / f"{hook_name}.py"
        config_file = self.hooks_dir / "config.json"
        
        result = {
            "type": "hook",
            "name": hook_name,
            "tests": []
        }
        
        # 测试1: hook文件存在
        test1 = {
            "name": "hook文件存在",
            "passed": hook_file.exists(),
            "message": "hook文件存在" if hook_file.exists() else "hook文件不存在"
        }
        result["tests"].append(test1)
        
        # 测试2: hook文件可读
        test2 = {
            "name": "hook文件可读",
            "passed": False,
            "message": ""
        }
        
        if hook_file.exists():
            try:
                with open(hook_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                test2["passed"] = len(content) > 0
                test2["message"] = f"hook文件可读，内容长度: {len(content)}字符"
            except Exception as e:
                test2["message"] = f"hook文件读取失败: {str(e)}"
        else:
            test2["message"] = "hook文件不存在，无法读取"
        
        result["tests"].append(test2)
        
        # 测试3: hook在配置中启用
        test3 = {
            "name": "hook在配置中启用",
            "passed": False,
            "message": ""
        }
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                hook_config = config.get("hooks", {}).get(hook_name, {})
                test3["passed"] = hook_config.get("enabled", False)
                test3["message"] = f"hook{'已' if test3['passed'] else '未'}在配置中启用"
            except Exception as e:
                test3["message"] = f"检查配置失败: {str(e)}"
        else:
            test3["message"] = "配置文件不存在，无法检查"
        
        result["tests"].append(test3)
        
        # 计算通过率
        passed_tests = sum(1 for t in result["tests"] if t["passed"])
        total_tests = len(result["tests"])
        result["pass_rate"] = passed_tests / total_tests if total_tests > 0 else 0
        result["status"] = "PASS" if result["pass_rate"] >= 0.67 else "FAIL"
        
        # 打印结果
        status_icon = "✓" if result["status"] == "PASS" else "✗"
        print(f"{status_icon} {hook_name}: {passed_tests}/{total_tests}测试通过 ({result['pass_rate']*100:.0f}%)")
        
        self.test_results.append(result)
    
    def test_session_management(self):
        """测试会话管理"""
        print("-" * 80)
        print("测试会话管理")
        print("-" * 80)
        
        result = {
            "type": "session_management",
            "name": "会话管理",
            "tests": []
        }
        
        # 测试1: 会话目录存在
        test1 = {
            "name": "会话目录存在",
            "passed": self.sessions_dir.exists(),
            "message": f"会话目录{'存在' if self.sessions_dir.exists() else '不存在'}"
        }
        result["tests"].append(test1)
        
        # 测试2: 会话子目录存在
        test2 = {
            "name": "会话子目录存在",
            "passed": False,
            "message": ""
        }
        
        required_subdirs = ["context", "state", "cache"]
        existing_subdirs = [d for d in required_subdirs if (self.sessions_dir / d).exists()]
        
        test2["passed"] = len(existing_subdirs) >= 2
        test2["message"] = f"找到{len(existing_subdirs)}/{len(required_subdirs)}个必要子目录"
        result["tests"].append(test2)
        
        # 测试3: session-start hook可导入
        test3 = {
            "name": "session-start hook可导入",
            "passed": False,
            "message": ""
        }
        
        try:
            sys.path.insert(0, str(self.hooks_dir))
            from session_start import SessionStartHandler
            test3["passed"] = True
            test3["message"] = "session-start hook可成功导入"
        except Exception as e:
            test3["message"] = f"导入失败: {str(e)}"
        
        result["tests"].append(test3)
        
        # 测试4: session-end hook可导入
        test4 = {
            "name": "session-end hook可导入",
            "passed": False,
            "message": ""
        }
        
        try:
            from session_end import SessionEndHandler
            test4["passed"] = True
            test4["message"] = "session-end hook可成功导入"
        except Exception as e:
            test4["message"] = f"导入失败: {str(e)}"
        
        result["tests"].append(test4)
        
        # 计算通过率
        passed_tests = sum(1 for t in result["tests"] if t["passed"])
        total_tests = len(result["tests"])
        result["pass_rate"] = passed_tests / total_tests if total_tests > 0 else 0
        result["status"] = "PASS" if result["pass_rate"] >= 0.75 else "FAIL"
        
        # 打印结果
        status_icon = "✓" if result["status"] == "PASS" else "✗"
        print(f"{status_icon} 会话管理: {passed_tests}/{total_tests}测试通过 ({result['pass_rate']*100:.0f}%)")
        
        self.test_results.append(result)
        print()
    
    def test_memory_system(self):
        """测试记忆系统"""
        print("-" * 80)
        print("测试记忆系统")
        print("-" * 80)
        
        result = {
            "type": "memory_system",
            "name": "记忆系统",
            "tests": []
        }
        
        # 测试1: 记忆目录存在
        test1 = {
            "name": "记忆目录存在",
            "passed": self.memory_dir.exists(),
            "message": f"记忆目录{'存在' if self.memory_dir.exists() else '不存在'}"
        }
        result["tests"].append(test1)
        
        # 测试2: 记忆文件可创建
        test2 = {
            "name": "记忆文件可创建",
            "passed": False,
            "message": ""
        }
        
        try:
            test_file = self.memory_dir / "test_memory.json"
            test_data = {"test": "data", "timestamp": datetime.now().isoformat()}
            
            with open(test_file, 'w', encoding='utf-8') as f:
                json.dump(test_data, f, indent=2, ensure_ascii=False)
            
            # 验证文件
            with open(test_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            
            test2["passed"] = loaded_data == test_data
            test2["message"] = "记忆文件可成功创建和读取"
            
            # 清理测试文件
            test_file.unlink()
        except Exception as e:
            test2["message"] = f"创建记忆文件失败: {str(e)}"
        
        result["tests"].append(test2)
        
        # 计算通过率
        passed_tests = sum(1 for t in result["tests"] if t["passed"])
        total_tests = len(result["tests"])
        result["pass_rate"] = passed_tests / total_tests if total_tests > 0 else 0
        result["status"] = "PASS" if result["pass_rate"] >= 0.5 else "FAIL"
        
        # 打印结果
        status_icon = "✓" if result["status"] == "PASS" else "✗"
        print(f"{status_icon} 记忆系统: {passed_tests}/{total_tests}测试通过 ({result['pass_rate']*100:.0f}%)")
        
        self.test_results.append(result)
        print()
    
    def test_configuration(self):
        """测试配置"""
        print("-" * 80)
        print("测试配置")
        print("-" * 80)
        
        config_file = self.hooks_dir / "config.json"
        
        result = {
            "type": "configuration",
            "name": "配置",
            "tests": []
        }
        
        # 测试1: 配置文件存在
        test1 = {
            "name": "配置文件存在",
            "passed": config_file.exists(),
            "message": "配置文件存在" if config_file.exists() else "配置文件不存在"
        }
        result["tests"].append(test1)
        
        # 测试2: 配置文件可读
        test2 = {
            "name": "配置文件可读",
            "passed": False,
            "message": ""
        }
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                test2["passed"] = True
                test2["message"] = "配置文件可成功读取"
            except Exception as e:
                test2["message"] = f"读取配置文件失败: {str(e)}"
        else:
            test2["message"] = "配置文件不存在，无法读取"
        
        result["tests"].append(test2)
        
        # 测试3: 配置包含所有技能
        test3 = {
            "name": "配置包含所有技能",
            "passed": False,
            "message": ""
        }
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                expected_skills = [
                    "bidding-automation",
                    "folder-automation",
                    "content-engineering",
                    "verification-loop",
                    "continuous-learning",
                    "token-optimization",
                    "security-review",
                    "subagent-orchestration",
                    "project-automation",
                    "claudeception-adapter",
                    "deerflow-adapter"
                ]
                
                configured_skills = config.get("skills", {}).keys()
                found_skills = [s for s in expected_skills if s in configured_skills]
                
                test3["passed"] = len(found_skills) == len(expected_skills)
                test3["message"] = f"配置了{len(found_skills)}/{len(expected_skills)}个技能"
            except Exception as e:
                test3["message"] = f"检查技能配置失败: {str(e)}"
        else:
            test3["message"] = "配置文件不存在，无法检查"
        
        result["tests"].append(test3)
        
        # 测试4: 配置包含所有hooks
        test4 = {
            "name": "配置包含所有hooks",
            "passed": False,
            "message": ""
        }
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                expected_hooks = [
                    "pre-commit",
                    "post-commit",
                    "session-start",
                    "session-end"
                ]
                
                configured_hooks = config.get("hooks", {}).keys()
                found_hooks = [h for h in expected_hooks if h in configured_hooks]
                
                test4["passed"] = len(found_hooks) == len(expected_hooks)
                test4["message"] = f"配置了{len(found_hooks)}/{len(expected_hooks)}个hooks"
            except Exception as e:
                test4["message"] = f"检查hooks配置失败: {str(e)}"
        else:
            test4["message"] = "配置文件不存在，无法检查"
        
        result["tests"].append(test4)
        
        # 计算通过率
        passed_tests = sum(1 for t in result["tests"] if t["passed"])
        total_tests = len(result["tests"])
        result["pass_rate"] = passed_tests / total_tests if total_tests > 0 else 0
        result["status"] = "PASS" if result["pass_rate"] >= 0.75 else "FAIL"
        
        # 打印结果
        status_icon = "✓" if result["status"] == "PASS" else "✗"
        print(f"{status_icon} 配置: {passed_tests}/{total_tests}测试通过 ({result['pass_rate']*100:.0f}%)")
        
        self.test_results.append(result)
        print()
    
    def generate_report(self):
        """生成测试报告"""
        print("=" * 80)
        print("测试报告")
        print("=" * 80)
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        # 统计结果
        total_results = len(self.test_results)
        passed_results = sum(1 for r in self.test_results if r["status"] == "PASS")
        failed_results = total_results - passed_results
        
        # 计算平均通过率
        avg_pass_rate = sum(r["pass_rate"] for r in self.test_results) / total_results if total_results > 0 else 0
        
        print(f"测试时间: {self.start_time} - {end_time}")
        print(f"持续时间: {duration}")
        print()
        print(f"总测试数: {total_results}")
        print(f"通过: {passed_results}")
        print(f"失败: {failed_results}")
        print(f"通过率: {avg_pass_rate*100:.1f}%")
        print()
        
        # 按类型分组
        skills_results = [r for r in self.test_results if r["type"] == "skill"]
        hooks_results = [r for r in self.test_results if r["type"] == "hook"]
        other_results = [r for r in self.test_results if r["type"] not in ["skill", "hook"]]
        
        # 技能测试结果
        if skills_results:
            print("技能测试结果:")
            for result in skills_results:
                status_icon = "✓" if result["status"] == "PASS" else "✗"
                print(f"  {status_icon} {result['name']}: {result['pass_rate']*100:.0f}%")
            print()
        
        # Hooks测试结果
        if hooks_results:
            print("Hooks测试结果:")
            for result in hooks_results:
                status_icon = "✓" if result["status"] == "PASS" else "✗"
                print(f"  {status_icon} {result['name']}: {result['pass_rate']*100:.0f}%")
            print()
        
        # 其他测试结果
        if other_results:
            print("其他测试结果:")
            for result in other_results:
                status_icon = "✓" if result["status"] == "PASS" else "✗"
                print(f"  {status_icon} {result['name']}: {result['pass_rate']*100:.0f}%")
            print()
        
        # 保存报告
        report_file = self.project_root / "迁移功能测试报告.md"
        self.save_report(report_file)
        
        print(f"测试报告已保存到: {report_file}")
        print()
        
        # 总体评估
        if avg_pass_rate >= 0.9:
            print("✓ 测试结果: 优秀")
        elif avg_pass_rate >= 0.8:
            print("✓ 测试结果: 良好")
        elif avg_pass_rate >= 0.7:
            print("⚠ 测试结果: 一般")
        else:
            print("✗ 测试结果: 需要改进")
    
    def save_report(self, report_file: Path):
        """保存测试报告"""
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 迁移功能测试报告\n\n")
            f.write(f"**测试时间:** {self.start_time}\n\n")
            f.write(f"**持续时间:** {datetime.now() - self.start_time}\n\n")
            
            # 统计结果
            total_results = len(self.test_results)
            passed_results = sum(1 for r in self.test_results if r["status"] == "PASS")
            failed_results = total_results - passed_results
            avg_pass_rate = sum(r["pass_rate"] for r in self.test_results) / total_results if total_results > 0 else 0
            
            f.write("## 测试统计\n\n")
            f.write(f"- 总测试数: {total_results}\n")
            f.write(f"- 通过: {passed_results}\n")
            f.write(f"- 失败: {failed_results}\n")
            f.write(f"- 通过率: {avg_pass_rate*100:.1f}%\n\n")
            
            # 详细结果
            f.write("## 详细测试结果\n\n")
            
            for result in self.test_results:
                f.write(f"### {result['name']}\n\n")
                f.write(f"- 状态: {result['status']}\n")
                f.write(f"- 通过率: {result['pass_rate']*100:.0f}%\n\n")
                f.write("测试项:\n\n")
                
                for test in result["tests"]:
                    status_icon = "✓" if test["passed"] else "✗"
                    f.write(f"- {status_icon} {test['name']}: {test['message']}\n")
                
                f.write("\n")

def main():
    """主函数"""
    tester = MigrationTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
