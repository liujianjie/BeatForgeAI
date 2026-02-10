@echo off
echo ============================================
echo   BeatForge AI - 启动服务
echo ============================================
echo.

cd /d "%~dp0\..\backend"

echo 激活虚拟环境...
call venv\Scripts\activate.bat

echo 启动BeatForge AI服务...
echo 访问地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo ============================================

python main.py
