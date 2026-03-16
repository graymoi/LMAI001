#!/usr/bin/env python3
"""
Agency-Agents适配器
为Trae IDE提供Agency-Agents的131个专业化AI智能体的访问和协调功能
"""

import json
import re
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum


class NexusMode(Enum):
    """NEXUS工作模式"""
    FULL = "NEXUS-Full"      # 完整产品开发（12-24周）
    SPRINT = "NEXUS-Sprint"  # 功能/MVP开发（2-6周）
    MICRO = "NEXUS-Micro"    # 特定任务（1-5天）


@dataclass
class AgentConfig:
    """智能体配置"""
    name: str
    description: str
    category: str
    color: str = "blue"
    emoji: str = "🤖"
    vibe: str = ""
    role: str = ""
    personality: str = ""
    experience: str = ""
    core_mission: str = ""
    critical_rules: str = ""
    technical_deliverables: str = ""
    file_path: str = ""


@dataclass
class AgentResult:
    """智能体执行结果"""
    status: str
    output: str
    agent_name: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgencyAgentsAdapter:
    """Agency-Agents适配器类"""
    
    def __init__(self, config_path: str = None):
        """
        初始化Agency-Agents适配器
        
        Args:
            config_path: 配置文件路径
        """
        # 加载配置
        if config_path is None:
            config_path = Path(__file__).parent / "config.json"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 设置路径
        self.agency_path = Path(self.config["config"]["agency_agents_path"])
        
        # 加载智能体目录
        self.agent_cache = {}
        self._load_agent_index()
    
    def _load_agent_index(self):
        """加载智能体索引"""
        categories = [
            "engineering", "marketing", "design", "sales", "project_management",
            "testing", "support", "product", "paid_media", "game_development",
            "spatial_computing", "specialized", "academic"
        ]
        
        for category in categories:
            category_path = self.agency_path / category
            if category_path.exists():
                for agent_file in category_path.glob("*.md"):
                    try:
                        agent = self._parse_agent_file(agent_file)
                        if agent:
                            self.agent_cache[agent.name] = agent
                    except Exception as e:
                        print(f"Warning: Failed to load {agent_file}: {e}")
    
    def _parse_agent_file(self, file_path: Path) -> Optional[AgentConfig]:
        """
        解析智能体文件
        
        Args:
            file_path: 智能体文件路径
            
        Returns:
            智能体配置或None
        """
        content = file_path.read_text(encoding='utf-8')
        
        # 解析YAML frontmatter
        frontmatter = self._parse_frontmatter(content)
        
        if not frontmatter:
            return None
        
        # 提取body
        body = self._extract_body(content)
        
        # 创建智能体配置
        agent = AgentConfig(
            name=frontmatter.get("name", ""),
            description=frontmatter.get("description", ""),
            category=file_path.parent.name,
            color=frontmatter.get("color", "blue"),
            emoji=frontmatter.get("emoji", "🤖"),
            vibe=frontmatter.get("vibe", ""),
            file_path=str(file_path)
        )
        
        # 从body中提取其他信息
        agent.role = self._extract_section(body, "Your Identity & Memory")
        agent.personality = self._extract_section(body, "Personality")
        agent.core_mission = self._extract_section(body, "Your Core Mission")
        agent.critical_rules = self._extract_section(body, "Critical Rules You Must Follow")
        agent.technical_deliverables = self._extract_section(body, "Your Technical Deliverables")
        
        return agent
    
    def _parse_frontmatter(self, content: str) -> Optional[Dict[str, str]]:
        """
        解析YAML frontmatter
        
        Args:
            content: 文件内容
            
        Returns:
            frontmatter字典或None
        """
        lines = content.split('\n')
        
        if not lines or lines[0] != '---':
            return None
        
        frontmatter_lines = []
        for line in lines[1:]:
            if line == '---':
                break
            frontmatter_lines.append(line)
        
        frontmatter_text = '\n'.join(frontmatter_lines)
        
        # 简单解析YAML
        frontmatter = {}
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()
        
        return frontmatter
    
    def _extract_body(self, content: str) -> str:
        """
        提取body内容
        
        Args:
            content: 文件内容
            
        Returns:
            body内容
        """
        lines = content.split('\n')
        
        # 找到第二个---之后的内容
        dash_count = 0
        body_lines = []
        in_body = False
        
        for line in lines:
            if line == '---':
                dash_count += 1
                if dash_count == 2:
                    in_body = True
                continue
            
            if in_body:
                body_lines.append(line)
        
        return '\n'.join(body_lines)
    
    def _extract_section(self, body: str, section_title: str) -> str:
        """
        提取特定章节内容
        
        Args:
            body: body内容
            section_title: 章节标题
            
        Returns:
            章节内容
        """
        # 查找章节
        pattern = rf"## {re.escape(section_title)}\s*\n(.*?)(?=\n## |\n---|$)"
        match = re.search(pattern, body, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        return ""
    
    def load_agent(self, agent_name: str) -> Optional[AgentConfig]:
        """
        加载智能体配置
        
        Args:
            agent_name: 智能体名称
            
        Returns:
            智能体配置或None
        """
        return self.agent_cache.get(agent_name)
    
    def search_agents(self, query: str, category: str = None, limit: int = 5) -> List[Dict[str, Any]]:
        """
        搜索智能体
        
        Args:
            query: 搜索查询
            category: 类别过滤（可选）
            limit: 返回数量限制
            
        Returns:
            匹配的智能体列表
        """
        results = []
        query_lower = query.lower()
        
        for agent_name, agent in self.agent_cache.items():
            # 类别过滤
            if category and agent.category != category:
                continue
            
            # 计算匹配分数
            score = self._calculate_match_score(query_lower, agent_name, agent.description)
            
            if score > 0:
                results.append({
                    "name": agent_name,
                    "category": agent.category,
                    "score": score,
                    "description": agent.description,
                    "emoji": agent.emoji
                })
        
        # 按分数排序
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:limit]
    
    def _calculate_match_score(self, query: str, agent_name: str, description: str) -> float:
        """
        计算匹配分数
        
        Args:
            query: 搜索查询
            agent_name: 智能体名称
            description: 智能体描述
            
        Returns:
            匹配分数（0-1）
        """
        agent_name_lower = agent_name.lower()
        description_lower = description.lower()
        
        score = 0.0
        
        # 名称完全匹配
        if query == agent_name_lower:
            score += 1.0
        
        # 名称包含匹配
        elif query in agent_name_lower:
            score += 0.8
        
        # 描述包含匹配
        if query in description_lower:
            score += 0.5
        
        # 关键词匹配
        query_words = set(query.split())
        name_words = set(agent_name_lower.replace('-', ' ').split())
        desc_words = set(description_lower.split())
        
        name_matches = len(query_words & name_words)
        desc_matches = len(query_words & desc_words)
        
        if name_matches > 0:
            score += name_matches / len(query_words) * 0.6
        
        if desc_matches > 0:
            score += desc_matches / len(query_words) * 0.4
        
        return min(score, 1.0)
    
    def recommend_agents(self, task_description: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        推荐智能体
        
        Args:
            task_description: 任务描述
            context: 上下文信息（可选）
            
        Returns:
            推荐的智能体列表
        """
        # 提取关键词
        keywords = self._extract_keywords(task_description)
        
        # 搜索匹配的智能体
        candidates = []
        for keyword in keywords:
            matches = self.search_agents(keyword, limit=3)
            candidates.extend(matches)
        
        # 去重和排序
        unique_candidates = {}
        for candidate in candidates:
            name = candidate["name"]
            if name not in unique_candidates:
                unique_candidates[name] = candidate
            else:
                # 累加分数
                unique_candidates[name]["score"] += candidate["score"]
        
        # 按分数排序
        sorted_candidates = sorted(
            unique_candidates.values(),
            key=lambda x: x["score"],
            reverse=True
        )
        
        return sorted_candidates[:5]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        提取关键词
        
        Args:
            text: 文本
            
        Returns:
            关键词列表
        """
        keywords = []
        
        # 常见技术关键词
        tech_keywords = [
            "frontend", "backend", "react", "vue", "angular", "python",
            "javascript", "typescript", "database", "api", "ui", "ux",
            "design", "marketing", "sales", "testing", "devops",
            "security", "mobile", "game", "ai", "ml", "data",
            "project", "management", "documentation", "architecture",
            "development", "deployment", "monitoring", "optimization"
        ]
        
        text_lower = text.lower()
        for keyword in tech_keywords:
            if keyword in text_lower:
                keywords.append(keyword)
        
        return keywords
    
    def generate_activation_prompt(self, agent_name: str, task: str, context: Dict[str, Any] = None) -> str:
        """
        生成智能体激活提示
        
        Args:
            agent_name: 智能体名称
            task: 任务描述
            context: 上下文信息
            
        Returns:
            激活提示字符串
        """
        # 加载智能体配置
        agent = self.load_agent(agent_name)
        
        if not agent:
            raise ValueError(f"智能体不存在: {agent_name}")
        
        # 构建激活提示
        prompt = f"""You are {agent.name}, an expert {agent.description}.

## Your Identity & Memory
- Role: {agent.role or agent.description}
- Personality: {agent.personality or 'Professional and focused'}
- Experience: {agent.experience or 'Extensive experience in the field'}

## Current Task
{task}

"""
        
        # 添加上下文
        if context:
            prompt += "## Context\n"
            for key, value in context.items():
                prompt += f"- **{key}**: {value}\n"
            prompt += "\n"
        
        # 添加核心使命
        if agent.core_mission:
            prompt += f"## Your Core Mission\n{agent.core_mission}\n\n"
        
        # 添加关键规则
        if agent.critical_rules:
            prompt += f"## Critical Rules You Must Follow\n{agent.critical_rules}\n\n"
        
        # 添加技术交付物
        if agent.technical_deliverables:
            prompt += f"## Your Technical Deliverables\n{agent.technical_deliverables}\n\n"
        
        return prompt
    
    def activate_agent(self, agent_name: str, task: str, context: Dict[str, Any] = None) -> AgentResult:
        """
        激活智能体（模拟）
        
        Args:
            agent_name: 智能体名称
            task: 任务描述
            context: 上下文信息
            
        Returns:
            执行结果
        """
        # 生成激活提示
        prompt = self.generate_activation_prompt(agent_name, task, context)
        
        # 这里需要实际的AI调用接口
        # 返回模拟结果
        return AgentResult(
            status="SUCCESS",
            output=f"Task '{task}' would be executed by {agent_name}",
            agent_name=agent_name,
            metadata={
                "prompt": prompt,
                "context": context
            }
        )
    
    def get_all_agents(self, category: str = None) -> List[AgentConfig]:
        """
        获取所有智能体
        
        Args:
            category: 类别过滤（可选）
            
        Returns:
            智能体列表
        """
        agents = list(self.agent_cache.values())
        
        if category:
            agents = [agent for agent in agents if agent.category == category]
        
        return agents
    
    def get_categories(self) -> Dict[str, int]:
        """
        获取所有类别及其智能体数量
        
        Returns:
            类别字典
        """
        categories = {}
        
        for agent in self.agent_cache.values():
            cat = agent.category
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1
        
        return categories


class NexusOrchestrator:
    """NEXUS协调器"""
    
    def __init__(self, adapter: AgencyAgentsAdapter, mode: NexusMode, project_name: str, spec_path: str):
        """
        初始化NEXUS协调器
        
        Args:
            adapter: Agency-Agents适配器
            mode: NEXUS模式
            project_name: 项目名称
            spec_path: 项目规格路径
        """
        self.adapter = adapter
        self.mode = mode
        self.project_name = project_name
        self.spec_path = spec_path
        self.current_phase = 0
        self.phase_results = {}
        self.handoff_history = []
    
    def execute_pipeline(self) -> bool:
        """执行完整的NEXUS管道"""
        phases = self._get_phases()
        
        for phase_num, phase in enumerate(phases, 1):
            self.current_phase = phase_num
            
            print(f"\n{'='*60}")
            print(f"Phase {phase_num}: {phase['name']}")
            print(f"{'='*60}")
            
            # 执行阶段
            result = self._execute_phase(phase)
            
            # 质量门控
            if not self._quality_gate(result):
                print(f"❌ Phase {phase_num} failed quality gate")
                return False
            
            # 保存结果
            self.phase_results[phase_num] = result
            
            print(f"✅ Phase {phase_num} completed successfully")
        
        print(f"\n🎉 {self.project_name} completed successfully!")
        return True
    
    def _get_phases(self) -> List[Dict[str, Any]]:
        """获取阶段列表"""
        if self.mode == NexusMode.FULL:
            return [
                {"name": "Discovery", "agents": ["Trend Researcher", "Feedback Synthesizer", "UX Researcher", "Analytics Reporter", "Legal Compliance Checker", "Tool Evaluator"]},
                {"name": "Strategy", "agents": ["Studio Producer", "Senior Project Manager", "Sprint Prioritizer", "UX Architect", "Brand Guardian", "Backend Architect", "Finance Tracker"]},
                {"name": "Foundation", "agents": ["DevOps Automator", "Frontend Developer", "Backend Architect", "UX Architect", "Infrastructure Maintainer"]},
                {"name": "Build", "agents": ["Frontend Developer", "Backend Architect", "DevOps Automator"], "qa_loop": True},
                {"name": "Harden", "agents": ["Reality Checker", "Performance Benchmarker", "API Tester", "Legal Compliance Checker"]},
                {"name": "Launch", "agents": ["Growth Hacker", "Content Creator", "DevOps Automator"]},
                {"name": "Operate", "agents": ["Analytics Reporter", "Infrastructure Maintainer", "Support Responder"]}
            ]
        elif self.mode == NexusMode.SPRINT:
            return [
                {"name": "Strategy", "agents": ["Senior Project Manager", "Sprint Prioritizer", "UX Architect", "Brand Guardian", "Backend Architect"]},
                {"name": "Foundation", "agents": ["DevOps Automator", "Frontend Developer", "Backend Architect"]},
                {"name": "Build", "agents": ["Frontend Developer", "Backend Architect"], "qa_loop": True},
                {"name": "Harden", "agents": ["Reality Checker", "Performance Benchmarker", "API Tester"]},
                {"name": "Launch", "agents": ["Growth Hacker", "Content Creator"]}
            ]
        else:  # MICRO
            return [
                {"name": "Execute", "agents": ["Frontend Developer"], "qa_loop": True}
            ]
    
    def _execute_phase(self, phase: Dict[str, Any]) -> Dict[str, AgentResult]:
        """
        执行阶段
        
        Args:
            phase: 阶段配置
            
        Returns:
            阶段结果
        """
        results = {}
        
        # 激活智能体
        for agent_name in phase["agents"]:
            print(f"\n🤖 Activating: {agent_name}")
            
            # 生成激活提示
            prompt = self.adapter.generate_activation_prompt(
                agent_name=agent_name,
                task=f"Execute Phase {self.current_phase}: {phase['name']}",
                context={
                    "project": self.project_name,
                    "spec": self.spec_path,
                    "phase": phase['name']
                }
            )
            
            # 执行任务
            result = self.adapter.activate_agent(agent_name, f"Execute Phase {self.current_phase}: {phase['name']}")
            results[agent_name] = result
        
        # QA循环
        if phase.get("qa_loop", False):
            results = self._run_qa_loop(results)
        
        return results
    
    def _run_qa_loop(self, results: Dict[str, AgentResult]) -> Dict[str, AgentResult]:
        """
        运行Dev↔QA循环
        
        Args:
            results: 开发结果
            
        Returns:
            验证后的结果
        """
        max_retries = self.adapter.config["nexus"]["qa_loop"]["max_retries"]
        retry_count = 0
        
        while retry_count < max_retries:
            # 激活QA智能体
            qa_result = self.adapter.activate_agent(
                agent_name="Evidence Collector",
                task="Verify implementation quality",
                context={
                    "implementation": results,
                    "retry_count": retry_count
                }
            )
            
            if qa_result.status == "SUCCESS":
                print("✅ QA verification passed")
                break
            
            print(f"⚠️ QA verification failed (attempt {retry_count + 1}/{max_retries})")
            
            # 修复问题
            for agent_name, result in results.items():
                fix_result = self.adapter.activate_agent(
                    agent_name=agent_name,
                    task=f"Fix QA feedback",
                    context={
                        "original_result": result,
                        "qa_feedback": qa_result
                    }
                )
                
                results[agent_name] = fix_result
            
            retry_count += 1
        
        return results
    
    def _quality_gate(self, result: Dict[str, AgentResult]) -> bool:
        """
        质量门控检查
        
        Args:
            result: 阶段结果
            
        Returns:
            是否通过质量门控
        """
        # 检查所有智能体都成功完成
        for agent_name, agent_result in result.items():
            if agent_result.status != "SUCCESS":
                return False
        
        return True


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Agency-Agents适配器')
    parser.add_argument('command', choices=['search', 'activate', 'recommend', 'list', 'nexus'], help='命令')
    parser.add_argument('--agent', help='智能体名称')
    parser.add_argument('--task', help='任务描述')
    parser.add_argument('--query', help='搜索查询')
    parser.add_argument('--category', help='类别过滤')
    parser.add_argument('--mode', choices=['full', 'sprint', 'micro'], default='sprint', help='NEXUS模式')
    parser.add_argument('--project', help='项目名称')
    parser.add_argument('--spec', help='项目规格路径')
    
    args = parser.parse_args()
    
    # 创建适配器实例
    adapter = AgencyAgentsAdapter()
    
    # 执行命令
    if args.command == 'search':
        results = adapter.search_agents(args.query, args.category)
        for result in results:
            print(f"{result['name']} (分数: {result['score']}) - {result['description']}")
    
    elif args.command == 'activate':
        result = adapter.activate_agent(args.agent, args.task)
        print(f"状态: {result.status}")
        print(f"输出: {result.output}")
    
    elif args.command == 'recommend':
        recommendations = adapter.recommend_agents(args.task)
        for rec in recommendations:
            print(f"{rec['name']} (分数: {rec['score']}) - {rec['description']}")
    
    elif args.command == 'list':
        agents = adapter.get_all_agents(args.category)
        for agent in agents:
            print(f"{agent.emoji} {agent.name} - {agent.description}")
    
    elif args.command == 'nexus':
        nexus_mode = NexusMode.FULL if args.mode == 'full' else (NexusMode.SPRINT if args.mode == 'sprint' else NexusMode.MICRO)
        
        orchestrator = NexusOrchestrator(
            adapter=adapter,
            mode=nexus_mode,
            project_name=args.project,
            spec_path=args.spec
        )
        
        success = orchestrator.execute_pipeline()
        
        if success:
            print("项目完成！")
        else:
            print("项目失败")


if __name__ == "__main__":
    main()
