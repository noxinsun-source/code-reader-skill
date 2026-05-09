"""
主入口文件
基建代码：演示如何使用 Agent 完成任务
"""

from core.agent import Agent
from utils.logger import get_logger


def main():
    """主函数：演示 Agent 的使用流程"""
    logger = get_logger(__name__)

    # 初始化 Agent
    agent = Agent(name="CodeAnalyzerAgent")
    logger.info("Agent initialized")

    # 定义任务
    task = "分析一个 Python 项目的代码结构，生成详细的分析报告"

    # 制定计划
    plan = agent.plan_task(task)
    logger.info(f"Generated {len(plan)} steps")

    # 执行计划
    result = agent.execute_plan(plan)
    logger.info(f"Execution completed. Success: {result['success']}")

    # 输出结果
    print("\n=== Execution Result ===")
    print(f"Success: {result['success']}")
    print(f"Steps executed: {len(result['results'])}")
    print(f"Errors: {len(result['errors'])}")


if __name__ == "__main__":
    main()
