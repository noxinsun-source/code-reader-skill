# 📊 代码分析示例 - Demo Agent 项目

**项目名**: `demo-agent`  
**分析日期**: 2026-05-09  
**分析工具**: Code Reader Skill v1.0  
**输出语言**: 中文  

---

## 📋 项目概览

### 项目功能
一个简单的 Python Agent 框架，演示如何：
1. 将自然语言任务分解为可执行步骤
2. 按序执行步骤并管理状态
3. 处理错误并维护执行上下文

### 技术栈
- **核心**: Python 3.8+
- **模式**: Agent 设计模式（自主规划 + 动态执行）
- **架构**: 模块化设计（Core / Tools / Utils）

### 文件统计
- 总文件数: 9
- Python 源文件: 8
- 注释行数: 180+
- 代码行数: 250+

---

## 📁 文件结构树

```
demo-agent/
│
├── core/                    ⭐ 核心模块（Agent 和 Planner）
│   ├── __init__.py         - 模块导出
│   ├── agent.py            - 核心 Agent 类 ⭐⭐⭐ 创新代码
│   │   ├── __init__()
│   │   ├── plan_task()     ⭐ 分层任务分解
│   │   ├── execute_plan()  ⭐ 管道式执行 + 参数注入
│   │   ├── _execute_action()
│   │   ├── _handle_read_files()
│   │   ├── _handle_analyze()
│   │   ├── _handle_generate()
│   │   └── get_state()
│   │
│   └── planner.py          - 任务规划器 ⭐⭐⭐ 创新代码
│       ├── TaskPlanner.__init__()
│       ├── decompose_task()      ⭐ 多阶段规划算法
│       ├── _extract_keywords()   🔧 基建
│       ├── _identify_task_type() ⭐ 动态识别
│       ├── _generate_initial_steps() 🔧 基建
│       ├── _resolve_dependencies()  ⭐ 拓扑排序
│       └── _inject_parameters()    🔧 基建
│
├── tools/                   🔧 工具模块（基建代码）
│   ├── __init__.py
│   ├── memory.py           - 记忆管理器（基建）
│   │   ├── Memory.__init__()
│   │   ├── add_record()
│   │   ├── get_context()
│   │   └── update_context()
│   │
│   └── executor.py         - 执行器（基建）
│       └── Executor.execute()
│
├── utils/                   🔧 工具函数（基建代码）
│   ├── __init__.py
│   └── logger.py           - 日志工具
│       └── get_logger()
│
└── main.py                 🔧 主入口（基建）
    └── main() - 演示使用
```

---

## 🔗 函数调用关系图

```
┌─────────────────┐
│  main()         │
└────────┬────────┘
         │
         ▼
┌──────────────────────────┐
│ Agent.__init__()         │
│ - 初始化 TaskPlanner     │
│ - 初始化状态             │
│ - 初始化日志器           │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Agent.plan_task(task_description)    │⭐
│                                      │
│ 流程：                               │
│  1️⃣ 调用 TaskPlanner.decompose()   │
│  2️⃣ 更新状态 state['task_count']   │
│  3️⃣ 返回执行计划                   │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ TaskPlanner.decompose_task()         │⭐
│                                      │
│ 关键步骤：                           │
│  • _extract_keywords()               │
│  • _identify_task_type()       ⭐   │
│  • _generate_initial_steps()         │
│  • _resolve_dependencies()     ⭐   │
│  • _inject_parameters()              │
│                                      │
│ 返回: List[Dict] 执行计划           │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Agent.execute_plan(plan)             │⭐
│                                      │
│ 步骤循环：                           │
│  for step in plan:                   │
│    │                                 │
│    ├─ 参数注入: ⭐ 创新点            │
│    │  prev_output → params           │
│    │                                 │
│    ├─ _execute_action(action, params)│
│    │                                 │
│    └─ 异常处理（容错）               │
│                                      │
│ 返回: Dict 执行结果                  │
└──────────────────────────────────────┘
```

---

## 📊 数据流转图

