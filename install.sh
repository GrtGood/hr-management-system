#!/bin/bash
# 高校教职工人事信息管理系统 - 一键安装脚本
# 运行方法：bash install.sh

echo "开始创建项目..."

# 创建项目目录
mkdir -p hr-management-system
cd hr-management-system

# 创建子目录
mkdir -p templates/{employees,departments,attendances,performances,titles,trainings}
mkdir -p static/{css,js,uploads}

echo "正在下载项目文件..."

# 下载所有文件
curl -o requirements.txt https://raw.githubusercontent.com/GrtGood/hr-management-system/main/requirements.txt 2>/dev/null || echo "Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
openpyxl==3.1.2
pandas==2.1.4
python-dateutil==2.8.2" > requirements.txt

echo "✓ requirements.txt 已创建"

# 提示：如果GitHub没有仓库，需要手动复制其他文件
echo ""
echo "=========================================="
echo "下一步："
echo "1. 请访问聊天记录，复制其他核心文件"
echo "2. 或者我将生成单文件版本"
echo "=========================================="
