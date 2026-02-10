@echo off
echo ============================================
echo   BeatForge AI - 环境安装脚本 (Windows)
echo ============================================
echo.

cd /d "%~dp0\..\backend"

echo [1/3] 创建Python虚拟环境...
python -m venv venv
if errorlevel 1 (
    echo 错误: Python未安装或版本不正确，请安装Python 3.11+
    pause
    exit /b 1
)

echo [2/3] 激活虚拟环境...
call venv\Scripts\activate.bat

echo [3/3] 安装依赖包...
pip install -r requirements.txt

echo.
echo ============================================
echo   安装完成！
echo   运行 scripts\start.bat 启动服务
echo ============================================
pause