```
┌──────────────────┐
│ 用户任务         │
│ (自然语言字符串) │
└────────┬─────────┘
         │ "分析 Python 项目"
         ▼
┌──────────────────────────┐
│ TaskPlanner.decompose()  │
│ (分层分解)               │
└────────┬─────────────────┘
         │
         ▼
    ⭐ 关键创新：
    多阶段分析
    [关键词提取 →
     任务识别 →
     步骤生成 →
     依赖解析 →
     参数注入]
    
         ▼
┌──────────────────────────┐
│ 执行计划                 │
│ List[Dict] with:         │
│  - action: str           │
│  - params: Dict          │
│  - timeout: int          │
│  - retry: int            │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Agent.execute_plan()     │
│ (管道式执行)             │
└────────┬─────────────────┘
         │
         ▼
    ⭐ 关键创新：
    参数注入机制
    [Step 1 Output] →
    [Step 2 Input] →
    [Step 2 Output] →
    [Step 3 Input]
    
         ▼
┌──────────────────────────┐
│ 最终结果                 │
│ Dict with:               │
│  - success: bool         │
│  - results: List         │
│  - final_output: Any     │
│  - errors: List          │
└──────────────────────────┘
```

---

## 🎯 核心函数详解

### 1️⃣ Agent.plan_task() - ⭐⭐⭐ 创新点

**位置**: `core/agent.py` (第 45-75 行)

**功能**: 将自然语言任务转化为可执行的步骤计划

**参数说明**:
- 输入: `task_description` (str) - 任务描述
  - shape: (,) - 单个字符串
  - 示例: "分析一个 Python 项目的结构"
  
- 输出: `List[Dict[str, Any]]` - 执行步骤列表
  - shape: (num_steps,) - 例如 3 个步骤
  - 结构: 每个元素包含 action, params, expected_output

**核心算法**:

```
输入: "分析 Python 项目结构"
  │
  ▼
1️⃣ 任务规划（分层分解）
   调用: TaskPlanner.decompose_task()
   
   内部流程：
   ├─ 关键词提取: ["分析", "Python", "项目", "结构"]
   ├─ 任务类型识别: 匹配 "分析" → type="analysis"
   ├─ 初始步骤生成: [read_files, analyze_structure, generate_report]
   ├─ 依赖关系解析: 确保正确的执行顺序（拓扑排序）
   └─ 参数优化: 添加 timeout, retry 等配置
  │
  ▼
2️⃣ 状态更新
   state['task_count'] += 1
  │
  ▼
3️⃣ 返回计划
   [
     {step_id: 0, action: "read_files", params: {...}},
     {step_id: 1, action: "analyze_structure", params: {...}},
     {step_id: 2, action: "generate_report", params: {...}}
   ]
```

**创新点说明**:
- **分层分解**: 不是直接执行，而是先规划，再执行
- **动态类型识别**: 根据关键词自动识别任务类型
- **依赖管理**: 确保步骤间的逻辑依赖关系

---

### 2️⃣ Agent.execute_plan() - ⭐⭐⭐ 创新点

**位置**: `core/agent.py` (第 77-150 行)

**功能**: 按照计划逐步执行任务，维护状态和上下文

**参数说明**:
- 输入: `plan` (List[Dict]) - 执行计划，来自 plan_task()
  - shape: (num_steps,) - 步骤数量可变
  - 每个步骤包含: action, params, timeout, retry
  
- 输出: `Dict[str, Any]` - 执行结果
  - 结构:
    ```python
    {
        "success": True/False,           # 整体是否成功
        "results": [...],                # 每步的执行结果
        "final_output": Any,             # 最后一步的输出
        "errors": [...]                  # 发生的错误列表
    }
    ```

**核心算法** ⭐ 管道式执行 + 参数注入:

