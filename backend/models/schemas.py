"""
BeatForge AI - 数据模型定义
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from enum import Enum


class MusicStyle(str, Enum):
    """电音风格枚举"""
    HOUSE = "house"
    TECHNO = "techno"
    DUBSTEP = "dubstep"
    TRANCE = "trance"
    AMBIENT = "ambient"
    DRUM_AND_BASS = "drum_and_bass"
    EDM = "edm"
    LO_FI = "lo_fi"


class AIGenerationRequest(BaseModel):
    """AI音乐生成请求"""
    prompt: str = Field(..., min_length=1, max_length=500, description="音乐描述提示词")
    style: MusicStyle = Field(default=MusicStyle.HOUSE, description="电音风格")
    bpm: int = Field(default=128, ge=60, le=200, description="每分钟节拍数")
    duration: int = Field(default=10, ge=5, le=30, description="生成时长(秒)")
    key: str = Field(default="C", description="调式")
    energy: float = Field(default=0.7, ge=0.0, le=1.0, description="能量强度 0.0-1.0")

    @validator('prompt')
    def validate_prompt(cls, v):
        # 基础安全检查
        if not v.strip():
            raise ValueError('提示词不能为空')
        return v.strip()


class AIGenerationResponse(BaseModel):
    """AI音乐生成响应"""
    success: bool
    message: str
    filename: Optional[str] = None
    download_url: Optional[str] = None
    duration: Optional[float] = None
    generation_time: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class StyleInfo(BaseModel):
    """风格信息"""
    id: str
    name: str
    description: str
    bpm_range: List[int]


class StyleListResponse(BaseModel):
    """风格列表响应"""
    styles: List[StyleInfo]


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    model_loaded: bool
    gpu_available: bool
    device: str
