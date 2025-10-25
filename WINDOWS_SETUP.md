# 🪟 Windows 快速设置指南

## 问题

您在本地Windows系统，而新创建的脚本文件还在远程服务器上。

---

## 🚀 解决方法（3选1）

### 方法1：直接创建bat文件（最快）⭐

在 `C:\Users\zxc31\Desktop\hr-management-system` 目录，创建文件 `quick_reset.bat`，内容如下：

```batch
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
```

然后双击运行 `quick_reset.bat` 即可！

---

### 方法2：手动执行命令（也很快）⭐⭐

在 `C:\Users\zxc31\Desktop\hr-management-system` 目录打开命令提示符，依次运行：

```cmd
python reset_database.py
python init_colleges.py
python init_test_data.py
```

3个命令执行完，所有测试数据就生成好了！

---

### 方法3：从GitHub拉取（需要先推送）

如果您已经推送了代码到GitHub：

```cmd
cd C:\Users\zxc31\Desktop\hr-management-system
git fetch origin
git pull origin feature/teacher-requirements
```

然后就可以运行 `quick_reset.bat` 了。

---

## 📝 创建 init_test_data.py

如果您的本地也没有 `init_test_data.py`，请创建此文件（约270行代码）。

**快捷方式：** 使用方法2手动执行命令，不需要bat脚本。

---

## ✅ 最简单的方法

**推荐使用方法2**，直接在命令提示符执行3条命令：

```cmd
cd C:\Users\zxc31\Desktop\hr-management-system
python reset_database.py
python init_colleges.py
python init_test_data.py
```

执行完后，所有测试数据就恢复了！

---

## 🎯 测试数据包含

执行完后会自动生成：
- ✅ 8个员工
- ✅ 8个部门
- ✅ 4个职称申请
- ✅ 40条考勤记录
- ✅ 3条绩效考核
- ✅ 3条培训记录
- ✅ 5个用户账号

---

## 📞 如果遇到问题

### 问题1：找不到 init_test_data.py

**原因：** 文件还在远程服务器上，本地没有

**解决：**
1. 从GitHub拉取代码
2. 或者手动创建这个文件（我可以提供完整代码）

### 问题2：找不到 reset_database.py

**原因：** 您可能不在正确的目录

**解决：**
```cmd
cd C:\Users\zxc31\Desktop\hr-management-system
dir reset_database.py
```

确认文件存在后再执行。

---

## 🎉 现在开始

最快的方法（不需要创建任何文件）：

```cmd
cd C:\Users\zxc31\Desktop\hr-management-system
python reset_database.py && python init_colleges.py && python init_test_data.py
```

一条命令搞定！

---

_如需帮助，请告诉我具体遇到什么问题。_