```
计划输入: [Step1, Step2, Step3, ...]
  │
  ▼
┌─────────────────────────────────┐
│ 步骤循环执行 (for each step)     │
└─────────────────────────────────┘
  │
  ├─ Step 1 执行
  │  ├─ action = "read_files"
  │  ├─ params = {...}
  │  ├─ 执行: result1 = read_files(params)
  │  └─ 保存: results[0] = result1
  │
  ├─ Step 2 执行 ⭐ 关键创新
  │  ├─ action = "analyze_structure"
  │  ├─ params = {...}
  │  ├─ ⭐ 参数注入: params['input_data'] = result1
  │  │        (使用 Step 1 的输出作为 Step 2 的输入)
  │  ├─ 执行: result2 = analyze_structure(params)
  │  └─ 保存: results[1] = result2
  │
  └─ Step 3 执行
     ├─ action = "generate_report"
     ├─ params = {...}
     ├─ ⭐ 参数注入: params['input_data'] = result2
     ├─ 执行: result3 = generate_report(params)
     └─ 保存: results[2] = result3
  │
  ▼
┌─────────────────────────────────┐
│ 异常处理（容错机制）              │
│ - 单步失败不中断整体              │
│ - 错误记录但继续执行              │
└─────────────────────────────────┘
  │
  ▼
返回结果: {
    "success": len(errors) == 0,
    "results": [result1, result2, result3],
    "final_output": result3,
    "errors": []
}
```

**创新点说明** ⭐:

1. **参数注入机制** (第 120 行):
   ```python
   if idx > 0 and results:
       prev_output = results[-1].get("output")
       params["input_data"] = prev_output  # ⭐ 核心创新
   ```
   - 将前一步的输出自动注入到当前步骤
   - 实现了"数据流转"的自动化
   - 用户无需手动传递参数

2. **容错机制** (第 125-133 行):
   - 单个步骤失败不会中断整体流程
   - 记录错误但继续执行后续步骤
   - 适合处理部分步骤可选的场景

3. **状态管理** (第 138 行):
   - `state['completed_tasks'] += 1`
   - 维护全局执行统计

---

### 3️⃣ TaskPlanner.decompose_task() - ⭐⭐⭐ 创新点

**位置**: `core/planner.py` (第 30-120 行)

**功能**: 多阶段任务规划，将复杂任务拆分为可执行步骤

**核心算法** ⭐ 分层分解:

```
任务输入: "帮我分析一个 Python 项目"
  │
  ▼
┌─────────────────────────────────┐
│ 第一阶段：关键词提取              │
└─────────────────────────────────┘
  │
  ├─ 输入: "帮我分析一个 Python 项目"
  ├─ 处理: 分割字符串，去除停用词
  │       ["帮", "我", "分析", "一个", "Python", "项目"]
  │       ↓ (过滤停用词)
  │       ["分析", "Python", "项目"]
  └─ 输出: keywords = ["分析", "Python", "项目"]
  │
  ▼
┌─────────────────────────────────┐
│ 第二阶段：动态任务识别 ⭐          │
└─────────────────────────────────┘
  │
  ├─ 输入: keywords
  ├─ 逻辑: if "分析" in keywords → task_type = "analysis"
  │        (支持多种类型: analysis, generation, general)
  └─ 输出: task_type = "analysis"
  │
  ▼
┌─────────────────────────────────┐
│ 第三阶段：初始步骤生成             │
└─────────────────────────────────┘
  │
  ├─ 输入: task_type = "analysis"
  ├─ 查找: action_templates["analysis"]
  │       = [read_files, analyze_structure, generate_report]
  └─ 输出: initial_steps = [read_files, ...]
  │
  ▼
┌──────────────────────────────────┐
│ 第四阶段：依赖关系解析 ⭐          │
│ (拓扑排序 Topological Sort)       │
└──────────────────────────────────┘
  │
  ├─ 输入: initial_steps
  ├─ 依赖图:
  │   analyze_structure ← read_files
  │   generate_report ← analyze_structure
  │
  ├─ 拓扑排序算法:
  │   1. 找到没有依赖的步骤: read_files
  │   2. 添加 read_files，标记已处理
  │   3. 找到只依赖 read_files 的: analyze_structure
  │   4. 添加 analyze_structure，继续...
  │
  └─ 输出: ordered_steps = [read_files, analyze_structure, generate_report]
  │
  ▼
┌─────────────────────────────────┐
│ 第五阶段：参数优化                 │
└─────────────────────────────────┘
  │
  ├─ 输入: ordered_steps
  ├─ 为每个步骤添加:
  │   - step_id: 步骤编号
  │   - params: 基本参数
  │   - timeout: 30 秒 (基建代码)
  │   - retry_count: 3 (基建代码)
  │   - expected_output: 输出格式描述
  │
  └─ 输出: 完整的执行计划
  │
  ▼
返回: [
    {
        "step_id": 0,
        "action": "read_files",
        "params": {"task_description": "帮我分析...", ...},
        "timeout": 30,
        "retry": 3
    },
    {
        "step_id": 1,
        "action": "analyze_structure",
        ...
    },
    {
        "step_id": 2,
        "action": "generate_report",
        ...
    }
]
```

