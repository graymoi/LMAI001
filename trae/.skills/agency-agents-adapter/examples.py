#!/usr/bin/env python3
"""
Agency-Agents实际使用示例
展示如何在真实项目中使用Agency-Agents进行项目规划、开发和协调
"""

import sys
from pathlib import Path

# 添加技能路径到Python路径
skill_path = Path(__file__).parent
sys.path.insert(0, str(skill_path))

from agency_agents_adapter import AgencyAgentsAdapter, NexusOrchestrator, NexusMode


def example_1_project_planning():
    """示例1: 项目规划"""
    print("="*70)
    print("示例1: 使用Product Manager进行项目规划")
    print("="*70)
    
    adapter = AgencyAgentsAdapter()
    
    # 激活Product Manager
    result = adapter.activate_agent(
        agent_name="Product Manager",
        task="Create a project plan for '背街小巷诊断数字化管理平台'",
        context={
            "project_name": "背街小巷诊断数字化管理平台",
            "tech_stack": "React + Laravel + PostgreSQL",
            "team_size": "5人",
            "timeline": "8周",
            "requirements": [
                "用户登录和认证",
                "数据可视化",
                "报告生成",
                "移动端支持"
            ]
        }
    )
    
    print(f"\n✅ 智能体: {result.agent_name}")
    print(f"状态: {result.status}")
    print(f"\n输出:")
    print(result.output)
    print()


def example_2_frontend_development():
    """示例2: 前端开发"""
    print("="*70)
    print("示例2: 使用Frontend Developer开发组件")
    print("="*70)
    
    adapter = AgencyAgentsAdapter()
    
    # 激活Frontend Developer
    result = adapter.activate_agent(
        agent_name="Frontend Developer",
        task="Build a user authentication component",
        context={
            "framework": "React",
            "styling": "Tailwind CSS",
            "features": [
                "Email input with validation",
                "Password input with show/hide",
                "Remember me checkbox",
                "Submit button with loading state"
            ],
            "api_endpoint": "/api/auth/login",
            "validation": "Client-side and server-side validation"
        }
    )
    
    print(f"\n✅ 智能体: {result.agent_name}")
    print(f"状态: {result.status}")
    print(f"\n输出:")
    print(result.output)
    print()


def example_3_backend_development():
    """示例3: 后端开发"""
    print("="*70)
    print("示例3: 使用Backend Architect设计API")
    print("="*70)
    
    adapter = AgencyAgentsAdapter()
    
    # 激活Backend Architect
    result = adapter.activate_agent(
        agent_name="Backend Architect",
        task="Design authentication API endpoints",
        context={
            "framework": "Laravel",
            "database": "PostgreSQL",
            "endpoints": [
                "POST /api/auth/login",
                "POST /api/auth/register",
                "POST /api/auth/logout",
                "GET /api/auth/me"
            ],
            "authentication": "JWT tokens",
            "security": "Rate limiting, input validation, SQL injection prevention"
        }
    )
    
    print(f"\n✅ 智能体: {result.agent_name}")
    print(f"状态: {result.status}")
    print(f"\n输出:")
    print(result.output)
    print()


def example_4_quality_assurance():
    """示例4: 质量保证"""
    print("="*70)
    print("示例4: 使用Evidence Collector进行质量验证")
    print("="*70)
    
    adapter = AgencyAgentsAdapter()
    
    # 激活Evidence Collector
    result = adapter.activate_agent(
        agent_name="Evidence Collector",
        task="Verify authentication feature implementation",
        context={
            "feature": "User Authentication",
            "requirements": [
                "Login form works correctly",
                "Registration form works correctly",
                "JWT token generation works correctly",
                "Error handling works correctly"
            ],
            "test_cases": [
                "Valid credentials login",
                "Invalid credentials login",
                "Email validation",
                "Password strength validation"
            ]
        }
    )
    
    print(f"\n✅ 智能体: {result.agent_name}")
    print(f"状态: {result.status}")
    print(f"\n输出:")
    print(result.output)
    print()


def example_5_agent_coordination():
    """示例5: 智能体协调"""
    print("="*70)
    print("示例5: 多智能体协调开发")
    print("="*70)
    
    adapter = AgencyAgentsAdapter()
    
    # 共享上下文
    shared_context = {
        "project": "背街小巷诊断数字化管理平台",
        "phase": "Development",
        "tech_stack": "React + Laravel + PostgreSQL"
    }
    
    # 1. 激活前端开发智能体
    print("\n[步骤1] 激活Frontend Developer...")
    frontend_result = adapter.activate_agent(
        agent_name="Frontend Developer",
        task="Build authentication UI components",
        context={**shared_context, "framework": "React", "styling": "Tailwind CSS"}
    )
    print(f"✅ Frontend Developer完成: {frontend_result.status}")
    
    # 2. 激活后端开发智能体
    print("\n[步骤2] 激活Backend Architect...")
    backend_result = adapter.activate_agent(
        agent_name="Backend Architect",
        task="Design authentication API",
        context={**shared_context, "framework": "Laravel", "database": "PostgreSQL"}
    )
    print(f"✅ Backend Architect完成: {backend_result.status}")
    
    # 3. 激活质量保证智能体
    print("\n[步骤3] 激活Evidence Collector...")
    qa_result = adapter.activate_agent(
        agent_name="Evidence Collector",
        task="Verify authentication feature",
        context={**shared_context, "feature": "User Authentication"}
    )
    print(f"✅ Evidence Collector完成: {qa_result.status}")
    
    print()


