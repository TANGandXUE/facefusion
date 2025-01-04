import signal
import sys
from typing import Optional
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import API_HOST, API_PORT
from .routes import face_swap

app = FastAPI(
    title="FaceFusion API",
    description="API service for face swapping using FaceFusion",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(face_swap.router, prefix="/api", tags=["face-swap"])

def signal_handler(signum, frame):
    """处理退出信号"""
    print("\nShutting down API server...")
    sys.exit(0)

def start(host: Optional[str] = None, port: Optional[int] = None):
    """启动API服务器"""
    # 设置信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # 优先使用传入的参数，其次使用环境变量，最后使用默认值
    server_host = host or os.environ.get('API_HOST') or API_HOST
    server_port = port or int(os.environ.get('API_PORT', '0')) or API_PORT

    # 启动服务器
    uvicorn.run(
        app,
        host=server_host,
        port=server_port,
        log_level="info"
    )

if __name__ == "__main__":
    start()
