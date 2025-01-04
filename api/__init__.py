"""
FaceFusion API Service
提供人脸替换的 REST API 服务
"""

__version__ = "1.0.0"
__author__ = "FaceFusion Team"

# 导出主要的接口
from .main import app, start
from .config import API_HOST, API_PORT

__all__ = ['app', 'start', 'API_HOST', 'API_PORT']

# 包初始化
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
