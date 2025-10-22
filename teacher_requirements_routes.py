# 老师要求的新功能路由
# 功能1：职称材料上传与审核
# 功能2：学院差异化绩效考核

from flask import request, redirect, url_for, flash, render_template, jsonify, send_from_directory
from flask_login import login_required, current_user
from models import db, Title, Employee, College, EvaluationStandard, Performance, PerformanceDetail, User
from datetime import datetime
from werkzeug.utils import secure_filename
import os


def register_teacher_requirements_routes(app, admin_required):
    """注册老师要求的新功能路由"""
    
    # ==================== 功能1：职称材料上传与审核 ====================
    
    @app.route('/titles/<int:id>/upload', methods=['GET', 'POST'])
    @admin_required
    def upload_title_materials(id):
        """上传职称申请材料"""
        title = Title.query.get_or_404(id)
        
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('请选择文件', 'error')
                return redirect(request.url)
            
            file = request.files['file']
            if file.filename == '':
                flash('请选择文件', 'error')
                return redirect(request.url)
            
            # 检查文件类型
            allowed_extensions = {'pdf', 'doc', 'docx', 'zip', 'rar'}
            if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                try:
                    # 确保上传目录存在
                    upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'title_materials')
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder, exist_ok=True)
                    
                    # 生成安全的文件名
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{title.employee_id}_{timestamp}_{filename}"
                    file_path = os.path.join(upload_folder, filename)
                    
                    # 保存文件
                    file.save(file_path)
                    
                    # 更新数据库
                    title.attachment_filename = file.filename
                    title.attachment_path = file_path
                    title.attachment_upload_time = datetime.now()
                    title.is_notified = False  # 重置通知状态
                    
                    db.session.commit()
                    
                    flash('材料上传成功！', 'success')
                    return redirect(url_for('titles'))
                    
                except Exception as e:
                    db.session.rollback()
                    flash(f'上传失败：{str(e)}', 'error')
            else:
                flash('只支持 PDF、Word、ZIP、RAR 格式的文件', 'error')
        
        return render_template('titles/upload.html', title=title)
    
    
    @app.route('/titles/<int:id>/review', methods=['GET', 'POST'])
    @admin_required
    def review_title(id):
        """审核职称申请"""
        title = Title.query.get_or_404(id)
        
        if request.method == 'POST':
            try:
                result = request.form.get('result')  # '已通过' 或 '未通过'
                comments = request.form.get('comments')
                
                title.status = result
                title.reviewer_id = current_user.id
                title.review_date = datetime.now()
                title.review_comments = comments
                title.is_notified = False  # 标记需要通知
                
                if result == '已通过':
                    title.approval_date = datetime.now().date()
                    title.certificate_no = request.form.get('certificate_no')
                
                db.session.commit()
                
                flash(f'审核完成！状态：{result}', 'success')
                return redirect(url_for('titles'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'审核失败：{str(e)}', 'error')
        
        return render_template('titles/review.html', title=title)
    
    
    @app.route('/titles/<int:id>/download')
    @login_required
    def download_title_material(id):
        """下载职称申请材料"""
        title = Title.query.get_or_404(id)
        
        if not title.attachment_path or not os.path.exists(title.attachment_path):
            flash('文件不存在', 'error')
            return redirect(url_for('titles'))
        
        try:
            directory = os.path.dirname(title.attachment_path)
            filename = os.path.basename(title.attachment_path)
            return send_from_directory(directory, filename, as_attachment=True, 
                                      download_name=title.attachment_filename)
        except Exception as e:
            flash(f'下载失败：{str(e)}', 'error')
            return redirect(url_for('titles'))
    
    
    @app.route('/api/check-notifications')
    @login_required
    def check_notifications():
        """检查是否有待通知的职称审核结果"""
        if current_user.role != 'admin':
            # 查询当前用户相关员工的未通知审核结果
            employee = Employee.query.filter_by(email=current_user.username).first()
            if employee:
                unnotified = Title.query.filter_by(
                    employee_id=employee.id,
                    is_notified=False
                ).filter(Title.status.in_(['已通过', '未通过'])).all()
                
                notifications = []
                for title in unnotified:
                    notifications.append({
                        'id': title.id,
                        'title_name': title.title_name,
                        'status': title.status,
                        'review_comments': title.review_comments,
                        'review_date': title.review_date.strftime('%Y-%m-%d %H:%M') if title.review_date else ''
                    })
                    # 标记为已通知
                    title.is_notified = True
                
                db.session.commit()
                return jsonify({'notifications': notifications})
        
        return jsonify({'notifications': []})
    
    
    # ==================== 功能2：学院管理 ====================
    
    @app.route('/colleges')
    @admin_required
    def colleges():
        """学院列表"""
        colleges_list = College.query.order_by(College.created_at.desc()).all()
        return render_template('colleges/list.html', colleges=colleges_list)
    
    
    @app.route('/colleges/add', methods=['GET', 'POST'])
    @admin_required
    def add_college():
        """添加学院"""
        if request.method == 'POST':
            try:
                college = College(
                    name=request.form.get('name'),
                    code=request.form.get('code'),
                    dean=request.form.get('dean'),
                    description=request.form.get('description')
                )
                
                db.session.add(college)
                db.session.commit()
                
                flash('学院添加成功！', 'success')
                return redirect(url_for('colleges'))
            except Exception as e:
                db.session.rollback()
                flash(f'添加失败：{str(e)}', 'error')
        
        return render_template('colleges/add.html')
    
    
    @app.route('/colleges/<int:id>/standards')
    @admin_required
    def college_standards(id):
        """学院考核标准管理"""
        college = College.query.get_or_404(id)
        standards = EvaluationStandard.query.filter_by(college_id=id, is_active=True).all()
        return render_template('colleges/standards.html', college=college, standards=standards)
    
    
    @app.route('/colleges/<int:id>/standards/add', methods=['GET', 'POST'])
    @admin_required
    def add_evaluation_standard(id):
        """添加考核标准"""
        college = College.query.get_or_404(id)
        
        if request.method == 'POST':
            try:
                standard = EvaluationStandard(
                    college_id=id,
                    item_name=request.form.get('item_name'),
                    item_type=request.form.get('item_type'),
                    weight=float(request.form.get('weight', 1.0)),
                    grade_a_score=float(request.form.get('grade_a_score', 100)),
                    grade_b_score=float(request.form.get('grade_b_score', 85)),
                    grade_c_score=float(request.form.get('grade_c_score', 75)),
                    grade_d_score=float(request.form.get('grade_d_score', 65)),
                    description=request.form.get('description')
                )
                
                db.session.add(standard)
                db.session.commit()
                
                flash('考核标准添加成功！', 'success')
                return redirect(url_for('college_standards', id=id))
            except Exception as e:
                db.session.rollback()
                flash(f'添加失败：{str(e)}', 'error')
        
        return render_template('colleges/add_standard.html', college=college)
    
    
    # ==================== 功能3：按学院绩效考核 ====================
    
    @app.route('/performances/advanced/add', methods=['GET', 'POST'])
    @admin_required
    def add_advanced_performance():
        """添加高级绩效考核（按学院标准）"""
        if request.method == 'POST':
            try:
                employee_id = request.form.get('employee_id')
                employee = Employee.query.get(employee_id)
                
                if not employee or not employee.department or not employee.department.college_id:
                    flash('员工未分配学院，无法使用学院标准考核', 'error')
                    return redirect(request.url)
                
                # 创建绩效记录
                performance = Performance(
                    employee_id=employee_id,
                    year=int(request.form.get('year')),
                    quarter=int(request.form.get('quarter')),
                    evaluator=request.form.get('evaluator'),
                    evaluation_date=datetime.now().date()
                )
                
                db.session.add(performance)
                db.session.flush()  # 获取performance.id
                
                # 获取该学院的考核标准
                college_id = employee.department.college_id
                standards = EvaluationStandard.query.filter_by(
                    college_id=college_id, 
                    is_active=True
                ).all()
                
                total_score = 0
                total_weight = 0
                
                # 为每个标准项添加评分
                for standard in standards:
                    grade = request.form.get(f'grade_{standard.id}')
                    if grade:
                        # 根据等级计算分数
                        if grade == 'A':
                            score = standard.grade_a_score
                        elif grade == 'B':
                            score = standard.grade_b_score
                        elif grade == 'C':
                            score = standard.grade_c_score
                        elif grade == 'D':
                            score = standard.grade_d_score
                        else:
                            score = 0
                        
                        # 保存详情
                        detail = PerformanceDetail(
                            performance_id=performance.id,
                            standard_id=standard.id,
                            grade=grade,
                            score=score * standard.weight,
                            comments=request.form.get(f'comments_{standard.id}')
                        )
                        db.session.add(detail)
                        
                        total_score += score * standard.weight
                        total_weight += standard.weight
                
                # 计算加权平均分
                if total_weight > 0:
                    performance.total_score = total_score / total_weight
                else:
                    performance.total_score = 0
                
                # 自动评级
                if performance.total_score >= 90:
                    performance.rating = '优秀'
                elif performance.total_score >= 80:
                    performance.rating = '良好'
                elif performance.total_score >= 60:
                    performance.rating = '合格'
                else:
                    performance.rating = '不合格'
                
                db.session.commit()
                
                flash('绩效考核添加成功！', 'success')
                return redirect(url_for('performances'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'添加失败：{str(e)}', 'error')
        
        employees = Employee.query.filter_by(status='在职').all()
        colleges_list = College.query.all()
        
        return render_template('performances/advanced_add.html', 
                             employees=employees,
                             colleges=colleges_list)
    
    
    @app.route('/api/college-standards/<int:college_id>')
    @admin_required
    def get_college_standards(college_id):
        """获取学院考核标准（API）"""
        standards = EvaluationStandard.query.filter_by(
            college_id=college_id,
            is_active=True
        ).all()
        
        result = []
        for std in standards:
            result.append({
                'id': std.id,
                'item_name': std.item_name,
                'item_type': std.item_type,
                'weight': std.weight,
                'description': std.description
            })
        
        return jsonify({'standards': result})
