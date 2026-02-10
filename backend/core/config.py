"""
BeatForge AI - 配置管理
"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = Path(__file__).resolve().parent.parent

# 存储目录
STORAGE_DIR = BASE_DIR / "storage"
AUDIO_DIR = STORAGE_DIR / "audio"
TEMP_DIR = STORAGE_DIR / "temp"

# 确保目录存在
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# 服务配置
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# AI模型配置
MODEL_NAME = os.getenv("MODEL_NAME", "facebook/musicgen-small")  # small模型更快，适合demo
MAX_DURATION = int(os.getenv("MAX_DURATION", "30"))  # 最大生成时长(秒)
DEFAULT_DURATION = int(os.getenv("DEFAULT_DURATION", "10"))  # 默认生成时长(秒)
SAMPLE_RATE = 32000  # MusicGen输出采样率

# 电音风格配置
MUSIC_STYLES = {
    "house": {
        "name": "House",
        "description": "四四拍节奏，温暖的贝斯线，经典House风格",
        "prompt_prefix": "house music, four on the floor beat, warm bassline",
        "bpm_range": (120, 130)
    },
    "techno": {
        "name": "Techno",
        "description": "硬核节拍，合成器音色，工业感",
        "prompt_prefix": "techno music, hard kick drum, synthesizer, industrial",
        "bpm_range": (125, 140)
    },
    "dubstep": {
        "name": "Dubstep",
        "description": "重低音，Wobble Bass，半拍节奏",
        "prompt_prefix": "dubstep music, heavy bass drop, wobble bass, halftime rhythm",
        "bpm_range": (138, 142)
    },
    "trance": {
        "name": "Trance",
        "description": "梦幻旋律，渐进式编排，情感丰富",
        "prompt_prefix": "trance music, euphoric melody, progressive arrangement, emotional",
        "bpm_range": (128, 140)
    },
    "ambient": {
        "name": "Ambient",
        "description": "氛围音乐，空灵音色，放松感",
        "prompt_prefix": "ambient electronic music, atmospheric pads, ethereal, relaxing",
        "bpm_range": (60, 100)
    },
    "drum_and_bass": {
        "name": "Drum & Bass",
        "description": "快速碎拍，深沉贝斯，高能量",
        "prompt_prefix": "drum and bass music, fast breakbeat, deep bass, high energy",
        "bpm_range": (160, 180)
    },
    "edm": {
        "name": "EDM",
        "description": "主流电子舞曲，大气Drop，节日感",
        "prompt_prefix": "EDM, electronic dance music, big drop, festival energy, euphoric",
        "bpm_range": (126, 132)
    },
    "lo_fi": {
        "name": "Lo-Fi",
        "description": "低保真，温暖质感，放松节拍",
        "prompt_prefix": "lo-fi electronic music, warm texture, chill beat, vinyl crackle",
        "bpm_range": (70, 90)
    }
}
