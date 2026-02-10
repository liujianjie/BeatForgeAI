"""
BeatForge AI - 应用入口
AI驱动的电音制作工作站后端服务
"""
import sys
import logging
from pathlib import Path

# 将backend目录加入Python路径
sys.path.insert(0, str(Path(__file__).resolve().parent))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from core.config import HOST, PORT, DEBUG, BASE_DIR
from api.routes import router as api_router

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("BeatForgeAI")

# 创建FastAPI应用
app = FastAPI(
    title="BeatForge AI",
    description="AI驱动的电音制作工作站 - 通过文本提示词生成电子音乐",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS中间件 - 允许Unity客户端和Web前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(api_router, prefix="/api")

# 静态文件 - 前端页面
frontend_dir = BASE_DIR / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")


@app.get("/", tags=["首页"])
async def root():
    """返回Web测试前端页面"""
    index_path = frontend_dir / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {
        "name": "BeatForge AI",
        "version": "0.1.0",
        "description": "AI驱动的电音制作工作站",
        "docs": "/docs",
        "api_prefix": "/api",
    }


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("=" * 60)
    logger.info("  BeatForge AI 服务启动中...")
    logger.info(f"  文档地址: http://localhost:{PORT}/docs")
    logger.info(f"  前端地址: http://localhost:{PORT}/")
    logger.info("=" * 60)
    
    # 注意：模型在首次请求时懒加载，避免启动太慢
    # 如果想预加载模型，取消下面的注释：
    # from services.ai_service import ai_service
    # ai_service.load_model()


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("BeatForge AI 服务已关闭")


if __name__ == "__main__":
    logger.info(f"启动服务: {HOST}:{PORT}, debug={DEBUG}")
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info",
    )
