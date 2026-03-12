# Trae IDE 配置文件夹

## 文件夹概述

本文件夹包含Trae IDE的所有配置文件，包括agents、skills、hooks、rules等，用于项目自动化管理和智能协作。

---

## 文件夹结构

```
trae/
├── agents.md              # 智能体配置
├── claude.me             # Claude AI助手配置
├── claude.local.md       # Claude本地配置
├── trae.md              # Trae IDE项目配置
├── .skills/             # 技能配置文件夹
│   ├── bidding-automation/    # 标书编写自动化技能
│   │   └── SKILL.md
│   └── folder-automation/    # 文件夹管理自动化技能
│       └── SKILL.md
├── .hooks/              # Git钩子配置文件夹
│   ├── pre-commit.py          # 提交前钩子
│   ├── post-commit.py         # 提交后钩子
│   └── config.json           # 钩子配置文件
└── .rules/              # 项目规则文件夹
    └── project-rules.md       # 项目管理规则
```

---

## 文件说明

### 1. agents.md

**文件类型：** 智能体配置文件
**文件用途：** 定义项目管理系统的智能体配置
**包含内容：**
- 智能体架构
- 智能体职责
- 智能体协作机制
- 智能体进化机制
- 智能体经济价值

**使用场景：**
- 智能体调用
- 智能体协作
- 智能体管理

### 2. claude.me

**文件类型：** Claude AI助手配置文件
**文件用途：** 定义Claude AI助手的工作原则和流程
**包含内容：**
- Claude角色定义
- 工作原则
- 工作流程
- 智能体调用
- 文件管理规则
- 自动化规则
- 质量标准
- 性能指标
- 经济价值
- 进化机制

**使用场景：**
- Claude AI助手工作指导
- 任务执行规范
- 质量控制标准

### 3. claude.local.md

**文件类型：** Claude本地配置文件
**文件用途：** 定义Claude的本地环境配置
**包含内容：**
- 本地环境配置
- 本地路径配置
- 本地工具配置
- 本地自动化配置
- 本地日志配置
- 本地备份配置
- 本地缓存配置
- 本地临时文件配置
- 本地监控配置
- 本地通知配置
- 本地安全配置
- 本地性能配置
- 本地调试配置
- 本地测试配置
- 本地部署配置

**使用场景：**
- 本地环境设置
- 本地工具配置
- 本地自动化配置

### 4. trae.md

**文件类型：** Trae IDE项目配置文件
**文件用途：** 定义Trae IDE的项目配置
**包含内容：**
- 项目信息
- 项目核心目标
- 项目工作流程
- 项目文档管理
- 项目规则
- 项目协作规则
- 项目自动化规则
- 项目经济价值规则
- 项目进化规则

**使用场景：**
- 项目管理
- 项目协作
- 项目自动化

---

## .skills 文件夹

### 文件夹用途

存放所有技能配置文件，用于自动化任务执行。

### 默认归类规则

#### 1. 文档管理类技能

**存放位置：** `.skills/document-management/`
**技能类型：**
- 文档生成
- 文档检查
- 文档优化
- 文档转换
- 文档导出

**示例技能：**
- `bidding-automation` - 标书编写自动化

#### 2. 代码管理类技能

**存放位置：** `.skills/code-management/`
**技能类型：**
- 代码生成
- 代码检查
- 代码优化
- 代码重构
- 代码测试

**示例技能：**
- `code-review` - 代码审查自动化
- `code-format` - 代码格式化

#### 3. 文件管理类技能

**存放位置：** `.skills/file-management/`
**技能类型：**
- 文件整理
- 文件分类
- 文件重命名
- 文件去重
- 文件备份

**示例技能：**
- `folder-automation` - 文件夹管理自动化

#### 4. 数据管理类技能

**存放位置：** `.skills/data-management/`
**技能类型：**
- 数据收集
- 数据分析
- 数据可视化
- 数据清洗
- 数据转换

