from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# 用户表（用于登录和权限管理）
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin 或 user
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """检查是否是管理员"""
        return self.role == 'admin'
    
    def is_user(self):
        """检查是否是普通用户"""
        return self.role == 'user'
    
    def get_display_name(self):
        """获取显示名称"""
        return self.username


# 部门表
class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    employees = db.relationship('Employee', backref='department', foreign_keys='Employee.department_id')
    # manager关系通过属性访问，避免循环引用
    @property
    def manager(self):
        """获取部门负责人"""
        if self.manager_id:
            return Employee.query.get(self.manager_id)
        return None
    
    def __repr__(self):
        return f'<Department {self.name}>'


# 员工基础信息表
class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_no = db.Column(db.String(20), unique=True, nullable=False)  # 工号
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))  # 性别
    birth_date = db.Column(db.Date)  # 出生日期
    id_card = db.Column(db.String(18), unique=True)  # 身份证号
    phone = db.Column(db.String(20))  # 电话
    email = db.Column(db.String(100))  # 邮箱
    address = db.Column(db.String(200))  # 地址
    
    # 工作信息
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    position = db.Column(db.String(50))  # 职位
    employment_type = db.Column(db.String(20))  # 聘用类型（全职/兼职/临时）
    hire_date = db.Column(db.Date)  # 入职日期
    status = db.Column(db.String(20), default='在职')  # 状态（在职/离职）
    
    # 教育背景
    education = db.Column(db.String(50))  # 学历
    major = db.Column(db.String(100))  # 专业
    graduate_school = db.Column(db.String(100))  # 毕业院校
    
    # 其他
    photo = db.Column(db.String(200))  # 照片路径
    remarks = db.Column(db.Text)  # 备注
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    attendances = db.relationship('Attendance', backref='employee', lazy='dynamic')
    performances = db.relationship('Performance', backref='employee', lazy='dynamic')
    titles = db.relationship('Title', backref='employee', lazy='dynamic')
    trainings = db.relationship('Training', backref='employee', lazy='dynamic')
    
    def __repr__(self):
        return f'<Employee {self.name}>'


# 考勤表
class Attendance(db.Model):
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)  # 考勤日期
    check_in_time = db.Column(db.Time)  # 上班打卡时间
    check_out_time = db.Column(db.Time)  # 下班打卡时间
    status = db.Column(db.String(20), default='正常')  # 状态（正常/迟到/早退/缺勤/请假）
    leave_type = db.Column(db.String(20))  # 请假类型（病假/事假/年假等）
    remarks = db.Column(db.Text)  # 备注
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Attendance {self.employee.name} {self.date}>'


# 绩效考核表
class Performance(db.Model):
    __tablename__ = 'performances'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)  # 考核年度
    quarter = db.Column(db.Integer)  # 考核季度（1-4）
    
    # 考核指标（可根据实际需求调整）
    teaching_score = db.Column(db.Float, default=0)  # 教学评分（0-100）
    research_score = db.Column(db.Float, default=0)  # 科研评分（0-100）
    service_score = db.Column(db.Float, default=0)  # 服务评分（0-100）
    total_score = db.Column(db.Float, default=0)  # 总分
    rating = db.Column(db.String(20))  # 等级（优秀/良好/合格/不合格）
    
    comments = db.Column(db.Text)  # 评语
    evaluator = db.Column(db.String(50))  # 考核人
    evaluation_date = db.Column(db.Date)  # 考核日期
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def calculate_total_score(self):
        """计算总分"""
        self.total_score = (self.teaching_score + self.research_score + self.service_score) / 3
        
        # 自动评级
        if self.total_score >= 90:
            self.rating = '优秀'
        elif self.total_score >= 80:
            self.rating = '良好'
        elif self.total_score >= 60:
            self.rating = '合格'
        else:
            self.rating = '不合格'
    
    def __repr__(self):
        return f'<Performance {self.employee.name} {self.year}Q{self.quarter}>'


# 职称评审表
class Title(db.Model):
    __tablename__ = 'titles'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    title_name = db.Column(db.String(50), nullable=False)  # 职称名称（助教/讲师/副教授/教授等）
    title_level = db.Column(db.String(20))  # 职称级别（初级/中级/高级）
    application_date = db.Column(db.Date)  # 申请日期
    approval_date = db.Column(db.Date)  # 批准日期
    status = db.Column(db.String(20), default='待审核')  # 状态（待审核/已通过/未通过）
    certificate_no = db.Column(db.String(50))  # 证书编号
    remarks = db.Column(db.Text)  # 备注
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<Title {self.employee.name} - {self.title_name}>'


# 培训与发展表
class Training(db.Model):
    __tablename__ = 'trainings'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    training_name = db.Column(db.String(100), nullable=False)  # 培训名称
    training_type = db.Column(db.String(50))  # 培训类型（内部培训/外部培训/在线培训等）
    training_content = db.Column(db.Text)  # 培训内容
    start_date = db.Column(db.Date)  # 开始日期
    end_date = db.Column(db.Date)  # 结束日期
    duration_hours = db.Column(db.Float)  # 培训时长（小时）
    location = db.Column(db.String(100))  # 培训地点
    instructor = db.Column(db.String(50))  # 讲师
    cost = db.Column(db.Float, default=0)  # 培训费用
    status = db.Column(db.String(20), default='已计划')  # 状态（已计划/进行中/已完成/已取消）
    completion_status = db.Column(db.String(20))  # 完成情况（优秀/良好/合格/不合格）
    certificate = db.Column(db.String(200))  # 证书路径
    remarks = db.Column(db.Text)  # 备注
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<Training {self.training_name} - {self.employee.name}>'
