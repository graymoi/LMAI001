#!/usr/bin/env python3
"""
Agency-Agents适配器测试脚本
测试所有核心功能：智能体加载、搜索、推荐、激活和NEXUS协调
"""

import sys
import os
from pathlib import Path

# 添加技能路径到Python路径
skill_path = Path(__file__).parent
sys.path.insert(0, str(skill_path))

from agency_agents_adapter import AgencyAgentsAdapter, NexusOrchestrator, NexusMode


def print_header(title):
    """打印标题"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_success(message):
    """打印成功消息"""
    print(f"✅ {message}")


def print_error(message):
    """打印错误消息"""
    print(f"❌ {message}")


def print_info(message):
    """打印信息消息"""
    print(f"ℹ️  {message}")


def test_adapter_initialization():
    """测试适配器初始化"""
    print_header("测试1: 适配器初始化")
    
    try:
        adapter = AgencyAgentsAdapter()
        print_success("适配器初始化成功")
        return adapter
    except Exception as e:
        print_error(f"适配器初始化失败: {e}")
        return None


def test_agent_loading(adapter):
    """测试智能体加载"""
    print_header("测试2: 智能体加载")
    
    if not adapter:
        print_error("适配器未初始化")
        return False
    
    try:
        # 测试加载单个智能体
        agent = adapter.load_agent("Frontend Developer")
        
        if agent:
            print_success(f"智能体加载成功: {agent.name}")
            print_info(f"  描述: {agent.description}")
            print_info(f"  类别: {agent.category}")
            print_info(f"  表情符号: {agent.emoji}")
            return True
        else:
            print_error("智能体加载失败")
            return False
    
    except Exception as e:
        print_error(f"智能体加载异常: {e}")
        return False


def test_agent_search(adapter):
    """测试智能体搜索"""
    print_header("测试3: 智能体搜索")
    
    if not adapter:
        print_error("适配器未初始化")
        return False
    
    try:
        # 测试搜索
        results = adapter.search_agents("react frontend", limit=5)
        
        if results:
            print_success(f"搜索成功，找到 {len(results)} 个智能体")
            for i, result in enumerate(results, 1):
                print_info(f"  {i}. {result['name']} (分数: {result['score']})")
                print_info(f"     {result['description']}")
            return True
        else:
            print_error("搜索未找到结果")
            return False
    
    except Exception as e:
        print_error(f"搜索异常: {e}")
        return False


def test_agent_recommendation(adapter):
    """测试智能体推荐"""
    print_header("测试4: 智能体推荐")
    
    if not adapter:
        print_error("适配器未初始化")
        return False
    
    try:
        # 测试推荐
        recommendations = adapter.recommend_agents(
            "Build a React application with Tailwind CSS and integrate with REST API"
        )
        
        if recommendations:
            print_success(f"推荐成功，推荐 {len(recommendations)} 个智能体")
            for i, rec in enumerate(recommendations, 1):
                print_info(f"  {i}. {rec['name']} (分数: {rec['score']})")
                print_info(f"     {rec['description']}")
            return True
        else:
            print_error("推荐未找到结果")
            return False
    
    except Exception as e:
        print_error(f"推荐异常: {e}")
        return False


def test_agent_activation(adapter):
    """测试智能体激活"""
    print_header("测试5: 智能体激活")
    
    if not adapter:
        print_error("适配器未初始化")
        return False
    
    try:
        # 测试激活
        result = adapter.activate_agent(
            agent_name="Frontend Developer",
            task="Build a React component for user authentication",
            context={
                "framework": "React",
                "styling": "Tailwind CSS"
            }
        )
        
        if result:
            print_success(f"智能体激活成功: {result.agent_name}")
            print_info(f"  状态: {result.status}")
            print_info(f"  输出: {result.output[:100]}...")
            return True
        else:
            print_error("智能体激活失败")
            return False
    
    except Exception as e:
        print_error(f"激活异常: {e}")
        return False


def test_get_all_agents(adapter):
    """测试获取所有智能体"""
    print_header("测试6: 获取所有智能体")
    
    if not adapter:
        print_error("适配器未初始化")
        return False
    
    try:
        # 获取所有智能体
        agents = adapter.get_all_agents()
        
        if agents:
            print_success(f"获取成功，共 {len(agents)} 个智能体")
            
            # 按类别统计
            categories = adapter.get_categories()
            print_info(f"  类别统计:")
            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                print_info(f"    - {cat}: {count} 个智能体")
            
            return True
        else:
            print_error("未找到智能体")
            return False
    
    except Exception as e:
        print_error(f"获取智能体异常: {e}")
        return False


def test_generate_activation_prompt(adapter):
    """测试生成激活提示"""
    print_header("测试7: 生成激活提示")
    
    if not adapter:
        print_error("适配器未初始化")
        return False
    
    try:
        # 生成激活提示
        prompt = adapter.generate_activation_prompt(
            agent_name="Frontend Developer",
            task="Build a React component for user authentication",
            context={
                "framework": "React",
                "styling": "Tailwind CSS"
            }
        )
        
        if prompt:
            print_success("激活提示生成成功")
            print_info(f"  提示长度: {len(prompt)} 字符")
            print_info(f"  提示预览:")
            print(f"\n{prompt[:500]}...")
            return True
        else:
            print_error("激活提示生成失败")
            return False
    
    except Exception as e:
        print_error(f"生成提示异常: {e}")
        return False


def test_nexus_orchestrator(adapter):
    """测试NEXUS协调器"""
    print_header("测试8: NEXUS协调器")
    
    if not adapter:
        print_error("适配器未初始化")
        return False
    
    try:
        # 创建NEXUS协调器
        orchestrator = NexusOrchestrator(
            adapter=adapter,
            mode=NexusMode.MICRO,
            project_name="测试项目",
            spec_path="F:/AIlm/000项目管理/agency-agents/README.md"
        )
        
        print_success("NEXUS协调器创建成功")
        print_info(f"  模式: {orchestrator.mode.value}")
        print_info(f"  项目: {orchestrator.project_name}")
        print_info(f"  阶段数: {len(orchestrator._get_phases())}")
        
        # 注意：不执行完整管道，只测试初始化
        print_info("  注意: 完整管道执行需要实际AI调用接口")
        
        return True
    
    except Exception as e:
        print_error(f"NEXUS协调器异常: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print_header("Agency-Agents适配器测试")
    print_info("开始测试所有核心功能...\n")
    
    # 初始化适配器
    adapter = test_adapter_initialization()
    
    if not adapter:
        print_error("适配器初始化失败，无法继续测试")
        return
    
    # 运行测试
    test_results = []
    
    test_results.append(("智能体加载", test_agent_loading(adapter)))
    test_results.append(("智能体搜索", test_agent_search(adapter)))
    test_results.append(("智能体推荐", test_agent_recommendation(adapter)))
    test_results.append(("智能体激活", test_agent_activation(adapter)))
    test_results.append(("获取所有智能体", test_get_all_agents(adapter)))
    test_results.append(("生成激活提示", test_generate_activation_prompt(adapter)))
    test_results.append(("NEXUS协调器", test_nexus_orchestrator(adapter)))
    
    # 总结结果
    print_header("测试总结")
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {test_name}")
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print_success("所有测试通过！Agency-Agents适配器工作正常。")
    else:
        print_error(f"{total - passed} 个测试失败，请检查错误信息。")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
