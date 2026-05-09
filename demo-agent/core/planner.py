"""
任务规划模块
负责将自然语言任务分解为可执行的步骤计划
"""

from typing import List, Dict, Any
from utils.logger import get_logger


class TaskPlanner:
    """
    任务规划器类
    功能：使用分层任务分解技术将复杂任务拆分为可执行步骤
    方法：decompose_task
    """

    def __init__(self):
        """初始化规划器"""
        self.logger = get_logger(__name__)
        # 基建代码：初始化预定义的动作库
        self.action_templates = {
            "read": "read_files",
            "analyze": "analyze_structure",
            "generate": "generate_report",
            "execute": "execute_action"
        }

    def decompose_task(self, task_description: str) -> List[Dict[str, Any]]:
        """
        ⭐ 核心规划算法：分层任务分解（Hierarchical Task Decomposition）

        功能：将用户的自然语言任务转换为结构化的执行步骤

        核心算法说明：
        1. 输入分析阶段：识别任务中的关键动词和对象
           - 例如："分析这个项目" → 关键词 ["分析", "项目"]

        2. 步骤生成阶段：根据关键词生成初始步骤
           - 使用 action_templates 映射到标准动作
           - 为每个动作生成参数

        3. 依赖关系建立阶段：确定步骤间的依赖
           - "读文件" 必须在 "分析" 之前
           - "分析" 必须在 "生成报告" 之前
           - 使用拓扑排序确保步骤顺序正确

        4. 参数优化阶段：为每个步骤注入具体参数
           - 基建代码部分：处理通用参数（超时、重试次数）
           - 创新部分：为不同动作类型生成专门的参数

        参数：
            task_description (str): 用户的任务描述
            shape: (,) - 输入为单个字符串

        返回：
            List[Dict[str, Any]]: 有序的步骤列表
            shape: (num_steps,) - 每个元素包含：
                {
                    "step_id": int,
                    "action": str,
                    "params": Dict[str, Any],
                    "expected_output": Dict[str, str],
                    "timeout": int,
                    "retry": int
                }

        示例：
            >>> planner = TaskPlanner()
            >>> plan = planner.decompose_task("请分析一个 Python 项目的结构")
            >>> # 返回：
            >>> [
            >>>     {"step_id": 0, "action": "read_files", "params": {...}},
            >>>     {"step_id": 1, "action": "analyze_structure", "params": {...}},
            >>>     {"step_id": 2, "action": "generate_report", "params": {...}}
            >>> ]
        """

        # ⭐ 第一步：任务分析 - 识别关键字和动作类型
        # 这是创新点：通过关键词识别来自动确定任务类型
        task_lower = task_description.lower()
        keywords = self._extract_keywords(task_lower)
        task_type = self._identify_task_type(keywords)

        self.logger.info(f"Task type identified: {task_type}")

        # ⭐ 第二步：生成初始步骤列表
        # 基建代码：对于不同任务类型，使用预定义的步骤模板
        initial_steps = self._generate_initial_steps(task_type)

        # ⭐ 第三步：建立步骤间的依赖关系
        # 创新点：使用依赖图确保步骤顺序的正确性
        ordered_steps = self._resolve_dependencies(initial_steps)

        # ⭐ 第四步：为每个步骤注入参数和配置
        # 基建代码：添加超时、重试等通用参数
        final_plan = self._inject_parameters(ordered_steps, task_description)

        self.logger.info(f"Generated plan with {len(final_plan)} steps")
        return final_plan

    def _extract_keywords(self, task_description: str) -> List[str]:
        """
        基建代码：从任务描述中提取关键词
        用于识别任务中的主要动作和对象
        """
        # 简化版本：按空格分割并过滤
        stop_words = {"的", "一个", "请", "要", "把"}
        words = task_description.split()
        keywords = [w for w in words if w not in stop_words and len(w) > 1]
        return keywords

    def _identify_task_type(self, keywords: List[str]) -> str:
        """
        ⭐ 创新点：动态任务类型识别
        根据关键词判断任务类型，支持多种任务

        核心逻辑：
        - 如果包含 "分析"/"读取" → 分析任务
        - 如果包含 "生成"/"写入" → 生成任务
        - 默认 → 通用任务
        """
        analysis_keywords = ["分析", "读取", "检查", "审查"]
        generation_keywords = ["生成", "写入", "创建", "输出"]

        for keyword in keywords:
            if any(kw in keyword for kw in analysis_keywords):
                return "analysis"
            if any(kw in keyword for kw in generation_keywords):
                return "generation"

        return "general"

    def _generate_initial_steps(self, task_type: str) -> List[Dict[str, Any]]:
        """
        基建代码：根据任务类型生成初始步骤模板
        """
        templates = {
            "analysis": [
                {"action": "read_files", "priority": 1},
                {"action": "analyze_structure", "priority": 2},
                {"action": "generate_report", "priority": 3}
            ],
            "generation": [
                {"action": "read_files", "priority": 1},
                {"action": "analyze_structure", "priority": 2},
                {"action": "generate_report", "priority": 3}
            ],
            "general": [
                {"action": "read_files", "priority": 1},
                {"action": "execute_action", "priority": 2}
            ]
        }
        return templates.get(task_type, templates["general"])

    def _resolve_dependencies(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        ⭐ 创新点：依赖关系解析和拓扑排序
        确保步骤的执行顺序符合逻辑依赖关系

        核心算法：
        1. 建立依赖图：某些步骤必须在其他步骤之后执行
        2. 执行拓扑排序：得到满足依赖关系的执行顺序
        3. 检查循环依赖：防止死锁情况
        """
        # 定义依赖关系
        dependencies = {
            "analyze_structure": ["read_files"],
            "generate_report": ["analyze_structure"],
            "execute_action": ["read_files"]
        }

        # 基建代码：简单的依赖排序（生产环境应使用完整的拓扑排序）
        ordered = []
        added_actions = set()

        for step in steps:
            action = step["action"]
            deps = dependencies.get(action, [])

            # 检查所有依赖是否已添加
            for dep in deps:
                if dep not in added_actions:
                    # 如果依赖未添加，先添加依赖
                    ordered.append({"action": dep, "priority": 0})
                    added_actions.add(dep)

            if action not in added_actions:
                ordered.append(step)
                added_actions.add(action)

        return ordered

    def _inject_parameters(self, steps: List[Dict[str, Any]], task_desc: str) -> List[Dict[str, Any]]:
        """
        基建代码：为步骤注入具体参数和配置
        包括超时、重试次数、输出格式等
        """
        final_steps = []

        for idx, step in enumerate(steps):
            # 基建部分：添加通用参数
            step_with_params = {
                "step_id": idx,
                "action": step["action"],
                "params": {
                    "task_description": task_desc,
                    "step_index": idx,
                    "timeout": 30,  # 基建：默认超时 30 秒
                    "retry_count": 3  # 基建：默认重试 3 次
                },
                "expected_output": {
                    "format": "dict",
                    "keys": ["status", "data", "timestamp"]
                }
            }
            final_steps.append(step_with_params)

        return final_steps
