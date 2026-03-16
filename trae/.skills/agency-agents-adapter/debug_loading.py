#!/usr/bin/env python3
"""
调试智能体加载问题
"""

import sys
from pathlib import Path

# 添加技能路径到Python路径
skill_path = Path(__file__).parent
sys.path.insert(0, str(skill_path))

from agency_agents_adapter import AgencyAgentsAdapter


def main():
    adapter = AgencyAgentsAdapter()

    print("="*70)
    print("  调试智能体加载")
    print("="*70)
    print()

    # 检查agency_path
    print(f"Agency路径: {adapter.agency_path}")
    print(f"Agency路径存在: {adapter.agency_path.exists()}")
    print()

    # 检查project_management路径
    pm_path = adapter.agency_path / "project_management"
    print(f"Project Management路径: {pm_path}")
    print(f"Project Management路径存在: {pm_path.exists()}")
    print()

    # 列出project_management目录下的文件
    if pm_path.exists():
        print(f"Project Management目录下的文件:")
        for f in sorted(pm_path.glob("*.md")):
            print(f"  - {f.name}")
        print()

    # 尝试手动加载project_manager-senior.md
    if pm_path.exists():
        file_path = pm_path / "project-manager-senior.md"
        print(f"尝试加载: {file_path.name}")
        agent = adapter._parse_agent_file(file_path)
        if agent:
            print(f"  ✅ 加载成功")
            print(f"  名称: {agent.name}")
            print(f"  类别: {agent.category}")
            print(f"  描述: {agent.description}")
        else:
            print(f"  ❌ 加载失败")
        print()

    # 检查缓存
    print(f"缓存中的智能体数量: {len(adapter.agent_cache)}")
    print()

    # 检查project_management类别的智能体
    print("缓存中project_management类别的智能体:")
    count = 0
    for name, agent in adapter.agent_cache.items():
        if agent.category == "project_management":
            print(f"  - {name}")
            count += 1
    print(f"总计: {count} 个智能体")
    print()

    # 重新加载智能体索引
    print("重新加载智能体索引...")
    adapter.agent_cache = {}
    adapter._load_agent_index()
    print(f"重新加载后的智能体数量: {len(adapter.agent_cache)}")
    print()

    # 再次检查project_management类别的智能体
    print("重新加载后project_management类别的智能体:")
    count = 0
    for name, agent in adapter.agent_cache.items():
        if agent.category == "project_management":
            print(f"  - {name}")
            count += 1
    print(f"总计: {count} 个智能体")
    print()

    # 检查所有类别
    print("所有类别及其智能体数量:")
    categories = {}
    for name, agent in adapter.agent_cache.items():
        if agent.category not in categories:
            categories[agent.category] = 0
        categories[agent.category] += 1

    for category in sorted(categories.keys()):
        print(f"  {category}: {categories[category]} 个智能体")


if __name__ == "__main__":
    main()
