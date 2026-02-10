"""
BeatForge AI - API路由定义
"""
import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from core.config import AUDIO_DIR, MUSIC_STYLES
from models.schemas import (
    AIGenerationRequest,
    AIGenerationResponse,
    StyleListResponse,
    StyleInfo,
    HealthResponse,
)
from services.ai_service import ai_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["系统"])
async def health_check():
    """健康检查接口"""
    status = ai_service.get_status()
    return HealthResponse(
        status="ok",
        model_loaded=status["model_loaded"],
        gpu_available=status["gpu_available"],
        device=status["device"],
    )


@router.get("/ai/styles", response_model=StyleListResponse, tags=["AI生成"])
async def get_styles():
    """获取支持的电音风格列表"""
    styles = []
    for style_id, style_config in MUSIC_STYLES.items():
        styles.append(StyleInfo(
            id=style_id,
            name=style_config["name"],
            description=style_config["description"],
            bpm_range=list(style_config["bpm_range"]),
        ))
    return StyleListResponse(styles=styles)


@router.post("/ai/generate", response_model=AIGenerationResponse, tags=["AI生成"])
async def generate_music(request: AIGenerationRequest):
    """
    AI生成电音
    
    通过文本提示词和参数生成电子音乐片段
    """
    logger.info(f"收到生成请求: style={request.style}, prompt={request.prompt}, "
                f"bpm={request.bpm}, duration={request.duration}")

    try:
        filename, generation_time, metadata = await ai_service.generate_music(request)

        return AIGenerationResponse(
            success=True,
            message="音频生成成功",
            filename=filename,
            download_url=f"/api/audio/{filename}",
            duration=metadata["actual_duration"],
            generation_time=round(generation_time, 2),
            metadata=metadata,
        )

    except RuntimeError as e:
        logger.error(f"生成失败: {str(e)}")
        return AIGenerationResponse(
            success=False,
            message=f"生成失败: {str(e)}",
        )
    except Exception as e:
        logger.error(f"未知错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")


@router.get("/audio/{filename}", tags=["音频"])
async def download_audio(filename: str):
    """下载生成的音频文件"""
    filepath = AUDIO_DIR / filename

    if not filepath.exists():
        raise HTTPException(status_code=404, detail="音频文件不存在")

    # 安全检查：防止路径遍历
    if not filepath.resolve().is_relative_to(AUDIO_DIR.resolve()):
        raise HTTPException(status_code=403, detail="禁止访问")

    return FileResponse(
        path=str(filepath),
        media_type="audio/wav",
        filename=filename,
    )


@router.get("/audio/list/all", tags=["音频"])
async def list_audio_files():
    """列出所有已生成的音频文件"""
    files = []
    for f in AUDIO_DIR.glob("*.wav"):
        files.append({
            "filename": f.name,
            "size_bytes": f.stat().st_size,
            "download_url": f"/api/audio/{f.name}",
        })
    
    # 按修改时间倒序
    files.sort(key=lambda x: x["filename"], reverse=True)
    
    return {"files": files, "total": len(files)}