def example_6_nexus_sprint():
    """示例6: NEXUS-Sprint模式"""
    print("="*70)
    print("示例6: 使用NEXUS-Sprint模式开发MVP")
    print("="*70)
    
    adapter = AgencyAgentsAdapter()
    
    # 创建NEXUS-Sprint协调器
    orchestrator = NexusOrchestrator(
        adapter=adapter,
        mode=NexusMode.SPRINT,
        project_name="背街小巷诊断数字化管理平台 MVP",
        spec_path="F:/AIlm/000项目管理/agency-agents/README.md"
    )
    
    print(f"\n✅ NEXUS协调器创建成功")
    print(f"模式: {orchestrator.mode.value}")
    print(f"项目: {orchestrator.project_name}")
    print(f"阶段数: {len(orchestrator._get_phases())}")
    
    # 显示阶段信息
    print(f"\n阶段规划:")
    phases = orchestrator._get_phases()
    for i, phase in enumerate(phases, 1):
        print(f"  Phase {i}: {phase['name']}")
        print(f"    智能体: {', '.join(phase['agents'][:3])}...")
    
    print(f"\n注意: 完整管道执行需要实际AI调用接口")
    print()


def example_7_search_and_recommend():
    """示例7: 智能体搜索和推荐"""
    print("="*70)
    print("示例7: 智能体搜索和推荐")
    print("="*70)
    
    adapter = AgencyAgentsAdapter()
    
    # 搜索智能体
    print("\n[搜索] 搜索'frontend'相关智能体:")
    search_results = adapter.search_agents("frontend", limit=3)
    for i, result in enumerate(search_results, 1):
        print(f"  {i}. {result['name']} (分数: {result['score']})")
        print(f"     {result['description']}")
    
    # 推荐智能体
    print("\n[推荐] 推荐智能体用于'Build a React dashboard':")
    recommendations = adapter.recommend_agents("Build a React dashboard with data visualization")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"  {i}. {rec['name']} (分数: {rec['score']})")
        print(f"     {rec['description']}")
    
    print()


def example_8_custom_workflow():
    """示例8: 自定义工作流"""
    print("="*70)
    print("示例8: 自定义工作流 - 完整功能开发")
    print("="*70)
    
    adapter = AgencyAgentsAdapter()
    
    # 定义工作流
    workflow = [
        {
            "agent": "Product Manager",
            "task": "Create task breakdown",
            "context": {"feature": "User Dashboard"}
        },
        {
            "agent": "UX Architect",
            "task": "Design dashboard layout",
            "context": {"feature": "User Dashboard"}
        },
        {
            "agent": "Frontend Developer",
            "task": "Build dashboard components",
            "context": {"framework": "React", "styling": "Tailwind CSS"}
        },
        {
            "agent": "Backend Architect",
            "task": "Design dashboard API",
            "context": {"framework": "Laravel"}
        },
        {
            "agent": "Evidence Collector",
            "task": "Verify dashboard implementation",
            "context": {"feature": "User Dashboard"}
        }
    ]
    
    # 执行工作流
    print(f"\n执行工作流: 'User Dashboard'开发")
    print(f"共 {len(workflow)} 个步骤\n")
    
    for i, step in enumerate(workflow, 1):
        print(f"[步骤 {i}] 激活 {step['agent']}...")
        result = adapter.activate_agent(
            agent_name=step["agent"],
            task=step["task"],
            context=step["context"]
        )
        print(f"✅ {step['agent']}完成: {result.status}")
    
    print()


def main():
    """运行所有示例"""
    print("\n" + "="*70)
    print("  Agency-Agents实际使用示例")
    print("="*70)
    print()
    
    # 运行示例
    example_1_project_planning()
    example_2_frontend_development()
    example_3_backend_development()
    example_4_quality_assurance()
    example_5_agent_coordination()
    example_6_nexus_sprint()
    example_7_search_and_recommend()
    example_8_custom_workflow()
    
    print("="*70)
    print("  所有示例执行完成！")
    print("="*70)
    print()


if __name__ == "__main__":
    main()
