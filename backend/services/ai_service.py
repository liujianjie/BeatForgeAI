"""
BeatForge AI - AI音乐生成服务
使用Meta的MusicGen模型生成电子音乐
"""
import time
import uuid
import logging
import numpy as np
from pathlib import Path
from typing import Optional, Tuple

import torch
import scipy.io.wavfile as wav_io

from core.config import MODEL_NAME, AUDIO_DIR, SAMPLE_RATE, MUSIC_STYLES, MAX_DURATION
from models.schemas import AIGenerationRequest

logger = logging.getLogger(__name__)


class AIService:
    """AI音乐生成服务"""

    def __init__(self):
        self.model = None
        self.processor = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_loaded = False
        logger.info(f"AI服务初始化，使用设备: {self.device}")

    def load_model(self):
        """加载MusicGen模型"""
        if self.model_loaded:
            logger.info("模型已加载，跳过")
            return

        try:
            logger.info(f"开始加载模型: {MODEL_NAME}")
            start_time = time.time()

            from transformers import AutoProcessor, MusicgenForConditionalGeneration

            self.processor = AutoProcessor.from_pretrained(MODEL_NAME)
            self.model = MusicgenForConditionalGeneration.from_pretrained(MODEL_NAME)
            self.model.to(self.device)
            self.model.eval()

            load_time = time.time() - start_time
            self.model_loaded = True
            logger.info(f"模型加载完成，耗时: {load_time:.2f}秒")

        except Exception as e:
            logger.error(f"模型加载失败: {str(e)}")
            raise RuntimeError(f"模型加载失败: {str(e)}")

    def build_prompt(self, request: AIGenerationRequest) -> str:
        """
        根据请求参数构建完整的提示词
        将用户输入 + 风格模板 + 参数信息组合成最终提示词
        """
        style_config = MUSIC_STYLES.get(request.style.value, MUSIC_STYLES["house"])
        prompt_parts = []

        # 1. 风格前缀
        prompt_parts.append(style_config["prompt_prefix"])

        # 2. 用户提示词
        prompt_parts.append(request.prompt)

        # 3. BPM信息
        prompt_parts.append(f"{request.bpm} BPM")

        # 4. 调式信息
        if request.key and request.key != "C":
            prompt_parts.append(f"key of {request.key}")

        # 5. 能量描述
        if request.energy >= 0.8:
            prompt_parts.append("high energy, intense, powerful")
        elif request.energy >= 0.5:
            prompt_parts.append("moderate energy, groovy")
        else:
            prompt_parts.append("low energy, calm, subtle")

        # 6. 音质描述
        prompt_parts.append("high quality, professional production, stereo")

        full_prompt = ", ".join(prompt_parts)
        logger.info(f"构建提示词: {full_prompt}")
        return full_prompt

    async def generate_music(self, request: AIGenerationRequest) -> Tuple[str, float, dict]:
        """
        生成AI电音
        
        Args:
            request: 生成请求参数
            
        Returns:
            (文件名, 生成耗时, 元数据)
        """
        if not self.model_loaded:
            self.load_model()

        start_time = time.time()

        # 构建提示词
        full_prompt = self.build_prompt(request)

        # 限制时长
        duration = min(request.duration, MAX_DURATION)

        try:
            # 处理输入
            inputs = self.processor(
                text=[full_prompt],
                padding=True,
                return_tensors="pt"
            ).to(self.device)

            # 计算生成token数量
            # MusicGen: 约50 tokens/秒 (对于32kHz采样率)
            max_new_tokens = int(duration * 50)

            logger.info(f"开始生成音频，时长: {duration}秒, tokens: {max_new_tokens}")

            # 生成音频
            with torch.no_grad():
                audio_values = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    do_sample=True,
                    guidance_scale=3.0,
                )

            # 转换为numpy数组
            audio_array = audio_values[0, 0].cpu().numpy()

            # 归一化到 [-1, 1]
            if np.max(np.abs(audio_array)) > 0:
                audio_array = audio_array / np.max(np.abs(audio_array))

            # 生成文件名
            filename = f"beatforge_{request.style.value}_{uuid.uuid4().hex[:8]}.wav"
            filepath = AUDIO_DIR / filename

            # 保存为WAV文件
            # 转换为16位整数
            audio_int16 = (audio_array * 32767).astype(np.int16)
            wav_io.write(str(filepath), SAMPLE_RATE, audio_int16)

            generation_time = time.time() - start_time
            actual_duration = len(audio_array) / SAMPLE_RATE

            # 元数据
            metadata = {
                "prompt": full_prompt,
                "style": request.style.value,
                "bpm": request.bpm,
                "key": request.key,
                "energy": request.energy,
                "requested_duration": duration,
                "actual_duration": round(actual_duration, 2),
                "sample_rate": SAMPLE_RATE,
                "device": self.device,
                "model": MODEL_NAME,
            }

            logger.info(f"音频生成完成: {filename}, 耗时: {generation_time:.2f}秒, "
                        f"实际时长: {actual_duration:.2f}秒")

            return filename, generation_time, metadata

        except Exception as e:
            logger.error(f"音频生成失败: {str(e)}")
            raise RuntimeError(f"音频生成失败: {str(e)}")

    def get_status(self) -> dict:
        """获取服务状态"""
        return {
            "model_loaded": self.model_loaded,
            "gpu_available": torch.cuda.is_available(),
            "device": self.device,
            "model_name": MODEL_NAME,
        }


# 全局单例
ai_service = AIService()
