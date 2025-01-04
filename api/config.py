from pathlib import Path

# API 服务配置
API_HOST = "0.0.0.0"
API_PORT = 8000

# 文件存储路径配置
TEMP_DIR = Path("temp")
OUTPUT_DIR = Path("output")

# FaceFusion 处理参数
FACE_SWAPPER_MODEL = "inswapper_128_fp16"
EXECUTION_PROVIDERS = ["cuda"]
EXECUTION_THREAD_COUNT = 4

# 文件处理配置
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
ALLOWED_IMAGE_TYPES = [".jpg", ".jpeg", ".png"]
ALLOWED_VIDEO_TYPES = [".mp4", ".avi", ".mov"]

# 创建必要的目录
TEMP_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
