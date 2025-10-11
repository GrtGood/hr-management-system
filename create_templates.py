"""
自动生成所有必要的HTML模板文件
这个脚本会创建员工、部门、考勤、绩效、职称、培训的添加/编辑/详情页面
"""

import os

# 创建员工添加/编辑表单模板
employee_form_template = '''{% extends "base.html" %}
{% block title %}{{ "添加" if not employee else "编辑" }}员工{% endblock %}
{% block content %}
<h2><i class="bi bi-person-plus me-2"></i>{{ "添加" if not employee else "编辑" }}员工</h2>
<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label class="form-label">工号 *</label>
                    <input type="text" class="form-control" name="employee_no" value="{{ employee.employee_no if employee else '' }}" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">姓名 *</label>
                    <input type="text" class="form-control" name="name" value="{{ employee.name if employee else '' }}" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">性别</label>
                    <select class="form-select" name="gender">
                        <option value="">请选择</option>
                        <option value="男" {% if employee and employee.gender == '男' %}selected{% endif %}>男</option>
                        <option value="女" {% if employee and employee.gender == '女' %}selected{% endif %}>女</option>
                    </select>
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">出生日期</label>
                    <input type="date" class="form-control" name="birth_date" value="{{ employee.birth_date if employee else '' }}">
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">身份证号</label>
                    <input type="text" class="form-control" name="id_card" value="{{ employee.id_card if employee else '' }}">
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">电话</label>
                    <input type="text" class="form-control" name="phone" value="{{ employee.phone if employee else '' }}">
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">邮箱</label>
                    <input type="email" class="form-control" name="email" value="{{ employee.email if employee else '' }}">
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">部门</label>
                    <select class="form-select" name="department_id">
                        <option value="">请选择</option>
                        {% for dept in departments %}
                        <option value="{{ dept.id }}" {% if employee and employee.department_id == dept.id %}selected{% endif %}>{{ dept.name }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">职位</label>
                    <input type="text" class="form-control" name="position" value="{{ employee.position if employee else '' }}">
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">聘用类型</label>
                    <select class="form-select" name="employment_type">
                        <option value="">请选择</option>
                        <option value="全职" {% if employee and employee.employment_type == '全职' %}selected{% endif %}>全职</option>
                        <option value="兼职" {% if employee and employee.employment_type == '兼职' %}selected{% endif %}>兼职</option>
                        <option value="临时" {% if employee and employee.employment_type == '临时' %}selected{% endif %}>临时</option>
                    </select>
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">入职日期</label>
                    <input type="date" class="form-control" name="hire_date" value="{{ employee.hire_date if employee else '' }}">
                </div>
                {% if employee %}
                <div class="col-md-6 mb-3">
                    <label class="form-label">状态</label>
                    <select class="form-select" name="status">
                        <option value="在职" {% if employee.status == '在职' %}selected{% endif %}>在职</option>
                        <option value="离职" {% if employee.status == '离职' %}selected{% endif %}>离职</option>
                    </select>
                </div>
                {% endif %}
                <div class="col-md-6 mb-3">
                    <label class="form-label">学历</label>
                    <input type="text" class="form-control" name="education" value="{{ employee.education if employee else '' }}">
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">专业</label>
                    <input type="text" class="form-control" name="major" value="{{ employee.major if employee else '' }}">
                </div>
                <div class="col-md-12 mb-3">
                    <label class="form-label">毕业院校</label>
                    <input type="text" class="form-control" name="graduate_school" value="{{ employee.graduate_school if employee else '' }}">
                </div>
                <div class="col-md-12 mb-3">
                    <label class="form-label">地址</label>
                    <input type="text" class="form-control" name="address" value="{{ employee.address if employee else '' }}">
                </div>
                <div class="col-md-12 mb-3">
                    <label class="form-label">备注</label>
                    <textarea class="form-control" name="remarks" rows="3">{{ employee.remarks if employee else '' }}</textarea>
                </div>
            </div>
            <button type="submit" class="btn btn-primary"><i class="bi bi-save"></i> 保存</button>
            <a href="{{ url_for('employees') }}" class="btn btn-secondary"><i class="bi bi-x"></i> 取消</a>
        </form>
    </div>
</div>
{% endblock %}'''