**示例技能：**
- `data-analysis` - 数据分析自动化
- `data-visualization` - 数据可视化自动化

#### 5. 项目管理类技能

**存放位置：** `.skills/project-management/`
**技能类型：**
- 项目规划
- 进度跟踪
- 资源管理
- 风险管理
- 质量管理

**示例技能：**
- `project-planning` - 项目规划自动化
- `progress-tracking` - 进度跟踪自动化

#### 6. 自动化类技能

**存放位置：** `.skills/automation/`
**技能类型：**
- 流程自动化
- 任务自动化
- 通知自动化
- 报告自动化
- 备份自动化

**示例技能：**
- `workflow-automation` - 工作流自动化
- `task-automation` - 任务自动化

---

## .hooks 文件夹

### 文件夹用途

存放所有Git钩子脚本，用于自动化Git操作。

### 默认归类规则

#### 1. 提交前钩子

**文件名：** `pre-commit.py`
**触发时机：** 执行git commit命令后，在提交前触发
**主要功能：**
- 文件格式检查
- 文件大小检查
- 文件编码检查
- 文档质量检查
- 代码质量检查

**配置文件：** `config.json`

#### 2. 提交后钩子

**文件名：** `post-commit.py`
**触发时机：** 提交完成后触发
**主要功能：**
- 记录提交日志
- 更新统计信息
- 通知团队
- 触发自动化任务

**配置文件：** `config.json`

#### 3. 其他钩子

**预定义钩子：**
- `pre-push.py` - 推送前钩子
- `post-push.py` - 推送后钩子
- `pre-merge.py` - 合并前钩子
- `post-merge.py` - 合并后钩子

**配置文件：** `config.json`

---

## .rules 文件夹

### 文件夹用途

存放所有项目管理规则，用于规范项目管理行为。

### 默认归类规则

#### 1. 文件管理规则

**文件名：** `file-management-rules.md`
**规则内容：**
- 文件夹结构规则
- 文件命名规则
- 文件内容规则
- 文件组织规则

#### 2. 文档编写规则

**文件名：** `document-writing-rules.md`
**规则内容：**
- 标书编写规则
- 文档质量规则
- 文档格式规则
- 文档审核规则

#### 3. 代码编写规则

**文件名：** `code-writing-rules.md`
**规则内容：**
- 代码规范规则
- 代码质量规则
- 代码安全规则
- 代码测试规则

#### 4. Git管理规则

**文件名：** `git-management-rules.md`
**规则内容：**
- 提交规则
- 分支规则
- 标签规则
- 合并规则

#### 5. 自动化规则

**文件名：** `automation-rules.md`
**规则内容：**
- 自动化触发规则
- 自动化执行规则
- 自动化结果规则
- 自动化优化规则

#### 6. 经济价值规则

**文件名：** `economic-value-rules.md`
**规则内容：**
- 价值创造规则
- 价值评估规则
- 价值优化规则
- 价值报告规则

#### 7. 进化规则

**文件名：** `evolution-rules.md`
**规则内容：**
- 自动进化规则
- 持续改进规则
- 学习进化规则
- 优化进化规则

---

## 新增技能指南

### 1. 创建技能文件夹

```bash
# 在.skills文件夹下创建新的技能文件夹
mkdir trae/.skills/your-skill-name
```

### 2. 创建SKILL.md文件

```bash
# 在技能文件夹下创建SKILL.md文件
touch trae/.skills/your-skill-name/SKILL.md
```

### 3. 编写技能内容

按照以下结构编写技能内容：

```markdown
# 技能名称

## 技能概述
[技能描述]

## 技能功能
[功能列表]

## 技能配置
[配置说明]

## 技能使用
[使用方法]

## 技能优化
[优化方法]

## 技能价值
[价值说明]

## 技能维护
[维护方法]

## 附录
[附加信息]
```

### 4. 配置技能

在`.hooks/config.json`中添加技能配置：

