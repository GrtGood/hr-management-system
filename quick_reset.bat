@echo off
REM 一键重置数据库并生成测试数据 - Windows版本

echo ==========================================
echo   快速重置数据库和测试数据
echo ==========================================

echo.
echo 步骤1: 重置数据库...
python reset_database.py

echo.
echo 步骤2: 初始化学院和考核标准...
python init_colleges.py

echo.
echo 步骤3: 生成测试数据...
python init_test_data.py

echo.
echo ==========================================
echo   ✅ 全部完成！
echo ==========================================
echo.
echo 可以启动系统了：
echo   python app.py
echo.
echo 访问：http://localhost:5000
echo 登录：admin / admin123
echo.
pause
