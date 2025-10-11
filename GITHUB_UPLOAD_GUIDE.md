# 📤 GitHub上传指南

## 🎯 你的情况

- GitHub用户名：**GrtGood**
- 推荐仓库名：**hr-management-system**
- 项目已在本地Git准备好，只需推送到GitHub

---

## ✅ 方法1：使用自动脚本（最简单）

### 第1步：在GitHub创建空仓库

1. 电脑浏览器打开：https://github.com/new
2. 仓库名输入：`hr-management-system`
3. 选择 **Private**（私有，只有你能看到）或 **Public**（公开）
4. **重要**：不要勾选任何选项（README、.gitignore、license都不要选）
5. 点击 "Create repository"

### 第2步：在电脑上运行推送脚本

把项目复制到电脑后，在项目目录打开终端/命令行：

**Linux/Mac:**
```bash
chmod +x push_to_github.sh
./push_to_github.sh
```

**Windows (Git Bash):**
```bash
bash push_to_github.sh
```

### 第3步：输入GitHub凭据

- 用户名：`GrtGood`
- 密码：需要使用 **Personal Access Token**（不是GitHub登录密码）

**如何获取Token：**
1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 点击生成，复制Token（只显示一次！）
5. 在命令行密码处粘贴这个Token

### 第4步：创建Pull Request

1. 推送成功后，访问：https://github.com/GrtGood/hr-management-system
2. 你会看到黄色提示："**Compare & pull request**"
3. 点击按钮，填写PR标题和描述
4. 点击 "Create pull request"

---

## ✅ 方法2：手动命令（如果脚本不work）

### 第1步：创建GitHub仓库（同上）

### 第2步：在项目目录运行以下命令

```bash
# 进入项目目录
cd /path/to/hr-management-system

# 添加远程仓库
git remote add origin https://github.com/GrtGood/hr-management-system.git

# 推送master分支
git push -u origin master

# 推送feature分支
git push -u origin feature/hr-management-system-complete
```

### 第3步：创建Pull Request（同上）

---

## ❌ 常见问题

### Q1: 提示 "Authentication failed"
**A**: GitHub已经不支持密码登录，必须使用Personal Access Token

生成Token步骤：
1. https://github.com/settings/tokens
2. Generate new token (classic)
3. 勾选 `repo` 权限
4. 生成并复制Token
5. 在命令行密码处粘贴Token

### Q2: 提示 "remote origin already exists"
**A**: 先删除旧的remote
```bash
git remote remove origin
git remote add origin https://github.com/GrtGood/hr-management-system.git
```

### Q3: 推送很慢或卡住
**A**: 确保你的GitHub加速梯子已开启

### Q4: 提示 "repository not found"
**A**: 检查是否已在GitHub上创建了仓库，仓库名是否正确

---

## 📋 推送后检查清单

访问 https://github.com/GrtGood/hr-management-system 检查：

- [ ] 看到 `master` 和 `feature/hr-management-system-complete` 两个分支
- [ ] 可以看到3个commit记录
- [ ] 文件列表显示32个文件（包括README.md、app.py等）
- [ ] 有黄色提示可以创建Pull Request

---

## 🎉 推送成功后

你就可以在任何电脑上clone项目了：

```bash
git clone https://github.com/GrtGood/hr-management-system.git
cd hr-management-system
pip install -r requirements.txt
python app.py
```

---

## 💡 小提示

1. **Token保存**：第一次输入Token后，Git会记住，下次不用再输入
2. **私有仓库**：如果选择Private，只有你能看到，适合毕设
3. **公开仓库**：如果选择Public，任何人都能看到，可以写到简历里
4. **备份**：推送到GitHub后，你的代码就有云端备份了

---

**有问题随时问我！**
