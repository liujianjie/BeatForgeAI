# BeatForge AI

AI驱动的电音制作工作站 - 通过文本提示词生成电子音乐

## 项目结构

```
BeatForgeAI/
├── backend/                # Python后端服务
│   ├── api/               # FastAPI路由
│   ├── services/          # 业务服务层
│   ├── models/            # 数据模型
│   ├── core/              # 核心配置
│   ├── utils/             # 工具函数
│   ├── main.py            # 应用入口
│   └── requirements.txt   # Python依赖
├── frontend/              # Web测试前端
│   └── index.html         # 测试页面
├── storage/               # 文件存储
│   ├── audio/             # 生成的音频文件
│   └── temp/              # 临时文件
├── docker-compose.yml     # Docker编排
├── Dockerfile             # 后端Docker镜像
└── README.md              # 项目说明
```

## 快速开始

### 环境要求
- Python 3.11+
- CUDA支持的GPU（推荐RTX 3060+）或CPU模式
- 8GB+ RAM

### 安装步骤

1. 创建虚拟环境
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 启动服务
```bash
python main.py
```

4. 打开浏览器访问
```
http://localhost:8000
```

### Docker方式启动
```bash
docker-compose up --build
```

## API接口

### POST /api/ai/generate
生成AI电音

请求体:
```json
{
    "prompt": "energetic house music with deep bass",
    "style": "house",
    "bpm": 128,
    "duration": 10,
    "key": "C",
    "energy": 0.7
}
```

### GET /api/ai/styles
获取支持的电音风格列表

### GET /api/audio/{filename}
下载生成的音频文件

## 技术栈
- **后端**: Python + FastAPI + WebSocket
- **AI模型**: Meta MusicGen (facebook/musicgen-small)
- **音频处理**: librosa, soundfile, scipy
- **前端**: Unity (后续) / Web测试页面 (当前)
