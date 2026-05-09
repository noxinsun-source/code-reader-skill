"""
核心 Agent 类模块
定义了整个 Agent 系统的主类，负责协调规划、工具调用和任务执行
"""

from typing import Dict, List, Any, Optional
from .planner import TaskPlanner
from utils.logger import get_logger


class Agent:
    """
    核心 Agent 类
    功能：初始化智能体、维护状态、执行任务流程
    属性：
        - name: Agent 名称
        - planner: 任务规划器实例
        - state: 当前状态字典
        - logger: 日志记录器
    """

    def __init__(self, name: str = "DefaultAgent", **kwargs):
        """
        初始化 Agent 实例
        参数：
            name (str): Agent 名称，默认为 "DefaultAgent"
            **kwargs: 其他配置参数
        """
        self.name = name
        self.planner = TaskPlanner()
        self.state: Dict[str, Any] = {
            "initialized": True,
            "task_count": 0,
            "completed_tasks": 0
        }
        self.logger = get_logger(__name__)
        self.logger.info(f"Agent '{name}' initialized successfully")

    def plan_task(self, task_description: str) -> List[Dict[str, Any]]:
        """
        ⭐ 核心规划函数
        功能：根据任务描述生成执行计划

        核心算法说明：
        1. 将用户的自然语言任务输入给规划器
        2. 规划器使用分层分解 (Hierarchical Task Decomposition) 技术
        3. 将大任务拆分为多个小步骤，每步都可执行
        4. 返回一个有序的步骤列表，包含动作、参数和预期输出

        参数：
            task_description (str): 任务的自然语言描述
            shape: (batch_size,) - 输入为单个字符串

        返回：
            List[Dict]: 执行步骤列表
            shape: (num_steps, step_dict) - 每个 step_dict 包含
                - "action": 要执行的动作名称
                - "params": 动作的参数字典
                - "expected_output": 预期的输出格式

        示例：
            >>> agent = Agent("MyAgent")
            >>> plan = agent.plan_task("帮我分析一个 Python 项目")
            >>> # 返回：
            >>> # [
            >>> #     {"action": "read_files", "params": {...}},
            >>> #     {"action": "analyze_structure", "params": {...}},
            >>> #     {"action": "generate_report", "params": {...}}
            >>> # ]
        """
        # ⭐ 关键算法：将任务交给规划器进行分层分解
        plan_steps = self.planner.decompose_task(task_description)

        # 更新状态：记录任务数量
        self.state["task_count"] += 1

        self.logger.info(f"Generated plan with {len(plan_steps)} steps")
        return plan_steps

    def execute_plan(self, plan: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        执行任务计划的主函数
        功能：按照规划步骤逐一执行任务

        核心算法说明：
        1. 遍历计划中的每个步骤
        2. 根据 "action" 字段调用对应的执行器
        3. 收集每一步的执行结果
        4. 将前一步的输出作为下一步的输入（管道传递）
        5. 如果某个步骤失败，记录错误但继续执行（容错机制）

        参数：
            plan (List[Dict]): 任务计划，来自 plan_task()
            shape: (num_steps, step_dict)

        返回：
            Dict: 最终执行结果
            结构：{
                "success": bool,
                "results": List[Dict],  # 每步的执行结果
                "final_output": Any,    # 最终输出
                "errors": List[str]     # 执行过程中遇到的错误
            }
        """
        results = []
        errors = []
        final_output = None

        # ⭐ 核心执行循环：管道式的步骤执行
        # 这是 Agent 的关键：不是一次性执行所有步骤，
        # 而是根据前一步的结果动态调整下一步的执行
        for idx, step in enumerate(plan):
            try:
                # 提取步骤信息
                action = step.get("action")
                params = step.get("params", {})

                # ⭐ 关键创新点：参数注入机制
                # 将前一步的输出注入到当前步骤的参数中
                if idx > 0 and results:
                    prev_output = results[-1].get("output")
                    params["input_data"] = prev_output

                # 执行当前步骤
                step_result = self._execute_action(action, params)
                results.append({
                    "step": idx,
                    "action": action,
                    "status": "success",
                    "output": step_result
                })
                final_output = step_result

            except Exception as e:
                # 容错机制：记录错误但继续执行
                error_msg = f"Step {idx} ({action}) failed: {str(e)}"
                errors.append(error_msg)
                self.logger.error(error_msg)
                results.append({
                    "step": idx,
                    "action": action,
                    "status": "failed",
                    "error": str(e)
                })

        # 更新状态
        success = len(errors) == 0
        self.state["completed_tasks"] += 1

        return {
            "success": success,
            "results": results,
            "final_output": final_output,
            "errors": errors
        }

    def _execute_action(self, action: str, params: Dict[str, Any]) -> Any:
        """
        执行单个动作的内部函数
        功能：根据动作类型调用相应的处理器

        参数：
            action (str): 动作名称，例如 "read_files", "analyze_structure"
            params (Dict): 动作的参数字典

        返回：
            Any: 动作执行的结果
        """
        # ⭐ 动作分发机制：根据 action 字段路由到不同的处理器
        action_map = {
            "read_files": self._handle_read_files,
            "analyze_structure": self._handle_analyze,
            "generate_report": self._handle_generate,
        }

        handler = action_map.get(action)
        if not handler:
            raise ValueError(f"Unknown action: {action}")

        return handler(params)

    def _handle_read_files(self, params: Dict[str, Any]) -> Dict[str, str]:
        """文件读取处理器"""
        # 模拟文件读取
        return {"status": "read_complete", "files_count": params.get("count", 0)}

    def _handle_analyze(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """分析处理器"""
        # 模拟分析逻辑
        return {"status": "analysis_complete", "insights": ["insight1", "insight2"]}

    def _handle_generate(self, params: Dict[str, Any]) -> str:
        """报告生成处理器"""
        # 模拟报告生成
        return "Analysis report generated successfully"

    def get_state(self) -> Dict[str, Any]:
        """
        获取 Agent 当前状态

        返回：
            Dict: 包含初始化状态、任务计数、完成计数等信息
        """
        return self.state.copy()

    def reset(self) -> None:
        """重置 Agent 状态为初始化状态"""
        self.state = {
            "initialized": True,
            "task_count": 0,
            "completed_tasks": 0
        }
        self.logger.info(f"Agent '{self.name}' reset successfully")