```json
{
  "skills": {
    "your-skill-name": {
      "enabled": true,
      "auto_trigger": true,
      "config_file": ".skills/your-skill-name/config.json"
    }
  }
}
```

---

## 新增钩子指南

### 1. 创建钩子脚本

```bash
# 在.hooks文件夹下创建新的钩子脚本
touch trae/.hooks/your-hook-name.py
```

### 2. 编写钩子脚本

按照以下结构编写钩子脚本：

```python
#!/usr/bin/env python3
"""
钩子描述
"""

import sys
import subprocess
from pathlib import Path

class YourHookHandler:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        # 初始化配置
        
    def run_checks(self):
        """运行检查"""
        # 实现检查逻辑
        pass
        
    def run_actions(self):
        """运行操作"""
        # 实现操作逻辑
        pass

def main():
    handler = YourHookHandler()
    handler.run_actions()

if __name__ == "__main__":
    main()
```

### 3. 配置钩子

在`.hooks/config.json`中添加钩子配置：

```json
{
  "hooks": {
    "your-hook-name": {
      "enabled": true,
      "script": ".hooks/your-hook-name.py",
      "trigger": "commit"
    }
  }
}
```

---

## 新增规则指南

### 1. 创建规则文件

```bash
# 在.rules文件夹下创建新的规则文件
touch trae/.rules/your-rule-name.md
```

### 2. 编写规则内容

按照以下结构编写规则内容：

```markdown
# 规则名称

## 规则概述
[规则描述]

## 规则内容
[规则列表]

## 规则检查清单
[检查清单]

## 更新历史
[更新记录]
```

### 3. 应用规则

在相关配置文件中引用规则：

```json
{
  "rules": {
    "your-rule-name": {
      "enabled": true,
      "enforce": true
    }
  }
}
```

---

## 配置文件说明

### .hooks/config.json

**文件用途：** 钩子和技能的统一配置文件

**配置结构：**
```json
{
  "hooks": {
    "pre-commit": {...},
    "post-commit": {...}
  },
  "automation": {
    "document_automation": {...},
    "code_automation": {...},
    "folder_automation": {...}
  },
  "notifications": {...},
  "logging": {...},
  "skills": {...},
  "rules": {...}
}
```

---

## 维护指南

### 日常维护

1. **检查技能状态**
   - 检查技能是否正常运行
   - 检查技能性能是否正常
   - 检查技能输出是否正确

2. **检查钩子状态**
   - 检查钩子是否正常触发
   - 检查钩子执行是否正常
   - 检查钩子日志是否正常

3. **检查规则状态**
   - 检查规则是否适用
   - 检查规则是否有效
   - 检查规则是否需要更新

### 定期维护

1. **技能优化**
   - 评估技能性能
   - 识别优化机会
   - 执行优化操作
   - 评估优化效果

2. **钩子优化**
   - 评估钩子性能
   - 识别优化机会
   - 执行优化操作
   - 评估优化效果

3. **规则优化**
   - 评估规则适用性
   - 识别优化机会
   - 执行优化操作
   - 评估优化效果

---

## 故障排除

### 常见问题

**Q1: 技能无法正常工作？**

A: 检查以下几点：
1. 技能配置是否正确
2. 技能依赖是否安装
3. 技能权限是否足够
4. 技能日志是否有错误

**Q2: 钩子无法正常触发？**

A: 检查以下几点：
1. 钩子脚本是否有执行权限
2. 钩子配置是否正确
3. Git版本是否支持钩子
4. 钩子日志是否有错误

**Q3: 规则无法正常应用？**

A: 检查以下几点：
1. 规则配置是否正确
2. 规则格式是否正确
3. 规则权限是否足够
4. 规则日志是否有错误

---

## 更新历史

| 版本 | 日期 | 更新内容 | 更新人 |
|-----|------|---------|--------|
| V1.0 | 2026-03-13 | 初始版本创建 | AI助手 |

---

**文档版本：** V1.0
**最后更新：** 2026年3月13日
**维护人员：** AI助手
