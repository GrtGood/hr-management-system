#!/bin/bash

echo "===================================="
echo "   高校教职工人事信息管理系统"
echo "===================================="
echo ""

# 检查Python环境
echo "正在检查Python环境..."
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ 错误：未找到Python！"
    echo ""
    echo "请先安装Python 3.8或更高版本"
    echo "下载地址：https://www.python.org/downloads/"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi

# 使用python3或python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
else
    PYTHON_CMD="python"
    PIP_CMD="pip"
fi

echo "✅ Python环境检查通过"
echo ""

# 安装依赖
echo "正在安装依赖包..."
$PIP_CMD install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败，尝试使用默认源..."
    $PIP_CMD install -r requirements.txt --quiet
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败！请检查网络连接"
        echo ""
        read -p "按回车键退出..."
        exit 1
    fi
fi

echo "✅ 依赖安装完成"
echo ""

# 启动系统
echo "正在启动系统..."
echo ""
echo "===================================="
echo "   系统启动信息"
echo "===================================="
echo "登录地址：http://localhost:5000"
echo "用户名：admin"
echo "密码：admin123"
echo "===================================="
echo ""
echo "请保持此窗口打开，关闭窗口将停止系统"
echo "启动后请打开浏览器访问上述地址"
echo ""

$PYTHON_CMD app.py

echo ""
echo "系统已停止运行"
read -p "按回车键退出..."