#!/usr/bin/env python3
"""自动生成测试数据 - 一键恢复所有测试用例"""

from app import app, db
from models import User, Employee, Department, Attendance, Performance, Title, Training, College
from datetime import datetime, date, timedelta
import random

print("="*60)
print("  开始生成测试数据")
print("="*60)

with app.app_context():
    # 1. 获取学院数据
    colleges = {c.code: c for c in College.query.all()}
    
    if not colleges:
        print("❌ 错误：请先运行 python init_colleges.py 初始化学院数据")
        exit(1)
    
    print(f"\n✅ 已加载 {len(colleges)} 个学院")
    
    # 2. 创建用户账号
    print("\n📝 创建用户账号...")
    users_data = [
        {'username': 'teacher1', 'password': '123456', 'role': 'user'},
        {'username': 'teacher2', 'password': '123456', 'role': 'user'},
        {'username': 'teacher3', 'password': '123456', 'role': 'user'},
        {'username': 'hr_admin', 'password': '123456', 'role': 'admin'},
    ]
    
    for user_data in users_data:
        if not User.query.filter_by(username=user_data['username']).first():
            user = User(username=user_data['username'], role=user_data['role'])
            user.set_password(user_data['password'])
            db.session.add(user)
            print(f"  创建用户：{user_data['username']} ({user_data['role']})")
    
    db.session.commit()
    
    # 3. 创建部门
    print("\n🏢 创建部门...")
    departments_data = [
        {'name': '中文系', 'code': 'ZW', 'college_id': colleges['WXY'].id, 'description': '负责中国语言文学教学'},
        {'name': '外语系', 'code': 'WY', 'college_id': colleges['WXY'].id, 'description': '负责外国语言文学教学'},
        {'name': '教育系', 'code': 'JY', 'college_id': colleges['JYX'].id, 'description': '负责教育学教学'},
        {'name': '心理系', 'code': 'XL', 'college_id': colleges['JYX'].id, 'description': '负责心理学教学'},
        {'name': '计算机科学系', 'code': 'JSJ', 'college_id': colleges['JSJ'].id, 'description': '负责计算机科学教学'},
        {'name': '软件工程系', 'code': 'RJ', 'college_id': colleges['JSJ'].id, 'description': '负责软件工程教学'},
        {'name': '数学系', 'code': 'SX', 'college_id': colleges['SXX'].id, 'description': '负责数学教学'},
        {'name': '统计系', 'code': 'TJ', 'college_id': colleges['SXX'].id, 'description': '负责统计学教学'},
    ]
    
    created_depts = {}
    for dept_data in departments_data:
        dept = Department.query.filter_by(code=dept_data['code']).first()
        if not dept:
            dept = Department(**dept_data)
            db.session.add(dept)
            college_name = College.query.get(dept_data['college_id']).name
            print(f"  创建部门：{dept_data['name']} ({dept_data['code']}) -> {college_name}")
        created_depts[dept_data['code']] = dept
    
    db.session.commit()
    
    # 刷新部门对象以获取ID
    for code in created_depts:
        created_depts[code] = Department.query.filter_by(code=code).first()
    
    # 4. 创建员工
    print("\n👥 创建员工...")
    employees_data = [
        # 文学院
        {'employee_no': 'T2024001', 'name': '张晓明', 'gender': '男', 'birth_date': '1985-03-15',
         'phone': '13800138001', 'email': 'teacher1', 'department_code': 'ZW',
         'position': '副教授', 'employment_type': '全职', 'hire_date': '2015-09-01',
         'education': '博士', 'major': '中国古代文学', 'graduate_school': '北京大学'},
        
        {'employee_no': 'T2024002', 'name': '李芳', 'gender': '女', 'birth_date': '1988-07-20',
         'phone': '13800138002', 'email': 'teacher2', 'department_code': 'WY',
         'position': '讲师', 'employment_type': '全职', 'hire_date': '2018-09-01',
         'education': '博士', 'major': '英语语言文学', 'graduate_school': '复旦大学'},
        
        # 教育学院
        {'employee_no': 'T2024003', 'name': '王建国', 'gender': '男', 'birth_date': '1982-11-10',
         'phone': '13800138003', 'email': 'wjg@example.com', 'department_code': 'JY',
         'position': '教授', 'employment_type': '全职', 'hire_date': '2012-09-01',
         'education': '博士', 'major': '教育学原理', 'graduate_school': '华东师范大学'},
        
        {'employee_no': 'T2024004', 'name': '赵敏', 'gender': '女', 'birth_date': '1990-05-08',
         'phone': '13800138004', 'email': 'zm@example.com', 'department_code': 'XL',
         'position': '讲师', 'employment_type': '全职', 'hire_date': '2019-09-01',
         'education': '博士', 'major': '发展心理学', 'graduate_school': '北京师范大学'},
        
        # 计算机学院
        {'employee_no': 'T2024005', 'name': '刘伟', 'gender': '男', 'birth_date': '1986-09-25',
         'phone': '13800138005', 'email': 'teacher3', 'department_code': 'JSJ',
         'position': '副教授', 'employment_type': '全职', 'hire_date': '2016-09-01',
         'education': '博士', 'major': '计算机科学与技术', 'graduate_school': '清华大学'},
        
        {'employee_no': 'T2024006', 'name': '陈静', 'gender': '女', 'birth_date': '1992-02-14',
         'phone': '13800138006', 'email': 'cj@example.com', 'department_code': 'RJ',
         'position': '讲师', 'employment_type': '全职', 'hire_date': '2020-09-01',
         'education': '博士', 'major': '软件工程', 'graduate_school': '浙江大学'},
        
        # 数学学院
        {'employee_no': 'T2024007', 'name': '孙强', 'gender': '男', 'birth_date': '1984-12-03',
         'phone': '13800138007', 'email': 'sq@example.com', 'department_code': 'SX',
         'position': '教授', 'employment_type': '全职', 'hire_date': '2014-09-01',
         'education': '博士', 'major': '基础数学', 'graduate_school': '中国科学技术大学'},
        
        {'employee_no': 'T2024008', 'name': '周丽', 'gender': '女', 'birth_date': '1991-08-18',
         'phone': '13800138008', 'email': 'zl@example.com', 'department_code': 'TJ',
         'position': '讲师', 'employment_type': '全职', 'hire_date': '2021-09-01',
         'education': '博士', 'major': '统计学', 'graduate_school': '南开大学'},
    ]
    
    created_employees = {}
    for emp_data in employees_data:
        emp = Employee.query.filter_by(employee_no=emp_data['employee_no']).first()
        if not emp:
            dept_code = emp_data.pop('department_code')
            emp_data['department_id'] = created_depts[dept_code].id
            emp_data['birth_date'] = datetime.strptime(emp_data['birth_date'], '%Y-%m-%d').date()
            emp_data['hire_date'] = datetime.strptime(emp_data['hire_date'], '%Y-%m-%d').date()
            emp = Employee(**emp_data)
            db.session.add(emp)
            print(f"  创建员工：{emp.name} ({emp.employee_no}) - {emp.position}")
        created_employees[emp_data['employee_no']] = emp
    
    db.session.commit()
    
    # 刷新员工对象以获取ID
    for no in created_employees:
        created_employees[no] = Employee.query.filter_by(employee_no=no).first()
    
    # 5. 创建职称申请
    print("\n🎓 创建职称申请...")
    titles_data = [
        {'employee_no': 'T2024001', 'title_name': '教授', 'title_level': '高级',
         'application_date': '2024-03-01', 'status': '待审核'},
        
        {'employee_no': 'T2024002', 'title_name': '副教授', 'title_level': '中级',
         'application_date': '2024-04-15', 'status': '待审核'},
        
        {'employee_no': 'T2024005', 'title_name': '教授', 'title_level': '高级',
         'application_date': '2024-05-10', 'status': '待审核',
         'remarks': '算法研究方向，已发表CCF A类论文3篇'},
        
        {'employee_no': 'T2024007', 'title_name': '教授', 'title_level': '高级',
         'application_date': '2024-02-20', 'status': '已通过',
         'approval_date': '2024-06-01', 'certificate_no': 'PROF-2024-001'},
    ]
    
    for title_data in titles_data:
        emp_no = title_data.pop('employee_no')
        employee = created_employees.get(emp_no)
        if employee:
            title_data['employee_id'] = employee.id
            title_data['application_date'] = datetime.strptime(title_data['application_date'], '%Y-%m-%d').date()
            if 'approval_date' in title_data:
                title_data['approval_date'] = datetime.strptime(title_data['approval_date'], '%Y-%m-%d').date()
            
            title = Title(**title_data)
            db.session.add(title)
            print(f"  创建职称申请：{employee.name} 申请 {title.title_name} ({title.status})")
    
    db.session.commit()
    
    # 6. 创建考勤记录
    print("\n📅 创建考勤记录...")
    today = date.today()
    attendance_count = 0
    
    for emp_no, employee in created_employees.items():
        # 为每个员工创建最近7天的考勤记录
        for i in range(7):
            check_date = today - timedelta(days=i)
            if check_date.weekday() < 5:  # 工作日
                status = random.choice(['正常', '正常', '正常', '迟到', '早退'])
                check_in = '09:00' if status == '正常' else '09:15'
                check_out = '17:00' if status != '早退' else '16:30'
                
                attendance = Attendance(
                    employee_id=employee.id,
                    date=check_date,
                    check_in_time=datetime.strptime(check_in, '%H:%M').time(),
                    check_out_time=datetime.strptime(check_out, '%H:%M').time(),
                    status=status
                )
                db.session.add(attendance)
                attendance_count += 1
    
    print(f"  创建 {attendance_count} 条考勤记录")
    db.session.commit()
    
    # 7. 创建绩效考核记录
    print("\n📊 创建绩效考核记录...")
    performances_data = [
        {'employee_no': 'T2024001', 'year': 2023, 'quarter': 4,
         'teaching_score': 90, 'research_score': 85, 'service_score': 88,
         'evaluator': '院长', 'evaluation_date': '2024-01-15'},
        
        {'employee_no': 'T2024005', 'year': 2023, 'quarter': 4,
         'teaching_score': 88, 'research_score': 95, 'service_score': 85,
         'evaluator': '院长', 'evaluation_date': '2024-01-15',
         'comments': '算法研究成果突出'},
        
        {'employee_no': 'T2024007', 'year': 2023, 'quarter': 4,
         'teaching_score': 92, 'research_score': 90, 'service_score': 87,
         'evaluator': '院长', 'evaluation_date': '2024-01-15'},
    ]
    
    for perf_data in performances_data:
        emp_no = perf_data.pop('employee_no')
        employee = created_employees.get(emp_no)
        if employee:
            perf_data['employee_id'] = employee.id
            perf_data['evaluation_date'] = datetime.strptime(perf_data['evaluation_date'], '%Y-%m-%d').date()
            
            performance = Performance(**perf_data)
            performance.calculate_total_score()
            db.session.add(performance)
            print(f"  创建绩效考核：{employee.name} {perf_data['year']}年Q{perf_data['quarter']} - {performance.rating}")
    
    db.session.commit()
    
    # 8. 创建培训记录
    print("\n📚 创建培训记录...")
    trainings_data = [
        {'employee_no': 'T2024002', 'training_name': '外语教学法研讨会',
         'training_type': '外部培训', 'start_date': '2024-06-01', 'end_date': '2024-06-03',
         'duration_hours': 24, 'location': '上海', 'instructor': '专家团队',
         'cost': 3000, 'status': '已完成', 'completion_status': '优秀'},
        
        {'employee_no': 'T2024005', 'training_name': '人工智能与算法前沿',
         'training_type': '外部培训', 'start_date': '2024-07-10', 'end_date': '2024-07-15',
         'duration_hours': 40, 'location': '北京', 'instructor': '清华大学',
         'cost': 5000, 'status': '已完成', 'completion_status': '优秀'},
        
        {'employee_no': 'T2024006', 'training_name': '软件工程实践',
         'training_type': '在线培训', 'start_date': '2024-08-01', 'end_date': '2024-08-31',
         'duration_hours': 20, 'location': '线上', 'instructor': '在线平台',
         'cost': 500, 'status': '进行中'},
    ]
    
    for train_data in trainings_data:
        emp_no = train_data.pop('employee_no')
        employee = created_employees.get(emp_no)
        if employee:
            train_data['employee_id'] = employee.id
            train_data['start_date'] = datetime.strptime(train_data['start_date'], '%Y-%m-%d').date()
            train_data['end_date'] = datetime.strptime(train_data['end_date'], '%Y-%m-%d').date()
            
            training = Training(**train_data)
            db.session.add(training)
            print(f"  创建培训记录：{employee.name} - {train_data['training_name']}")
    
    db.session.commit()

print("\n" + "="*60)
print("  ✅ 测试数据生成完成！")
print("="*60)

# 统计信息
with app.app_context():
    print("\n📊 数据统计：")
    print(f"  👥 员工：{Employee.query.count()} 人")
    print(f"  🏢 部门：{Department.query.count()} 个")
    print(f"  🏫 学院：{College.query.count()} 个")
    print(f"  🎓 职称申请：{Title.query.count()} 条")
    print(f"  📅 考勤记录：{Attendance.query.count()} 条")
    print(f"  📊 绩效考核：{Performance.query.count()} 条")
    print(f"  📚 培训记录：{Training.query.count()} 条")
    print(f"  👤 用户账号：{User.query.count()} 个")

print("\n🎉 可以开始测试了！")
print("\n登录账号：")
print("  管理员：admin / admin123")
print("  教师1：teacher1 / 123456")
print("  教师2：teacher2 / 123456")
print("  教师3：teacher3 / 123456")
print("  HR管理：hr_admin / 123456")
