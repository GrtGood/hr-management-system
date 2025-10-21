@echo off
chcp 65001 >nul
echo ====================================
echo   高校教职工人事信息管理系统
echo ====================================
echo.
echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python！
    echo.
    echo 请先安装Python 3.8或更高版本
    echo 下载地址：https://www.python.org/downloads/
    echo 安装时请勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python环境检查通过
echo.
echo 正在安装依赖包...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
if errorlevel 1 (
    echo ❌ 依赖安装失败，尝试使用默认源...
    pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo ❌ 依赖安装失败！请检查网络连接
        echo.
        pause
        exit /b 1
    )
)

echo ✅ 依赖安装完成
echo.
echo 正在启动系统...
echo.
echo ====================================
echo   系统启动信息
echo ====================================
echo 登录地址：http://localhost:5000
echo 用户名：admin
echo 密码：admin123
echo ====================================
echo.
echo 请保持此窗口打开，关闭窗口将停止系统
echo 启动后请打开浏览器访问上述地址
echo.

python app.py

echo.
echo 系统已停止运行
pause