**创新点分析** ⭐:

1. **多阶段处理**:
   - 不是一步到位，而是逐阶段精化
   - 每个阶段清晰定义输入和输出
   - 便于扩展和调试

2. **动态任务识别** (第 2 阶段):
   - 自动识别任务类型，无需用户指定
   - 支持多种任务类型

3. **依赖关系管理** (第 4 阶段):
   - 使用拓扑排序确保步骤顺序
   - 防止循环依赖
   - 确保逻辑正确性

---

## 🔧 基建代码标注

### Memory 类 (tools/memory.py)
```python
class Memory:
    """🔧 基建代码：Agent 的记忆管理器"""
    
    def __init__(self, max_history: int = 100):
        """基建：初始化记忆缓冲区"""
        self.history: deque = deque(maxlen=max_history)
    
    def add_record(self, action: str, result: Any) -> None:
        """🔧 基建：添加执行记录"""
        self.history.append({"action": action, "result": result})
    
    def get_context(self) -> Dict[str, Any]:
        """🔧 基建：获取上下文"""
        return self.context.copy()
```

### 日志工具 (utils/logger.py)
```python
def get_logger(name: str) -> logging.Logger:
    """🔧 基建代码：获取日志记录器
    
    这是标准的日志初始化，每个项目都需要。
    不是这个项目的特有创新。
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        # ... 配置处理器 ...
    return logger
```

---

## 📈 创新点总结

### ⭐⭐⭐ 核心创新 (High Impact)

| 编号 | 创新点 | 位置 | 算法复杂度 | 价值 |
|-----|--------|------|---------|------|
| 1 | **分层任务分解** | `decompose_task()` | O(n log n) | 使复杂任务自动化 |
| 2 | **参数注入机制** | `execute_plan()` | O(n) | 实现数据流转自动化 |
| 3 | **动态任务识别** | `_identify_task_type()` | O(n) | 减少用户输入 |
| 4 | **依赖关系解析** | `_resolve_dependencies()` | O(n²) | 确保执行逻辑正确 |
| 5 | **容错执行机制** | `execute_plan()` | O(1) | 提高系统稳定性 |

### 🔧 基建代码 (Scaffolding)

- 日志记录器初始化
- 记忆缓冲区管理
- 通用参数注入（timeout, retry）
- 主函数和演示代码

---

## 📊 统计数据

```
项目统计：
├─ 总文件数: 9 files
├─ Python 源代码: 8 files
├─ 代码行数: ~250 lines
├─ 注释行数: ~180 lines
├─ 注释比例: 42%
│
├─ 创新代码:
│  ├─ 核心函数: 5 个
│  ├─ 行数: ~150 lines
│  └─ 复杂度: 高 (涉及多层算法)
│
└─ 基建代码:
   ├─ 工具函数: 6 个
   ├─ 行数: ~100 lines
   └─ 复杂度: 低 (标准 API 调用)
```

---

## 🎓 学习路径

1. **入门** (15 分钟)
   - 读 `main.py` 了解使用流程
   - 读 `Agent.__init__()` 了解初始化

2. **进阶** (30 分钟)
   - 读 `plan_task()` 了解任务规划
   - 读 `decompose_task()` 了解算法

3. **精通** (1 小时)
   - 理解参数注入机制
   - 理解依赖关系解析
   - 尝试扩展 action_templates

---

**生成时间**: 2026-05-09 16:30:00  
**生成器**: Code Reader Skill v1.0  
**格式**: Markdown  
**语言**: 中文
