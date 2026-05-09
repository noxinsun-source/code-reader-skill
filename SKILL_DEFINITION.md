# 🔍 Code Reader Skill - 代码解读与智能注释系统

**版本**: 1.0  
**语言**: 支持中英文切换  
**核心定位**: 代码理解与解读，直接在源代码基础上添加详细中文注释

---

## 📋 Skill 概述

这是一个可复用的代码分析 Skill，用于：
1. **整体结构分析** - 展示文件树、模块关系、功能概览
2. **函数关系映射** - 生成调用关系图、数据流转图表
3. **代码注释生成** - 逐行添加中文注释，标注创新点和基建代码
4. **算法详解** - 详细解释核心算法和实现逻辑

---

## 🎯 使用方式

### 在 Claude Code 中调用

```bash
# 分析一个本地 Python 项目
/code-reader /path/to/your/python/project

# 指定输出语言为英文
/code-reader /path/to/your/project --language=en

# 指定输出文件名
/code-reader /path/to/your/project --output=my_analysis.md
```

### 例子

```
/code-reader ~/projects/my-agent --language=zh
```

---

## 📤 输出格式

### 输出内容包括：

```markdown
# 📊 代码分析报告: [项目名]

## 1. 项目概览
- 项目功能描述
- 技术栈
- 主要目录结构

## 2. 文件结构树
```
project/
├── module1/
│   ├── file1.py       # 功能说明
│   └── file2.py
└── module2/
```

## 3. 函数与类清单
- Agent (core/agent.py)
  - __init__()
  - plan_task()  ⭐ 创新点
  - execute_plan()  ⭐ 创新点
  - ...

## 4. 整体流程图
```
┌─────────────┐
│  用户输入   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ 任务规划 (Planner)   │
│ - 关键词提取         │
│ - 任务类型识别 ⭐    │
│ - 依赖关系解析 ⭐    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ 计划执行 (Agent)    │
│ - 步骤循环执行       │
│ - 参数注入机制 ⭐   │
│ - 结果整合           │
└──────┬──────────────┘
       │
       ▼
┌─────────────┐
│ 最终输出     │
└─────────────┘
```

## 5. 核心模块详解

### 5.1 Agent 类 (core/agent.py)
**功能**: 协调任务规划和执行

**关键方法**:
1. `__init__()` - 初始化
   - 创建 TaskPlanner 实例
   - 初始化状态字典

2. `plan_task()` ⭐ **创新点**
   - 核心算法: 分层任务分解
   - 输入: 任务描述 (str)
   - 输出: 执行步骤列表 (List[Dict])
   - **实现逻辑**: 将自然语言任务转化为结构化步骤

3. `execute_plan()` ⭐ **创新点**
   - 核心算法: 管道式步骤执行 + 参数注入
   - **关键创新**: 前一步输出 → 后一步输入
   - 容错机制: 单步失败不中断整体流程
   - 状态管理: 维护执行上下文

4. `_execute_action()` 基建代码
   - 动作分发和路由

### 5.2 TaskPlanner 类 (core/planner.py)
**功能**: 任务规划和分解

**核心算法** ⭐ `decompose_task()`:
```
输入: "请分析 Python 项目"
  ↓
1️⃣ 关键词提取
   ["分析", "Python", "项目"]
  ↓
2️⃣ 任务类型识别 ⭐
   匹配到 "分析" → task_type = "analysis"
  ↓
3️⃣ 生成初始步骤
   [read_files → analyze_structure → generate_report]
  ↓
4️⃣ 依赖关系解析 ⭐
   确保 read_files 在 analyze_structure 之前
   (使用拓扑排序)
  ↓
5️⃣ 参数注入
   为每个步骤添加 timeout、retry 等参数
  ↓
