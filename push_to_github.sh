#!/bin/bash

# 高校教职工人事信息管理系统 - GitHub推送脚本
# 使用方法：在电脑上运行此脚本即可推送到GitHub

echo "=========================================="
echo "  GitHub推送脚本"
echo "=========================================="
echo ""

# 你的GitHub用户名
GITHUB_USERNAME="GrtGood"

# 仓库名称（可以修改）
REPO_NAME="hr-management-system"

echo "步骤 1/4: 检查当前Git状态..."
git status

echo ""
echo "步骤 2/4: 添加GitHub远程仓库..."
git remote remove origin 2>/dev/null  # 删除可能存在的旧remote
git remote add origin https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git

echo ""
echo "步骤 3/4: 推送master分支..."
git checkout master
git push -u origin master

echo ""
echo "步骤 4/4: 推送feature分支..."
git checkout feature/hr-management-system-complete
git push -u origin feature/hr-management-system-complete

echo ""
echo "=========================================="
echo "✅ 推送完成！"
echo "=========================================="
echo ""
echo "接下来的步骤："
echo "1. 访问: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo "2. 你会看到提示创建Pull Request的按钮"
echo "3. 点击 'Compare & pull request' 创建PR"
echo ""
echo "如果遇到认证问题，请使用GitHub Personal Access Token"
echo "生成Token: https://github.com/settings/tokens"
echo ""
