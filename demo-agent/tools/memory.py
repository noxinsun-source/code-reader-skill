"""
记忆管理模块
基建代码：负责维护 Agent 的执行历史和上下文信息
"""

from typing import Dict, List, Any
from collections import deque


class Memory:
    """
    Agent 记忆管理器
    功能：存储和管理执行历史、中间结果等
    """

    def __init__(self, max_history: int = 100):
        """初始化记忆库，最多保存 100 条历史记录"""
        self.history: deque = deque(maxlen=max_history)
        self.context: Dict[str, Any] = {}

    def add_record(self, action: str, result: Any) -> None:
        """基建代码：添加执行记录"""
        self.history.append({"action": action, "result": result})

    def get_context(self) -> Dict[str, Any]:
        """基建代码：获取当前上下文"""
        return self.context.copy()

    def update_context(self, key: str, value: Any) -> None:
        """基建代码：更新上下文信息"""
        self.context[key] = value
