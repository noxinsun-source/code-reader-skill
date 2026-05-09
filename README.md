# 🔍 Code Reader Skill - 代码解读与智能注释系统

**Language**: [中文](#cn) | [English](#en)

---

<a name="cn"></a>

## 中文版本

### 📌 快速概览

**Code Reader Skill** 是一个可复用的代码分析工具，用来：
- 📊 自动生成代码结构分析报告
- 🔗 绘制函数调用关系图
- 💬 逐行生成中文注释代码
- ⭐ 自动识别和标注创新点
- 🔧 标注基建代码（通用代码）

### 🎯 核心功能

#### 1. **整体结构分析**
- 展示项目文件树
- 列出所有模块和函数
- 标注每个文件的功能
- 统计代码行数和注释比例

#### 2. **函数关系映射**
- 函数调用关系图（ASCII 框线图）
- 数据流转流程图
- 依赖关系可视化
- 参数传递路径

#### 3. **代码注释生成**
- 原始代码 + 详细中文注释
- ⭐ 标注创新点（项目特有的算法）
- 🔧 标注基建代码（通用代码）
- 详解核心算法的实现逻辑

#### 4. **算法详解**
- 逐步分解核心算法
- 说明底层实现方式
- 展示参数和返回值
- 提供代码示例

### 🚀 快速开始

#### 安装

1. **克隆仓库**:
```bash
git clone https://github.com/your-username/code-reader-skill.git
cd code-reader-skill
```

2. **在 Claude Code 中使用**:
- 将 `SKILL_DEFINITION.md` 内容添加到 `~/.claude/CLAUDE.md`
- 或存放到 `~/.claude/skills/` 目录

#### 使用方式

```bash
# 分析一个 Python 项目（中文输出）
/code-reader /path/to/your/project

# 指定语言为英文
/code-reader /path/to/your/project --language=en

# 指定输出文件名
/code-reader /path/to/your/project --output=my_analysis.md

# 分析演示项目
/code-reader ./demo-agent
```

### 📂 项目结构

```
code-reader-skill/
├── README.md                    # 此文件
├── SKILL_DEFINITION.md          # Skill 完整定义
│
├── demo-agent/                  # 演示项目（测试案例）
│   ├── core/
│   │   ├── agent.py            # 核心 Agent 类 ⭐⭐⭐
│   │   └── planner.py          # 任务规划器 ⭐⭐⭐
│   ├── tools/
│   │   ├── memory.py           # 记忆管理（基建）
│   │   └── executor.py         # 执行器（基建）
│   ├── utils/
│   │   └── logger.py           # 日志工具（基建）
│   └── main.py                 # 主入口（基建）
│
└── examples/
    └── ANALYSIS_DEMO.md        # 演示项目的完整分析结果
```

### 📊 输出示例

#### 文件结构

```
demo-agent/
├── core/                    ⭐ 核心模块
│   ├── agent.py            ⭐⭐⭐ 创新代码
│   └── planner.py          ⭐⭐⭐ 创新代码
├── tools/                   🔧 基建代码
│   ├── memory.py
│   └── executor.py
├── utils/                   🔧 基建代码
│   └── logger.py
└── main.py                 🔧 主入口
```

#### 函数调用关系

```
┌──────────┐
│ main()   │
└────┬─────┘
     │
     ▼
┌────────────────────┐
│ Agent.plan_task()  │⭐ 创新点：分层分解
└────┬───────────────┘
     │
     ▼
┌──────────────────────────┐
│ TaskPlanner.decompose()  │⭐ 创新点：多阶段规划
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│ Agent.execute_plan()     │⭐ 创新点：参数注入
└────┬─────────────────────┘
     │
     ▼
  [输出结果]
```

#### 代码注释示例

```python
def execute_plan(self, plan: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    ⭐ 核心创新：管道式执行 + 参数注入
    
    功能：按照规划逐步执行任务
    
    核心算法说明：
    1. 步骤循环执行：遍历计划中的每个步骤
    2. 参数注入：⭐ 将前一步输出作为下一步输入
    3. 容错机制：单步失败不中断整体执行
    
    参数：
        plan: 执行计划 (List[Dict])
    
    返回：
        Dict 包含 success, results, final_output, errors
    """
    results = []
    for idx, step in enumerate(plan):
        # ⭐ 关键创新：参数注入机制
        if idx > 0 and results:
            prev_output = results[-1].get("output")
            params["input_data"] = prev_output  # 数据流转
```

### ⭐ 创新点 vs 🔧 基建代码

#### ⭐ 创新点（项目特有）
- **分层任务分解** (`decompose_task()`)
  - 多阶段处理：关键词提取 → 类型识别 → 步骤生成 → 依赖解析 → 参数优化
  - 复杂度：O(n log n)
  - 价值：使复杂任务规划自动化

- **参数注入机制** (`execute_plan()`)
  - 前一步输出自动注入到后一步输入
  - 实现数据流转的自动化
  - 减少用户手动参数传递

- **动态任务识别** (`_identify_task_type()`)
  - 根据关键词自动识别任务类型
  - 支持多种任务：分析、生成、通用

- **依赖关系解析** (`_resolve_dependencies()`)
  - 使用拓扑排序确保步骤顺序
  - 防止循环依赖
  - 确保执行逻辑正确性

#### 🔧 基建代码（通用代码）
- 日志记录器初始化 (`get_logger()`)
- 记忆缓冲区管理 (`Memory` 类)
- 执行器基础实现 (`Executor` 类)
- 通用参数注入（timeout, retry）
- 主函数和演示代码

### 📖 使用指南

#### 场景 1：学习新代码库
```bash
/code-reader ~/projects/new-framework
```
快速理解项目结构、关键函数、核心算法。

#### 场景 2：知识传承
```bash
/code-reader ~/projects/team-project
```
生成详细文档，便于团队成员理解。

#### 场景 3：代码审查
```bash
/code-reader ~/projects/pr-code
```
分析新代码的创新点和实现方式。

#### 场景 4：自动文档
```bash
/code-reader ~/projects/my-product
```
自动生成产品的技术文档部分。

### 🎓 Skill 的三段式分析法

#### 第一段：整体结构
- 项目功能描述
- 文件树结构
- 模块和函数清单

#### 第二段：关系映射
- 函数调用关系（ASCII 图表）
- 数据流转流程
- 依赖关系图

#### 第三段：代码注释
- 原始代码 + 中文注释
- ⭐ 创新点标注和详解
- 🔧 基建代码标注
- 核心算法逐步分解

### 💡 注释约定

```python
# 🔧 基建代码：标准做法，通用代码
def standard_function():
    """每个项目都有的机械性代码"""
    pass

# ⭐ 创新点：项目特有的算法
def innovative_function():
    """⭐ 创新点说明
    
    核心算法：
    - 步骤 1：...
    - 步骤 2：...
    - 结果：...
    """
    pass
```

### 🔧 配置选项

编辑 `SKILL_DEFINITION.md` 中的参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--language` | `zh` | 输出语言（zh/en） |
| `--output` | `analysis.md` | 输出文件名 |
| `--depth` | `5` | 分析深度（1-10） |
| `--include-test` | `false` | 是否包含测试文件 |

### 📊 支持的编程语言

- ✅ **Python** (最优化)
- ✅ **JavaScript/TypeScript**
- ✅ **Java**
- ✅ **C++**
- ✅ **Go**
- ✅ 其他（效果可能不同）

### 🤝 贡献指南

欢迎贡献！包括：
- 改进 Skill 的 Prompt
- 添加新的编程语言支持
- 优化分析算法
- 改进输出格式
- 添加更多示例

### 📝 常见问题

**Q: 如何指定输出语言？**
```bash
/code-reader /path/to/project --language=en
```

**Q: 分析很大的项目会很慢吗？**
使用 `--depth` 参数限制分析深度：
```bash
/code-reader /path/to/project --depth=3
```

**Q: 能否排除某些文件？**
编辑 `SKILL_DEFINITION.md` 中的文件过滤规则。

**Q: 输出文件在哪里？**
默认保存到当前目录，或使用 `--output` 指定。

### 📞 支持

- 📖 查看 `SKILL_DEFINITION.md` 获取完整文档
- 📊 参考 `examples/ANALYSIS_DEMO.md` 了解输出示例
- 🐍 测试 `demo-agent/` 项目

### 📄 许可证

MIT License - 自由使用和修改

### 👨‍💻 作者

Claude Code - AI Assistant  
创建时间: 2026-05-09

---

<a name="en"></a>

## English Version

### 📌 Quick Overview

**Code Reader Skill** is a reusable code analysis tool for:
- 📊 Automatically generating code structure analysis reports
- 🔗 Drawing function call relationship diagrams
- 💬 Generating line-by-line Chinese annotations
- ⭐ Auto-identifying and marking innovative code
- 🔧 Marking infrastructure code (common/boilerplate code)

### 🎯 Core Features

#### 1. **Structure Analysis**
- Project file tree display
- List all modules and functions
- Mark functionality of each file
- Statistics on code and comment lines

#### 2. **Function Relationship Mapping**
- Function call graphs (ASCII box diagrams)
- Data flow diagrams
- Dependency visualization
- Parameter passing paths

#### 3. **Code Annotation Generation**
- Original code + detailed Chinese comments
- ⭐ Mark innovative points (algorithm-specific)
- 🔧 Mark infrastructure code (generic code)
- Explain core algorithm implementation logic

#### 4. **Algorithm Explanation**
- Step-by-step algorithm decomposition
- Explain underlying implementation
- Show parameters and return values
- Provide code examples

### 🚀 Quick Start

#### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/your-username/code-reader-skill.git
cd code-reader-skill
```

2. **Use in Claude Code**:
- Add content from `SKILL_DEFINITION.md` to `~/.claude/CLAUDE.md`
- Or place in `~/.claude/skills/` directory

#### Usage

```bash
# Analyze a Python project (English output)
/code-reader /path/to/your/project --language=en

# Analyze with custom output filename
/code-reader /path/to/your/project --output=analysis.md --language=en

# Analyze the demo project
/code-reader ./demo-agent --language=en
```

### 📂 Project Structure

```
code-reader-skill/
├── README.md                    # This file
├── SKILL_DEFINITION.md          # Complete Skill definition
│
├── demo-agent/                  # Demo project (test case)
│   ├── core/
│   │   ├── agent.py            # Core Agent class ⭐⭐⭐
│   │   └── planner.py          # Task Planner ⭐⭐⭐
│   ├── tools/
│   │   ├── memory.py           # Memory management 🔧
│   │   └── executor.py         # Executor 🔧
│   ├── utils/
│   │   └── logger.py           # Logger utility 🔧
│   └── main.py                 # Main entry 🔧
│
└── examples/
    └── ANALYSIS_DEMO.md        # Complete analysis of demo project
```

### 📊 Output Example

See `examples/ANALYSIS_DEMO.md` for detailed analysis output.

### ⭐ Innovative Code vs 🔧 Infrastructure Code

#### ⭐ Innovative Points
- **Hierarchical Task Decomposition** - Multi-stage processing pipeline
- **Parameter Injection Mechanism** - Automatic data flow between steps
- **Dynamic Task Identification** - Auto-detect task types
- **Dependency Resolution** - Topological sort for correct execution order

#### 🔧 Infrastructure Code
- Logger initialization
- Memory buffer management
- Executor implementation
- Main function and demos

### 📖 Usage Guide

#### Scenario 1: Learn New Codebase
Quickly understand project structure, key functions, core algorithms.

#### Scenario 2: Knowledge Transfer
Generate detailed documentation for team members.

#### Scenario 3: Code Review
Analyze innovative points and implementation methods.

#### Scenario 4: Auto Documentation
Generate technical documentation automatically.

### 🔧 Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--language` | `zh` | Output language (zh/en) |
| `--output` | `analysis.md` | Output filename |
| `--depth` | `5` | Analysis depth (1-10) |
| `--include-test` | `false` | Include test files |

### 📊 Supported Languages

- ✅ **Python** (optimized)
- ✅ **JavaScript/TypeScript**
- ✅ **Java**
- ✅ **C++**
- ✅ **Go**
- ✅ Others (varying results)

### 🤝 Contributing

Contributions welcome! Including:
- Improve Skill prompts
- Add language support
- Optimize analysis algorithms
- Improve output format
- Add more examples

### 📝 FAQ

**Q: How to specify output language?**
```bash
/code-reader /path/to/project --language=en
```

**Q: Will analyzing large projects be slow?**
Use `--depth` parameter to limit analysis depth.

**Q: Can I exclude certain files?**
Edit file filtering rules in `SKILL_DEFINITION.md`.

**Q: Where is the output file saved?**
Default to current directory, or specify with `--output`.

### 📞 Support

- 📖 See `SKILL_DEFINITION.md` for complete documentation
- 📊 Refer to `examples/ANALYSIS_DEMO.md` for output examples
- 🐍 Test with `demo-agent/` project

### 📄 License

MIT License - Free to use and modify

### 👨‍💻 Author

Claude Code - AI Assistant  
Created: 2026-05-09

---

## 🎯 Next Steps

1. **Review** the `SKILL_DEFINITION.md` for complete documentation
2. **Explore** the `demo-agent/` for example code structure
3. **Check** `examples/ANALYSIS_DEMO.md` for analysis output format
4. **Try** analyzing your own projects!

**Last Updated**: 2026-05-09  
**Version**: 1.0.0
