import aiohttp
import asyncio
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
import uuid

from ..config import TEMP_DIR, ALLOWED_IMAGE_TYPES, ALLOWED_VIDEO_TYPES

async def download_file(url: str) -> Optional[Path]:
    """
    异步下载文件并返回临时文件路径
    """
    try:
        # 解析URL和文件扩展名
        parsed_url = urlparse(url)
        ext = Path(parsed_url.path).suffix.lower()

        # 验证文件类型
        if ext not in ALLOWED_IMAGE_TYPES + ALLOWED_VIDEO_TYPES:
            raise ValueError(f"Unsupported file type: {ext}")

        # 生成唯一的临时文件名
        temp_file = TEMP_DIR / f"{uuid.uuid4()}{ext}"

        # 异步下载文件
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to download file: {response.status}")

                # 分块写入文件
                with open(temp_file, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)

        return temp_file

    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return None

def is_image(file_path: Path) -> bool:
    """检查文件是否为图片"""
    return file_path.suffix.lower() in ALLOWED_IMAGE_TYPES

def is_video(file_path: Path) -> bool:
    """检查文件是否为视频"""
    return file_path.suffix.lower() in ALLOWED_VIDEO_TYPES
