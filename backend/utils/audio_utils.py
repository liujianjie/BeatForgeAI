"""
BeatForge AI - 音频工具函数
"""
import numpy as np
from typing import Optional


def normalize_audio(audio: np.ndarray, target_db: float = -3.0) -> np.ndarray:
    """
    音频归一化
    
    Args:
        audio: 音频数组
        target_db: 目标分贝值
    
    Returns:
        归一化后的音频数组
    """
    if np.max(np.abs(audio)) == 0:
        return audio
    
    # 计算当前RMS
    rms = np.sqrt(np.mean(audio ** 2))
    if rms == 0:
        return audio
    
    # 目标RMS
    target_rms = 10 ** (target_db / 20.0)
    
    # 缩放
    gain = target_rms / rms
    normalized = audio * gain
    
    # 防止削波
    max_val = np.max(np.abs(normalized))
    if max_val > 1.0:
        normalized = normalized / max_val
    
    return normalized


def fade_in_out(audio: np.ndarray, sample_rate: int, 
                fade_in_ms: int = 50, fade_out_ms: int = 100) -> np.ndarray:
    """
    添加淡入淡出效果
    
    Args:
        audio: 音频数组
        sample_rate: 采样率
        fade_in_ms: 淡入时长(毫秒)
        fade_out_ms: 淡出时长(毫秒)
    
    Returns:
        处理后的音频数组
    """
    result = audio.copy()
    
    # 淡入
    fade_in_samples = int(sample_rate * fade_in_ms / 1000)
    if fade_in_samples > 0 and fade_in_samples < len(result):
        fade_in_curve = np.linspace(0, 1, fade_in_samples)
        result[:fade_in_samples] *= fade_in_curve
    
    # 淡出
    fade_out_samples = int(sample_rate * fade_out_ms / 1000)
    if fade_out_samples > 0 and fade_out_samples < len(result):
        fade_out_curve = np.linspace(1, 0, fade_out_samples)
        result[-fade_out_samples:] *= fade_out_curve
    
    return result


def get_audio_info(audio: np.ndarray, sample_rate: int) -> dict:
    """
    获取音频信息
    
    Args:
        audio: 音频数组
        sample_rate: 采样率
    
    Returns:
        音频信息字典
    """
    duration = len(audio) / sample_rate
    rms = np.sqrt(np.mean(audio ** 2))
    peak = np.max(np.abs(audio))
    
    return {
        "duration_seconds": round(duration, 2),
        "sample_rate": sample_rate,
        "samples": len(audio),
        "rms_level": round(float(rms), 4),
        "peak_level": round(float(peak), 4),
        "rms_db": round(20 * np.log10(rms + 1e-10), 2),
        "peak_db": round(20 * np.log10(peak + 1e-10), 2),
    }
