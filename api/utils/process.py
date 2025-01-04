from pathlib import Path
from typing import Optional
import uuid
import logging

from facefusion import core
from facefusion import state_manager
from ..config import OUTPUT_DIR, FACE_SWAPPER_MODEL, EXECUTION_PROVIDERS, EXECUTION_THREAD_COUNT


def init_face_fusion():
    """初始化FaceFusion参数"""
    try:
        print("Initializing FaceFusion with parameters:")
        print(f"- Model: {FACE_SWAPPER_MODEL}")
        print(f"- Providers: {EXECUTION_PROVIDERS}")
        print(f"- Threads: {EXECUTION_THREAD_COUNT}")

        # 下载参数设置
        state_manager.init_item('download_providers', ['github', 'huggingface'])
        state_manager.init_item('download_scope', 'full')

        # 临时目录设置
        state_manager.init_item('temp_path', str(Path('temp')))
        state_manager.init_item('temp_frame_format', 'jpg')  # Literal['bmp', 'jpg', 'png']

        # 执行设备设置
        state_manager.init_item('execution_providers', ['cuda'])  # Literal['cpu', 'cuda', ...]
        state_manager.init_item('execution_device_id', '0')
        state_manager.init_item('execution_thread_count', EXECUTION_THREAD_COUNT)
        state_manager.init_item('execution_queue_count', 1)
        state_manager.init_item('video_memory_strategy', 'moderate')  # Literal['strict', 'moderate', 'tolerant']

        # 输出参数设置
        state_manager.init_item('output_video_encoder', 'libx264')  # Literal['libx264', ...]
        state_manager.init_item('output_video_quality', 80)
        state_manager.init_item('output_video_preset', 'medium')  # Literal['ultrafast', ..., 'veryslow']
        state_manager.init_item('output_video_fps', 30.0)
        state_manager.init_item('output_video_resolution', '1920x1080')
        state_manager.init_item('output_image_resolution', '1920x1080')
        state_manager.init_item('output_audio_encoder', 'aac')  # Literal['aac', 'libmp3lame', 'libopus', 'libvorbis']

        # 人脸检测参数
        state_manager.init_item('face_detector_model', 'yoloface')  # Literal['many', 'retinaface', 'scrfd', 'yoloface']
        state_manager.init_item('face_detector_size', '640x640')
        state_manager.init_item('face_detector_score', 0.5)
        state_manager.init_item('face_detector_angles', [0])

        # 人脸选择参数
        state_manager.init_item('face_selector_mode', 'reference')  # Literal['many', 'one', 'reference']
        state_manager.init_item('face_selector_order', 'left-right')  # Literal['left-right', ...]
        state_manager.init_item('reference_face_position', 0)
        state_manager.init_item('reference_face_distance', 0.6)
        state_manager.init_item('reference_frame_number', 0)

        # 人脸特征点检测参数
        state_manager.init_item('face_landmarker_model', '2dfan4')  # Literal['many', '2dfan4', 'peppa_wutz']
        state_manager.init_item('face_landmarker_score', 0.5)

        # 人脸遮罩参数
        state_manager.init_item('face_mask_types', ['box'])  # List[Literal['box', 'occlusion', 'region']]
        state_manager.init_item('face_mask_blur', 0.3)
        state_manager.init_item('face_mask_padding', (0, 0, 0, 0))  # Tuple[int, int, int, int]

        # 处理器设置
        state_manager.init_item('processors', ['face_swapper'])
        state_manager.init_item('face_swapper_model', FACE_SWAPPER_MODEL)
        state_manager.init_item('face_swapper_pixel_boost', '128x128')

        # 视频裁剪参数
        state_manager.init_item('trim_frame_start', 0)
        state_manager.init_item('trim_frame_end', 0)  # 0表示处理到结尾

        # 其他参数
        state_manager.init_item('skip_audio', False)
        state_manager.init_item('keep_temp', False)

        # 打印所有状态值
        print("\nCurrent state values:")
        for key in ['face_swapper_model', 'execution_providers', 'execution_thread_count', 'processors',
                   'face_detector_model', 'face_detector_size', 'face_detector_score', 'face_detector_angles',
                   'face_selector_mode', 'face_selector_order', 'reference_face_position', 'reference_face_distance',
                   'face_landmarker_model', 'face_landmarker_score', 'execution_queue_count',
                   'output_video_encoder', 'output_video_quality', 'output_video_fps', 'output_video_preset',
                   'output_audio_encoder', 'video_memory_strategy',
                   'download_providers', 'download_scope', 'output_video_resolution', 'output_image_resolution',
                   'temp_frame_format', 'face_swapper_pixel_boost', 'trim_frame_start', 'trim_frame_end']:
            print(f"- {key}: {state_manager.get_item(key)}")

    except Exception as e:
        print(f"Error in init_face_fusion: {str(e)}")
        raise


async def process_face_swap(source_path: Path, target_path: Path) -> Optional[Path]:
    """
    处理人脸替换
    返回输出文件路径
    """
    try:
        print("\nStarting face swap process:")
        print(f"- Source: {source_path}")
        print(f"- Target: {target_path}")

        # 初始化参数
        init_face_fusion()

        # 设置输入输出路径
        output_path = OUTPUT_DIR / f"{uuid.uuid4()}{target_path.suffix}"
        print(f"- Output: {output_path}")

        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 设置处理参数
        state_manager.init_item('source_paths', [str(source_path)])
        state_manager.init_item('target_path', str(target_path))
        state_manager.init_item('output_path', str(output_path))

        # 设置视频处理范围
        import cv2
        video = cv2.VideoCapture(str(target_path))
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        video.release()
        state_manager.init_item('trim_frame_end', total_frames)  # 设置结束帧为视频总帧数

        print("\nProcessing parameters:")
        print(f"- Source paths: {state_manager.get_item('source_paths')}")
        print(f"- Target path: {state_manager.get_item('target_path')}")
        print(f"- Output path: {state_manager.get_item('output_path')}")

        # 执行处理
        print("\nStarting conditional_process...")
        result = core.conditional_process()
        print(f"Process result code: {result}")

        if result == 0:
            if output_path.exists():
                print("Output file created successfully")
                return output_path
            else:
                print("Error: Output file was not created")
                return None
        else:
            print(f"Process failed with code: {result}")
            return None

    except Exception as e:
        print(f"Error in process_face_swap: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None
