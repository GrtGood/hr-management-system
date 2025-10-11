# 高校教职工人事信息管理系统

> 泰州学院 计算机科学与技术专业 本科毕业设计项目

## 📋 项目简介

本系统是一个基于Flask框架开发的高校教职工人事信息管理系统，主要用于管理教职工的基本信息、考勤、绩效考核、职称评审和培训发展等数据。

### 主要功能模块

✅ **员工基础信息管理** - 员工档案、基本信息录入与查询  
✅ **部门管理** - 组织架构、部门信息维护  
✅ **考勤管理** - 打卡记录、请假管理  
✅ **绩效考核** - 教学/科研/服务评分、等级评定  
✅ **职称评审** - 职称申请、审核流程  
✅ **培训与发展** - 培训记录、证书管理  
✅ **数据统计与导出** - Excel导出、数据可视化

### 技术栈

- **后端框架**: Flask 3.0
- **数据库**: SQLite (轻量级，无需安装配置)
- **ORM**: Flask-SQLAlchemy
- **认证**: Flask-Login
- **前端**: HTML + Bootstrap 5 + Bootstrap Icons
- **数据导出**: openpyxl, pandas

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip (Python包管理器)

### 安装步骤

1. **克隆/下载项目**
```bash
cd hr-management-system
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

如果安装速度慢，可以使用国内镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

3. **运行应用**
```bash
python app.py
```

首次运行会自动：
- 创建数据库
- 初始化表结构
- 创建管理员账户（用户名: admin，密码: admin123）

4. **访问系统**

打开浏览器访问: `http://localhost:5000`

使用默认账户登录：
- 用户名：`admin`
- 密码：`admin123`

## 📁 项目结构

```
hr-management-system/
├── app.py                 # Flask应用主文件
├── app_routes.py          # 额外路由（职称、培训、导出）
├── models.py              # 数据库模型定义
├── config.py              # 配置文件
├── requirements.txt       # Python依赖包
├── hr_system.db          # SQLite数据库文件（运行后自动生成）
├── templates/            # HTML模板目录
│   ├── base.html         # 基础模板
│   ├── login.html        # 登录页面
│   ├── index.html        # 首页
│   ├── employees/        # 员工管理模板
│   ├── departments/      # 部门管理模板
│   ├── attendances/      # 考勤管理模板
│   ├── performances/     # 绩效考核模板
│   ├── titles/           # 职称评审模板
│   └── trainings/        # 培训管理模板
└── static/               # 静态文件目录
    ├── css/
    ├── js/
    └── uploads/          # 文件上传目录
```

## 💡 使用说明

### 用户角色

系统支持两种用户角色：

1. **管理员（admin）**
   - 拥有所有功能权限
   - 可以添加、编辑、删除数据
   - 可以导出Excel报表

2. **普通用户（user）**
   - 只能查看数据
   - 不能进行增删改操作

### 功能使用

#### 1. 员工管理
- 添加员工：填写工号、姓名、部门等基本信息
- 编辑员工：更新员工信息、调整部门
- 查看详情：查看员工完整档案
- 导出数据：导出员工信息Excel表格

#### 2. 部门管理
- 添加部门：设置部门代码、名称、负责人
- 编辑部门：修改部门信息
- 删除部门：删除前需确保部门下无员工

#### 3. 考勤管理
- 录入考勤：记录员工打卡时间
- 请假管理：记录请假类型和时间
- 考勤查询：按员工、日期范围筛选

#### 4. 绩效考核
- 添加考核：录入教学、科研、服务三项评分
- 自动评级：系统自动计算总分并评定等级
  - 优秀：≥90分
  - 良好：80-89分
  - 合格：60-79分
  - 不合格：<60分

#### 5. 职称评审
- 申请职称：提交职称评审申请
- 审核流程：待审核 → 已通过/未通过
- 证书管理：记录职称证书编号

#### 6. 培训发展
- 培训计划：创建培训项目
- 培训记录：记录参与人员和完成情况
- 费用统计：统计培训成本

## 📊 数据导出

系统支持将数据导出为Excel文件：

- **导出员工信息**: `/export/employees`
- **导出考勤记录**: `/export/attendances`
- **导出绩效考核**: `/export/performances`

导出的Excel文件包含完整的字段信息，方便进行数据分析和存档。

## 🔧 配置说明

### 修改密钥

编辑 `config.py` 文件，修改 `SECRET_KEY`：

```python
SECRET_KEY = 'your-new-secret-key'
```

### 修改数据库

默认使用SQLite，如需更换为MySQL/PostgreSQL，修改 `config.py` 中的 `SQLALCHEMY_DATABASE_URI`。

### 修改端口

编辑 `app.py` 最后一行：

```python
app.run(debug=True, host='0.0.0.0', port=5000)  # 改为其他端口
```

## 🐛 常见问题

### Q1: 安装依赖时出错
**A**: 确保Python版本≥3.8，使用国内镜像源加速安装

### Q2: 无法访问系统
**A**: 检查5000端口是否被占用，或修改为其他端口

### Q3: 忘记管理员密码
**A**: 删除 `hr_system.db` 文件，重新运行 `python app.py` 会重新创建默认账户

### Q4: 数据库错误
**A**: 删除 `hr_system.db` 文件后重新运行程序

## 📝 开发说明

### 添加新功能

1. 在 `models.py` 中定义新的数据模型
2. 在 `app.py` 或 `app_routes.py` 中添加路由
3. 在 `templates/` 中创建对应的HTML模板

### 数据库迁移

当修改模型后，删除 `hr_system.db` 并重新运行程序，或使用Flask-Migrate进行迁移。

## 📄 许可证

本项目仅用于学习和毕业设计，未经许可不得用于商业用途。

## 👨‍💻 作者信息

- **学校**: 泰州学院
- **专业**: 计算机科学与技术
- **年级**: 22级
- **项目**: 本科毕业设计

## 📞 技术支持

如有问题，请查看代码注释或参考Flask官方文档：
- Flask文档: https://flask.palletsprojects.com/
- Bootstrap文档: https://getbootstrap.com/

---

**祝毕业设计顺利通过！🎓**
