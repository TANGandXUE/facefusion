from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from pathlib import Path
import os

from ..utils.download import download_file, is_image, is_video
from ..utils.process import process_face_swap

router = APIRouter()

class FaceSwapRequest(BaseModel):
    source_url: HttpUrl
    target_url: HttpUrl

class FaceSwapResponse(BaseModel):
    success: bool
    message: str
    output_path: str = None

@router.post("/face-swap", response_model=FaceSwapResponse)
async def face_swap(request: FaceSwapRequest):
    try:
        # 下载源文件和目标文件
        source_path = await download_file(str(request.source_url))
        print("source_path: ", source_path)
        if not source_path or not is_image(source_path):
            raise HTTPException(status_code=400, detail="Invalid source file")

        target_path = await download_file(str(request.target_url))
        print("target_path: ", target_path)
        if not target_path or not (is_image(target_path) or is_video(target_path)):
            raise HTTPException(status_code=400, detail="Invalid target file")

        # 处理人脸替换
        output_path = await process_face_swap(source_path, target_path)
        print("output_path: ", output_path)
        if not output_path:
            raise HTTPException(status_code=500, detail="Face swap processing failed")

        return FaceSwapResponse(
            success=True,
            message="Face swap completed successfully",
            output_path=str(output_path)
        )

    except Exception as e:
        print("error: ", e)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # 清理临时文件
        if source_path and os.path.exists(source_path):
            os.remove(source_path)
        if target_path and os.path.exists(target_path):
            os.remove(target_path)