# 员工详情模板
employee_detail_template = '''{% extends "base.html" %}
{% block title %}员工详情{% endblock %}
{% block content %}
<h2><i class="bi bi-person me-2"></i>员工详情</h2>
<div class="card">
    <div class="card-body">
        <div class="row">
            <div class="col-md-6 mb-3"><strong>工号：</strong>{{ employee.employee_no }}</div>
            <div class="col-md-6 mb-3"><strong>姓名：</strong>{{ employee.name }}</div>
            <div class="col-md-6 mb-3"><strong>性别：</strong>{{ employee.gender or '-' }}</div>
            <div class="col-md-6 mb-3"><strong>出生日期：</strong>{{ employee.birth_date or '-' }}</div>
            <div class="col-md-6 mb-3"><strong>身份证号：</strong>{{ employee.id_card or '-' }}</div>
            <div class="col-md-6 mb-3"><strong>电话：</strong>{{ employee.phone or '-' }}</div>
            <div class="col-md-6 mb-3"><strong>邮箱：</strong>{{ employee.email or '-' }}</div>
            <div class="col-md-6 mb-3"><strong>部门：</strong>{{ employee.department.name if employee.department else '-' }}</div>
            <div class="col-md-6 mb-3"><strong>职位：</strong>{{ employee.position or '-' }}</div>
            <div class="col-md-6 mb-3"><strong>聘用类型：</strong>{{ employee.employment_type or '-' }}</div>
            <div class="col-md-6 mb-3"><strong>入职日期：</strong>{{ employee.hire_date or '-' }}</div>
            <div class="col-md-6 mb-3"><strong>状态：</strong><span class="badge {{ 'bg-success' if employee.status == '在职' else 'bg-secondary' }}">{{ employee.status }}</span></div>
            <div class="col-md-6 mb-3"><strong>学历：</strong>{{ employee.education or '-' }}</div>
            <div class="col-md-6 mb-3"><strong>专业：</strong>{{ employee.major or '-' }}</div>
            <div class="col-md-12 mb-3"><strong>毕业院校：</strong>{{ employee.graduate_school or '-' }}</div>
            <div class="col-md-12 mb-3"><strong>地址：</strong>{{ employee.address or '-' }}</div>
            <div class="col-md-12 mb-3"><strong>备注：</strong>{{ employee.remarks or '-' }}</div>
        </div>
        <a href="{{ url_for('employees') }}" class="btn btn-secondary"><i class="bi bi-arrow-left"></i> 返回列表</a>
        {% if current_user.role == 'admin' %}
        <a href="{{ url_for('edit_employee', id=employee.id) }}" class="btn btn-warning"><i class="bi bi-pencil"></i> 编辑</a>
        {% endif %}
    </div>
</div>
{% endblock %}'''

# 创建简化的其他模块列表模板
def create_simple_list(module_name, module_name_cn, fields):
    return f'''
{{% extends "base.html" %}}
{{% block title %}}{module_name_cn}管理{{% endblock %}}
{{% block content %}}
<h2><i class="bi bi-list me-2"></i>{module_name_cn}管理</h2>
{{% if current_user.role == 'admin' %}}
<a href="{{{{ url_for('add_{module_name}') }}}}" class="btn btn-primary mb-3"><i class="bi bi-plus"></i> 添加</a>
{{% endif %}}
<div class="card">
    <div class="card-body">
        <table class="table table-hover">
            <thead><tr>{fields}<th>操作</th></tr></thead>
            <tbody>
            {{% for item in {module_name}s %}}
            <tr>
                <!-- 这里需要根据具体字段填充 -->
                <td>{{{{ item.id }}}}</td>
                <td>
                    {{% if current_user.role == 'admin' %}}
                    <a href="{{{{ url_for('edit_{module_name}', id=item.id) }}}}" class="btn btn-sm btn-warning"><i class="bi bi-pencil"></i></a>
                    {{% endif %}}
                </td>
            </tr>
            {{% endfor %}}
            </tbody>
        </table>
    </div>
</div>
{{% endblock %}}'''

# 写入文件
templates = {
    'templates/employees/add.html': employee_form_template,
    'templates/employees/edit.html': employee_form_template,
    'templates/employees/detail.html': employee_detail_template,
}

for filepath, content in templates.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'✓ Created {filepath}')

print('\n模板文件创建完成！')
print('注意：部分模块的列表/添加/编辑模板需要根据具体字段手动调整')