输出: 完整的执行计划 (List[Dict])
```

**创新点说明**:
- **动态任务识别**: 根据关键词自动识别任务类型
- **依赖关系解析**: 确保步骤执行顺序的逻辑正确性
- **参数优化**: 根据任务类型生成专门的参数

**基建代码**:
- 关键词提取: 通用的字符串处理
- 参数注入: 添加超时、重试等通用配置

---

## 🔬 创新点 vs 基建代码

### ⭐ 创新点（项目特有）
- `Agent.plan_task()` - 分层任务分解算法
- `Agent.execute_plan()` - 管道式执行 + 参数注入机制
- `TaskPlanner.decompose_task()` - 多阶段的任务规划流程
- `TaskPlanner._identify_task_type()` - 动态任务识别
- `TaskPlanner._resolve_dependencies()` - 依赖关系解析和拓扑排序

### 🔧 基建代码（通用代码）
- `get_logger()` - 日志记录器初始化
- `Memory.add_record()` - 历史记录存储
- `Executor.execute()` - 通用执行器
- 文件I/O、初始化、配置管理等机械代码

---

## 📝 代码示例（带注释）

### Agent 关键方法示例

```python
def execute_plan(self, plan: List[Dict[str, Any]]) -> Dict[str, Any]:
    """⭐ 核心创新：管道式执行 + 参数注入"""
    results = []
    errors = []
    final_output = None

    # 🔄 步骤循环执行 - 核心循环
    for idx, step in enumerate(plan):
        try:
            action = step.get("action")
            params = step.get("params", {})

            # ⭐ 关键创新点：参数注入机制
            # 将前一步的输出注入到当前步骤
            if idx > 0 and results:
                prev_output = results[-1].get("output")
                params["input_data"] = prev_output  # 🔗 数据流转

            # 执行当前步骤
            step_result = self._execute_action(action, params)
            results.append({...})
            final_output = step_result

        except Exception as e:
            # 🛡️ 容错机制：单步失败不中断
            errors.append(...)

    return {...}
```

---

## 🚀 集成到 Claude Code

### 方式 1: 作为 Skill 集成

1. 将此文件放入 `.claude/skills/` 目录
2. 或添加到 `CLAUDE.md` 的 Skill 定义中
3. 调用方式: `/code-reader [path]`

### 方式 2: 作为 Agent 使用

```python
from agent import CodeReaderAgent

agent = CodeReaderAgent()
report = agent.analyze("/path/to/project")
agent.save_report(report, "analysis.md")
```

---

## 📊 Skill 的三段式分析法

1. **第一段：整体结构**
   - 展示项目文件树
   - 列出所有模块和函数
   - 标注文件功能

2. **第二段：关系映射**
   - 函数调用关系图
   - 数据流转流程
   - 依赖关系

3. **第三段：代码注释**
   - 原始代码 + 中文注释
   - 标注 ⭐ 创新点
   - 标注 🔧 基建代码
   - 详解核心算法

---

## 📌 注释约定

```python
# 基建代码：通用代码（每个项目都有）
def _extract_keywords(self, text: str) -> List[str]:
    """提取关键词 - 基建代码"""
    return text.split()

# ⭐ 创新点：项目特有的算法
def _identify_task_type(self, keywords: List[str]) -> str:
    """⭐ 创新点：动态任务类型识别
    
    核心算法说明：
    - 遍历关键词，匹配任务类型
    - 支持多种任务（分析、生成、通用）
    - 返回识别出的任务类型
    """
    pass
```

---

## 🎓 使用场景

### 场景 1: 学习新代码库
```bash
/code-reader ~/projects/new-framework
# 快速理解项目结构、关键函数、核心算法
```

### 场景 2: 知识传承
```bash
/code-reader ~/projects/team-project
# 生成详细文档，便于团队成员理解
```

### 场景 3: 代码审查
```bash
/code-reader ~/projects/pr-code
# 分析新代码的创新点和实现方式
```

### 场景 4: 项目文档
```bash
/code-reader ~/projects/my-product
# 自动生成产品文档的技术部分
```

---

## ✨ 特点总结

| 特点 | 说明 |
|------|------|
| **零配置** | 指定路径即可，自动识别项目结构 |
| **智能注释** | 自动添加中文注释，标注关键部分 |
| **创新识别** | 自动区分创新代码和基建代码 |
| **可视化** | 生成框线图和流程图 |
| **语言支持** | 支持中英文切换 |
| **一个输出** | 生成单个 Markdown 文件，易于分享 |

---

## 📞 FAQ

**Q: 如何指定输出语言?**
A: 使用 `--language` 参数: `/code-reader /path --language=en`

**Q: 是否支持其他编程语言?**
A: 当前优化于 Python，其他语言仍可分析但效果可能不同

**Q: 输出文件在哪里?**
A: 默认保存到项目根目录，或使用 `--output` 指定路径

---

**创建日期**: 2026-05-09  
**最后更新**: 2026-05-09  
**维护者**: Claude Code
