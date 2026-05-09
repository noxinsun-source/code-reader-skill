"""
日志工具模块
基建代码：提供统一的日志记录功能
"""

import logging


def get_logger(name: str) -> logging.Logger:
    """基建代码：获取或创建日志记录器"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
