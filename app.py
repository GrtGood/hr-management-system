from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Employee, Department, Attendance, Performance, Title, Training
from config import Config
from datetime import datetime, date, timedelta
from functools import wraps
import os
from werkzeug.utils import secure_filename
from openpyxl import Workbook
from io import BytesIO
from sqlalchemy import func, extract

# 创建Flask应用
app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
db.init_app(app)

# 初始化登录管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 管理员权限装饰器
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('需要管理员权限', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# 检查文件扩展名
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# ==================== 首页和登录 ====================

@app.route('/')
@login_required
def index():
    """首页 - 显示统计数据"""
    # 统计数据
    total_employees = Employee.query.filter_by(status='在职').count()
    total_departments = Department.query.count()
    
    # 今日考勤
    today = date.today()
    today_attendances = Attendance.query.filter_by(date=today).count()
    
    # 待审核职称
    pending_titles = Title.query.filter_by(status='待审核').count()
    
    # 本月培训
    current_month = today.month
    current_year = today.year
    monthly_trainings = Training.query.filter(
        extract('year', Training.start_date) == current_year,
        extract('month', Training.start_date) == current_month
    ).count()
    
    # 最近员工
    recent_employees = Employee.query.order_by(Employee.created_at.desc()).limit(5).all()
    
    return render_template('index.html',
                         total_employees=total_employees,
                         total_departments=total_departments,
                         today_attendances=today_attendances,
                         pending_titles=pending_titles,
                         monthly_trainings=monthly_trainings,
                         recent_employees=recent_employees)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('登录成功！', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('用户名或密码错误', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """退出登录"""
    logout_user()
    flash('已退出登录', 'success')
    return redirect(url_for('login'))


# ==================== 员工管理 ====================

@app.route('/employees')
@login_required
def employees():
    """员工列表"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    department_id = request.args.get('department', type=int)
    
    # 高级搜索参数
    is_advanced = request.args.get('advanced') == '1'
    name = request.args.get('name', '')
    employee_no = request.args.get('employee_no', '')
    gender = request.args.get('gender', '')
    position = request.args.get('position', '')
    employment_type = request.args.get('employment_type', '')
    education = request.args.get('education', '')
    status = request.args.get('status', '')
    hire_date_start = request.args.get('hire_date_start', '')
    hire_date_end = request.args.get('hire_date_end', '')
    
    query = Employee.query
    
    if is_advanced:
        # 高级搜索逻辑
        if name:
            query = query.filter(Employee.name.like(f'%{name}%'))
        if employee_no:
            query = query.filter(Employee.employee_no.like(f'%{employee_no}%'))
        if gender:
            query = query.filter_by(gender=gender)
        if department_id:
            query = query.filter_by(department_id=department_id)
        if position:
            query = query.filter(Employee.position.like(f'%{position}%'))
        if employment_type:
            query = query.filter_by(employment_type=employment_type)
        if education:
            query = query.filter_by(education=education)
        if status:
            query = query.filter_by(status=status)
        if hire_date_start:
            query = query.filter(Employee.hire_date >= datetime.strptime(hire_date_start, '%Y-%m-%d').date())
        if hire_date_end:
            query = query.filter(Employee.hire_date <= datetime.strptime(hire_date_end, '%Y-%m-%d').date())
    else:
        # 基本搜索逻辑
        if search:
            query = query.filter(
                (Employee.name.like(f'%{search}%')) |
                (Employee.employee_no.like(f'%{search}%'))
            )
        # 部门筛选
        if department_id:
            query = query.filter_by(department_id=department_id)
    
    # 分页
    pagination = query.order_by(Employee.created_at.desc()).paginate(
        page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False
    )
    
    departments = Department.query.all()
    
    return render_template('employees/list.html',
                         employees=pagination.items,
                         pagination=pagination,
                         departments=departments,
                         search=search,
                         department_id=department_id)


@app.route('/employees/add', methods=['GET', 'POST'])
@admin_required
def add_employee():
    """添加员工"""
    if request.method == 'POST':
        try:
            employee = Employee(
                employee_no=request.form.get('employee_no'),
                name=request.form.get('name'),
                gender=request.form.get('gender'),
                birth_date=datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date() if request.form.get('birth_date') else None,
                id_card=request.form.get('id_card'),
                phone=request.form.get('phone'),
                email=request.form.get('email'),
                address=request.form.get('address'),
                department_id=request.form.get('department_id'),
                position=request.form.get('position'),
                employment_type=request.form.get('employment_type'),
                hire_date=datetime.strptime(request.form.get('hire_date'), '%Y-%m-%d').date() if request.form.get('hire_date') else None,
                education=request.form.get('education'),
                major=request.form.get('major'),
                graduate_school=request.form.get('graduate_school'),
                remarks=request.form.get('remarks')
            )
            
            db.session.add(employee)
            db.session.commit()
            
            flash('员工添加成功！', 'success')
            return redirect(url_for('employees'))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败：{str(e)}', 'error')
    
    departments = Department.query.all()
    return render_template('employees/add.html', departments=departments)


@app.route('/employees/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_employee(id):
    """编辑员工"""
    employee = Employee.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            employee.employee_no = request.form.get('employee_no')
            employee.name = request.form.get('name')
            employee.gender = request.form.get('gender')
            employee.birth_date = datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date() if request.form.get('birth_date') else None
            employee.id_card = request.form.get('id_card')
            employee.phone = request.form.get('phone')
            employee.email = request.form.get('email')
            employee.address = request.form.get('address')
            employee.department_id = request.form.get('department_id')
            employee.position = request.form.get('position')
            employee.employment_type = request.form.get('employment_type')
            employee.hire_date = datetime.strptime(request.form.get('hire_date'), '%Y-%m-%d').date() if request.form.get('hire_date') else None
            employee.status = request.form.get('status')
            employee.education = request.form.get('education')
            employee.major = request.form.get('major')
            employee.graduate_school = request.form.get('graduate_school')
            employee.remarks = request.form.get('remarks')
            
            db.session.commit()
            flash('员工信息更新成功！', 'success')
            return redirect(url_for('employees'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败：{str(e)}', 'error')
    
    departments = Department.query.all()
    return render_template('employees/edit.html', employee=employee, departments=departments)


@app.route('/employees/<int:id>/delete', methods=['POST'])
@admin_required
def delete_employee(id):
    """删除员工"""
    employee = Employee.query.get_or_404(id)
    try:
        db.session.delete(employee)
        db.session.commit()
        flash('员工已删除', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败：{str(e)}', 'error')
    
    return redirect(url_for('employees'))


@app.route('/employees/<int:id>')
@login_required
def employee_detail(id):
    """员工详情"""
    employee = Employee.query.get_or_404(id)
    return render_template('employees/detail.html', employee=employee)


# ==================== 部门管理 ====================

@app.route('/departments')
@login_required
def departments():
    """部门列表"""
    departments = Department.query.order_by(Department.created_at.desc()).all()
    return render_template('departments/list.html', departments=departments)


@app.route('/departments/add', methods=['GET', 'POST'])
@admin_required
def add_department():
    """添加部门"""
    if request.method == 'POST':
        try:
            department = Department(
                name=request.form.get('name'),
                code=request.form.get('code'),
                description=request.form.get('description'),
                manager_id=request.form.get('manager_id') or None
            )
            
            db.session.add(department)
            db.session.commit()
            
            flash('部门添加成功！', 'success')
            return redirect(url_for('departments'))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败：{str(e)}', 'error')
    
    employees = Employee.query.filter_by(status='在职').all()
    return render_template('departments/add.html', employees=employees)


@app.route('/departments/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_department(id):
    """编辑部门"""
    department = Department.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            department.name = request.form.get('name')
            department.code = request.form.get('code')
            department.description = request.form.get('description')
            department.manager_id = request.form.get('manager_id') or None
            
            db.session.commit()
            flash('部门信息更新成功！', 'success')
            return redirect(url_for('departments'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败：{str(e)}', 'error')
    
    employees = Employee.query.filter_by(status='在职').all()
    return render_template('departments/edit.html', department=department, employees=employees)


@app.route('/departments/<int:id>/delete', methods=['POST'])
@admin_required
def delete_department(id):
    """删除部门"""
    department = Department.query.get_or_404(id)
    
    # 检查是否有员工
    if department.employees:
        flash('该部门下还有员工，无法删除', 'error')
        return redirect(url_for('departments'))
    
    try:
        db.session.delete(department)
        db.session.commit()
        flash('部门已删除', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败：{str(e)}', 'error')
    
    return redirect(url_for('departments'))


# ==================== 考勤管理 ====================

@app.route('/attendances')
@login_required
def attendances():
    """考勤列表"""
    page = request.args.get('page', 1, type=int)
    employee_id = request.args.get('employee_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Attendance.query
    
    # 筛选
    if employee_id:
        query = query.filter_by(employee_id=employee_id)
    if start_date:
        query = query.filter(Attendance.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Attendance.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    # 分页
    pagination = query.order_by(Attendance.date.desc()).paginate(
        page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False
    )
    
    employees = Employee.query.filter_by(status='在职').all()
    
    return render_template('attendances/list.html',
                         attendances=pagination.items,
                         pagination=pagination,
                         employees=employees,
                         employee_id=employee_id,
                         start_date=start_date,
                         end_date=end_date)


@app.route('/attendances/add', methods=['GET', 'POST'])
@admin_required
def add_attendance():
    """添加考勤记录"""
    if request.method == 'POST':
        try:
            attendance = Attendance(
                employee_id=request.form.get('employee_id'),
                date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date(),
                check_in_time=datetime.strptime(request.form.get('check_in_time'), '%H:%M').time() if request.form.get('check_in_time') else None,
                check_out_time=datetime.strptime(request.form.get('check_out_time'), '%H:%M').time() if request.form.get('check_out_time') else None,
                status=request.form.get('status'),
                leave_type=request.form.get('leave_type'),
                remarks=request.form.get('remarks')
            )
            
            db.session.add(attendance)
            db.session.commit()
            
            flash('考勤记录添加成功！', 'success')
            return redirect(url_for('attendances'))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败：{str(e)}', 'error')
    
    employees = Employee.query.filter_by(status='在职').all()
    return render_template('attendances/add.html', employees=employees)


@app.route('/attendances/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_attendance(id):
    """编辑考勤记录"""
    attendance = Attendance.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            attendance.employee_id = request.form.get('employee_id')
            attendance.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
            attendance.check_in_time = datetime.strptime(request.form.get('check_in_time'), '%H:%M').time() if request.form.get('check_in_time') else None
            attendance.check_out_time = datetime.strptime(request.form.get('check_out_time'), '%H:%M').time() if request.form.get('check_out_time') else None
            attendance.status = request.form.get('status')
            attendance.leave_type = request.form.get('leave_type')
            attendance.remarks = request.form.get('remarks')
            
            db.session.commit()
            flash('考勤记录更新成功！', 'success')
            return redirect(url_for('attendances'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败：{str(e)}', 'error')
    
    employees = Employee.query.filter_by(status='在职').all()
    return render_template('attendances/edit.html', attendance=attendance, employees=employees)


@app.route('/attendances/<int:id>/delete', methods=['POST'])
@admin_required
def delete_attendance(id):
    """删除考勤记录"""
    attendance = Attendance.query.get_or_404(id)
    try:
        db.session.delete(attendance)
        db.session.commit()
        flash('考勤记录已删除', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败：{str(e)}', 'error')
    
    return redirect(url_for('attendances'))


# ==================== 绩效考核 ====================

@app.route('/performances')
@login_required
def performances():
    """绩效考核列表"""
    page = request.args.get('page', 1, type=int)
    employee_id = request.args.get('employee_id', type=int)
    year = request.args.get('year', type=int)
    
    query = Performance.query
    
    # 筛选
    if employee_id:
        query = query.filter_by(employee_id=employee_id)
    if year:
        query = query.filter_by(year=year)
    
    # 分页
    pagination = query.order_by(Performance.year.desc(), Performance.quarter.desc()).paginate(
        page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False
    )
    
    employees = Employee.query.filter_by(status='在职').all()
    years = db.session.query(Performance.year).distinct().all()
    years = [y[0] for y in years] if years else []
    
    return render_template('performances/list.html',
                         performances=pagination.items,
                         pagination=pagination,
                         employees=employees,
                         years=years,
                         employee_id=employee_id,
                         selected_year=year)


@app.route('/performances/add', methods=['GET', 'POST'])
@admin_required
def add_performance():
    """添加绩效考核"""
    if request.method == 'POST':
        try:
            performance = Performance(
                employee_id=request.form.get('employee_id'),
                year=request.form.get('year'),
                quarter=request.form.get('quarter'),
                teaching_score=float(request.form.get('teaching_score', 0)),
                research_score=float(request.form.get('research_score', 0)),
                service_score=float(request.form.get('service_score', 0)),
                comments=request.form.get('comments'),
                evaluator=request.form.get('evaluator'),
                evaluation_date=datetime.strptime(request.form.get('evaluation_date'), '%Y-%m-%d').date() if request.form.get('evaluation_date') else None
            )
            
            # 计算总分和等级
            performance.calculate_total_score()
            
            db.session.add(performance)
            db.session.commit()
            
            flash('绩效考核添加成功！', 'success')
            return redirect(url_for('performances'))
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败：{str(e)}', 'error')
    
    employees = Employee.query.filter_by(status='在职').all()
    return render_template('performances/add.html', employees=employees)


@app.route('/performances/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_performance(id):
    """编辑绩效考核"""
    performance = Performance.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            performance.employee_id = request.form.get('employee_id')
            performance.year = request.form.get('year')
            performance.quarter = request.form.get('quarter')
            performance.teaching_score = float(request.form.get('teaching_score', 0))
            performance.research_score = float(request.form.get('research_score', 0))
            performance.service_score = float(request.form.get('service_score', 0))
            performance.comments = request.form.get('comments')
            performance.evaluator = request.form.get('evaluator')
            performance.evaluation_date = datetime.strptime(request.form.get('evaluation_date'), '%Y-%m-%d').date() if request.form.get('evaluation_date') else None
            
            # 计算总分和等级
            performance.calculate_total_score()
            
            db.session.commit()
            flash('绩效考核更新成功！', 'success')
            return redirect(url_for('performances'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败：{str(e)}', 'error')
    
    employees = Employee.query.filter_by(status='在职').all()
    return render_template('performances/edit.html', performance=performance, employees=employees)


@app.route('/performances/<int:id>/delete', methods=['POST'])
@admin_required
def delete_performance(id):
    """删除绩效考核"""
    performance = Performance.query.get_or_404(id)
    try:
        db.session.delete(performance)
        db.session.commit()
        flash('绩效考核已删除', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败：{str(e)}', 'error')
    
    return redirect(url_for('performances'))


# 导入额外路由
from app_routes import (
    register_title_routes, 
    register_training_routes, 
    register_export_routes,
    register_import_routes,
    register_statistics_routes
)

# 注册路由
register_title_routes(app, admin_required)
register_training_routes(app, admin_required)
register_export_routes(app)
register_import_routes(app, admin_required)
register_statistics_routes(app)


# 初始化数据库和创建管理员账户
def init_database():
    """初始化数据库"""
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 检查是否已有管理员账户
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', role='admin')
            admin.set_password('admin123')  # 默认密码
            db.session.add(admin)
            db.session.commit()
            print('管理员账户已创建：用户名 admin，密码 admin123')
        
        print('数据库初始化完成！')


# ==================== 统计图表API ====================

@app.route('/api/gender-stats')
@login_required
def gender_stats():
    """员工性别分布统计"""
    try:
        stats = db.session.query(
            Employee.gender,
            func.count(Employee.id).label('count')
        ).filter_by(status='在职').group_by(Employee.gender).all()
        
        labels = []
        values = []
        for gender, count in stats:
            labels.append(gender or '未填写')
            values.append(count)
        
        return jsonify({
            'labels': labels,
            'values': values
        })
    except Exception as e:
        return jsonify({'labels': [], 'values': [], 'error': str(e)})


@app.route('/api/department-stats')
@login_required
def department_stats():
    """部门人数分布统计"""
    try:
        stats = db.session.query(
            Department.name,
            func.count(Employee.id).label('count')
        ).outerjoin(Employee, Department.id == Employee.department_id)\
         .filter(Employee.status == '在职')\
         .group_by(Department.name).all()
        
        labels = []
        values = []
        for dept_name, count in stats:
            if count > 0:  # 只显示有员工的部门
                labels.append(dept_name)
                values.append(count)
        
        return jsonify({
            'labels': labels,
            'values': values
        })
    except Exception as e:
        return jsonify({'labels': [], 'values': [], 'error': str(e)})


@app.route('/api/attendance-stats')
@login_required
def attendance_stats():
    """近7天考勤趋势统计"""
    try:
        today = date.today()
        labels = []
        values = []
        
        for i in range(6, -1, -1):  # 近7天
            check_date = today - timedelta(days=i)
            count = Attendance.query.filter_by(date=check_date).count()
            labels.append(check_date.strftime('%m-%d'))
            values.append(count)
        
        return jsonify({
            'labels': labels,
            'values': values
        })
    except Exception as e:
        return jsonify({'labels': [], 'values': [], 'error': str(e)})


@app.route('/api/performance-stats')
@login_required
def performance_stats():
    """绩效分布统计"""
    try:
        stats = db.session.query(
            Performance.rating,
            func.count(Performance.id).label('count')
        ).group_by(Performance.rating).all()
        
        labels = []
        values = []
        for rating, count in stats:
            labels.append(rating or '未评级')
            values.append(count)
        
        return jsonify({
            'labels': labels,
            'values': values
        })
    except Exception as e:
        return jsonify({'labels': [], 'values': [], 'error': str(e)})


# 主程序入口
if __name__ == '__main__':
    # 初始化数据库
    init_database()
    
    # 运行应用
    app.run(debug=True, host='0.0.0.0', port=5000)
