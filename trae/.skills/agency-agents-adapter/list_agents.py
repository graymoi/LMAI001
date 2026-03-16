#!/usr/bin/env python3
"""
列出所有可用的Agency-Agents智能体
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
    print("  所有可用的Agency-Agents智能体")
    print("="*70)
    print()

    # 获取所有智能体
    agents = adapter.get_all_agents()

    # 按类别分组
    categories = {}
    for agent in agents:
        if agent.category not in categories:
            categories[agent.category] = []
        categories[agent.category].append(agent)

    # 按类别输出
    for category in sorted(categories.keys()):
        print(f"\n{category.upper()}:")
        print("-" * 70)
        for agent in sorted(categories[category], key=lambda x: x.name):
            print(f"  - {agent.name}")

    print()
    print("="*70)
    print(f"  总计: {len(agents)} 个智能体")
    print("="*70)


if __name__ == "__main__":
    main()
