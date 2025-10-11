#!/bin/bash
# 批量生成所有必要的简化模板文件

# 创建部门添加/编辑模板
cat > templates/departments/add.html << 'EOF'
{% extends "base.html" %}
{% block title %}{{ "添加" if not department else "编辑" }}部门{% endblock %}
{% block content %}
<h2>{{ "添加" if not department else "编辑" }}部门</h2>
<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="mb-3">
                <label class="form-label">部门代码 *</label>
                <input type="text" class="form-control" name="code" value="{{ department.code if department else '' }}" required>
            </div>
            <div class="mb-3">
                <label class="form-label">部门名称 *</label>
                <input type="text" class="form-control" name="name" value="{{ department.name if department else '' }}" required>
            </div>
            <div class="mb-3">
                <label class="form-label">描述</label>
                <textarea class="form-control" name="description" rows="3">{{ department.description if department else '' }}</textarea>
            </div>
            <div class="mb-3">
                <label class="form-label">负责人</label>
                <select class="form-select" name="manager_id">
                    <option value="">请选择</option>
                    {% for emp in employees %}
                    <option value="{{ emp.id }}" {% if department and department.manager_id == emp.id %}selected{% endif %}>{{ emp.name }}</option>
                    {% endfor %}
                </select>
            </div>
            <button type="submit" class="btn btn-primary">保存</button>
            <a href="{{ url_for('departments') }}" class="btn btn-secondary">取消</a>
        </form>
    </div>
</div>
{% endblock %}
EOF

cp templates/departments/add.html templates/departments/edit.html

# 创建考勤列表模板
cat > templates/attendances/list.html << 'EOF'
{% extends "base.html" %}
{% block title %}考勤管理{% endblock %}
{% block content %}
<h2><i class="bi bi-calendar-check me-2"></i>考勤管理</h2>
{% if current_user.role == 'admin' %}
<a href="{{ url_for('add_attendance') }}" class="btn btn-primary mb-3"><i class="bi bi-plus"></i> 添加考勤</a>
<a href="{{ url_for('export_attendances') }}" class="btn btn-success mb-3"><i class="bi bi-download"></i> 导出Excel</a>
{% endif %}
<div class="card">
    <div class="card-body">
        <table class="table table-hover">
            <thead>
                <tr><th>员工</th><th>日期</th><th>上班时间</th><th>下班时间</th><th>状态</th><th>操作</th></tr>
            </thead>
            <tbody>
            {% for att in attendances %}
            <tr>
                <td>{{ att.employee.name }}</td>
                <td>{{ att.date }}</td>
                <td>{{ att.check_in_time or '-' }}</td>
                <td>{{ att.check_out_time or '-' }}</td>
                <td><span class="badge bg-info">{{ att.status }}</span></td>
                <td>
                    {% if current_user.role == 'admin' %}
                    <a href="{{ url_for('edit_attendance', id=att.id) }}" class="btn btn-sm btn-warning"><i class="bi bi-pencil"></i></a>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
EOF

# 创建考勤添加/编辑模板
cat > templates/attendances/add.html << 'EOF'
{% extends "base.html" %}
{% block title %}添加考勤{% endblock %}
{% block content %}
<h2>{{ "添加" if not attendance else "编辑" }}考勤记录</h2>
<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="mb-3">
                <label class="form-label">员工 *</label>
                <select class="form-select" name="employee_id" required>
                    <option value="">请选择</option>
                    {% for emp in employees %}
                    <option value="{{ emp.id }}" {% if attendance and attendance.employee_id == emp.id %}selected{% endif %}>{{ emp.name }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="mb-3">
                <label class="form-label">日期 *</label>
                <input type="date" class="form-control" name="date" value="{{ attendance.date if attendance else '' }}" required>
            </div>
            <div class="mb-3">
                <label class="form-label">上班时间</label>
                <input type="time" class="form-control" name="check_in_time" value="{{ attendance.check_in_time if attendance else '' }}">
            </div>
            <div class="mb-3">
                <label class="form-label">下班时间</label>
                <input type="time" class="form-control" name="check_out_time" value="{{ attendance.check_out_time if attendance else '' }}">
            </div>
            <div class="mb-3">
                <label class="form-label">状态</label>
                <select class="form-select" name="status">
                    <option value="正常">正常</option>
                    <option value="迟到">迟到</option>
                    <option value="早退">早退</option>
                    <option value="缺勤">缺勤</option>
                    <option value="请假">请假</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary">保存</button>
            <a href="{{ url_for('attendances') }}" class="btn btn-secondary">取消</a>
        </form>
    </div>
</div>
{% endblock %}
EOF

cp templates/attendances/add.html templates/attendances/edit.html

# 创建绩效列表模板
cat > templates/performances/list.html << 'EOF'
{% extends "base.html" %}
{% block title %}绩效考核{% endblock %}
{% block content %}
<h2><i class="bi bi-graph-up me-2"></i>绩效考核</h2>
{% if current_user.role == 'admin' %}
<a href="{{ url_for('add_performance') }}" class="btn btn-primary mb-3"><i class="bi bi-plus"></i> 添加考核</a>
<a href="{{ url_for('export_performances') }}" class="btn btn-success mb-3"><i class="bi bi-download"></i> 导出Excel</a>
{% endif %}
<div class="card">
    <div class="card-body">
        <table class="table table-hover">
            <thead>
                <tr><th>员工</th><th>年度</th><th>季度</th><th>教学</th><th>科研</th><th>服务</th><th>总分</th><th>等级</th><th>操作</th></tr>
            </thead>
            <tbody>
            {% for perf in performances %}
            <tr>
                <td>{{ perf.employee.name }}</td>
                <td>{{ perf.year }}</td>
                <td>Q{{ perf.quarter }}</td>
                <td>{{ perf.teaching_score }}</td>
                <td>{{ perf.research_score }}</td>
                <td>{{ perf.service_score }}</td>
                <td><strong>{{ "%.1f"|format(perf.total_score) }}</strong></td>
                <td><span class="badge bg-success">{{ perf.rating }}</span></td>
                <td>
                    {% if current_user.role == 'admin' %}
                    <a href="{{ url_for('edit_performance', id=perf.id) }}" class="btn btn-sm btn-warning"><i class="bi bi-pencil"></i></a>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
EOF

# 创建绩效添加/编辑模板
cat > templates/performances/add.html << 'EOF'
{% extends "base.html" %}
{% block title %}添加绩效考核{% endblock %}
{% block content %}
<h2>{{ "添加" if not performance else "编辑" }}绩效考核</h2>
<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="mb-3">
                <label class="form-label">员工 *</label>
                <select class="form-select" name="employee_id" required>
                    <option value="">请选择</option>
                    {% for emp in employees %}
                    <option value="{{ emp.id }}" {% if performance and performance.employee_id == emp.id %}selected{% endif %}>{{ emp.name }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label class="form-label">年度 *</label>
                    <input type="number" class="form-control" name="year" value="{{ performance.year if performance else '' }}" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">季度 *</label>
                    <select class="form-select" name="quarter" required>
                        <option value="1">第一季度</option>
                        <option value="2">第二季度</option>
                        <option value="3">第三季度</option>
                        <option value="4">第四季度</option>
                    </select>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4 mb-3">
                    <label class="form-label">教学评分 (0-100)</label>
                    <input type="number" class="form-control" name="teaching_score" min="0" max="100" value="{{ performance.teaching_score if performance else 0 }}">
                </div>
                <div class="col-md-4 mb-3">
                    <label class="form-label">科研评分 (0-100)</label>
                    <input type="number" class="form-control" name="research_score" min="0" max="100" value="{{ performance.research_score if performance else 0 }}">
                </div>
                <div class="col-md-4 mb-3">
                    <label class="form-label">服务评分 (0-100)</label>
                    <input type="number" class="form-control" name="service_score" min="0" max="100" value="{{ performance.service_score if performance else 0 }}">
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label">考核人</label>
                <input type="text" class="form-control" name="evaluator" value="{{ performance.evaluator if performance else '' }}">
            </div>
            <div class="mb-3">
                <label class="form-label">考核日期</label>
                <input type="date" class="form-control" name="evaluation_date" value="{{ performance.evaluation_date if performance else '' }}">
            </div>
            <div class="mb-3">
                <label class="form-label">评语</label>
                <textarea class="form-control" name="comments" rows="3">{{ performance.comments if performance else '' }}</textarea>
            </div>
            <button type="submit" class="btn btn-primary">保存</button>
            <a href="{{ url_for('performances') }}" class="btn btn-secondary">取消</a>
        </form>
    </div>
</div>
{% endblock %}
EOF

cp templates/performances/add.html templates/performances/edit.html

# 创建职称和培训的简化模板
cat > templates/titles/list.html << 'EOF'
{% extends "base.html" %}
{% block title %}职称评审{% endblock %}
{% block content %}
<h2><i class="bi bi-award me-2"></i>职称评审</h2>
{% if current_user.role == 'admin' %}
<a href="{{ url_for('add_title') }}" class="btn btn-primary mb-3"><i class="bi bi-plus"></i> 添加职称</a>
{% endif %}
<div class="card">
    <div class="card-body">
        <table class="table table-hover">
            <thead>
                <tr><th>员工</th><th>职称名称</th><th>级别</th><th>申请日期</th><th>状态</th><th>操作</th></tr>
            </thead>
            <tbody>
            {% for title in titles %}
            <tr>
                <td>{{ title.employee.name }}</td>
                <td>{{ title.title_name }}</td>
                <td>{{ title.title_level or '-' }}</td>
                <td>{{ title.application_date or '-' }}</td>
                <td><span class="badge {{ 'bg-warning' if title.status == '待审核' else 'bg-success' }}">{{ title.status }}</span></td>
                <td>
                    {% if current_user.role == 'admin' %}
                    <a href="{{ url_for('edit_title', id=title.id) }}" class="btn btn-sm btn-warning"><i class="bi bi-pencil"></i></a>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
EOF

cat > templates/titles/add.html << 'EOF'
{% extends "base.html" %}
{% block title %}添加职称{% endblock %}
{% block content %}
<h2>{{ "添加" if not title else "编辑" }}职称评审</h2>
<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="mb-3">
                <label class="form-label">员工 *</label>
                <select class="form-select" name="employee_id" required>
                    <option value="">请选择</option>
                    {% for emp in employees %}
                    <option value="{{ emp.id }}" {% if title and title.employee_id == emp.id %}selected{% endif %}>{{ emp.name }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="mb-3">
                <label class="form-label">职称名称 *</label>
                <input type="text" class="form-control" name="title_name" value="{{ title.title_name if title else '' }}" required>
            </div>
            <div class="mb-3">
                <label class="form-label">职称级别</label>
                <select class="form-select" name="title_level">
                    <option value="">请选择</option>
                    <option value="初级">初级</option>
                    <option value="中级">中级</option>
                    <option value="高级">高级</option>
                </select>
            </div>
            <div class="mb-3">
                <label class="form-label">申请日期</label>
                <input type="date" class="form-control" name="application_date" value="{{ title.application_date if title else '' }}">
            </div>
            <div class="mb-3">
                <label class="form-label">状态</label>
                <select class="form-select" name="status">
                    <option value="待审核">待审核</option>
                    <option value="已通过">已通过</option>
                    <option value="未通过">未通过</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary">保存</button>
            <a href="{{ url_for('titles') }}" class="btn btn-secondary">取消</a>
        </form>
    </div>
</div>
{% endblock %}
EOF

cp templates/titles/add.html templates/titles/edit.html

cat > templates/trainings/list.html << 'EOF'
{% extends "base.html" %}
{% block title %}培训发展{% endblock %}
{% block content %}
<h2><i class="bi bi-book me-2"></i>培训发展</h2>
{% if current_user.role == 'admin' %}
<a href="{{ url_for('add_training') }}" class="btn btn-primary mb-3"><i class="bi bi-plus"></i> 添加培训</a>
{% endif %}
<div class="card">
    <div class="card-body">
        <table class="table table-hover">
            <thead>
                <tr><th>培训名称</th><th>员工</th><th>类型</th><th>开始日期</th><th>时长(小时)</th><th>状态</th><th>操作</th></tr>
            </thead>
            <tbody>
            {% for training in trainings %}
            <tr>
                <td>{{ training.training_name }}</td>
                <td>{{ training.employee.name }}</td>
                <td>{{ training.training_type or '-' }}</td>
                <td>{{ training.start_date or '-' }}</td>
                <td>{{ training.duration_hours or '-' }}</td>
                <td><span class="badge bg-info">{{ training.status }}</span></td>
                <td>
                    {% if current_user.role == 'admin' %}
                    <a href="{{ url_for('edit_training', id=training.id) }}" class="btn btn-sm btn-warning"><i class="bi bi-pencil"></i></a>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
EOF

cat > templates/trainings/add.html << 'EOF'
{% extends "base.html" %}
{% block title %}添加培训{% endblock %}
{% block content %}
<h2>{{ "添加" if not training else "编辑" }}培训记录</h2>
<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="mb-3">
                <label class="form-label">员工 *</label>
                <select class="form-select" name="employee_id" required>
                    <option value="">请选择</option>
                    {% for emp in employees %}
                    <option value="{{ emp.id }}" {% if training and training.employee_id == emp.id %}selected{% endif %}>{{ emp.name }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="mb-3">
                <label class="form-label">培训名称 *</label>
                <input type="text" class="form-control" name="training_name" value="{{ training.training_name if training else '' }}" required>
            </div>
            <div class="mb-3">
                <label class="form-label">培训类型</label>
                <select class="form-select" name="training_type">
                    <option value="">请选择</option>
                    <option value="内部培训">内部培训</option>
                    <option value="外部培训">外部培训</option>
                    <option value="在线培训">在线培训</option>
                </select>
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label class="form-label">开始日期</label>
                    <input type="date" class="form-control" name="start_date" value="{{ training.start_date if training else '' }}">
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">结束日期</label>
                    <input type="date" class="form-control" name="end_date" value="{{ training.end_date if training else '' }}">
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label">培训时长(小时)</label>
                <input type="number" class="form-control" name="duration_hours" value="{{ training.duration_hours if training else '' }}">
            </div>
            <div class="mb-3">
                <label class="form-label">培训地点</label>
                <input type="text" class="form-control" name="location" value="{{ training.location if training else '' }}">
            </div>
            <div class="mb-3">
                <label class="form-label">讲师</label>
                <input type="text" class="form-control" name="instructor" value="{{ training.instructor if training else '' }}">
            </div>
            <div class="mb-3">
                <label class="form-label">费用</label>
                <input type="number" class="form-control" name="cost" value="{{ training.cost if training else '' }}">
            </div>
            <div class="mb-3">
                <label class="form-label">状态</label>
                <select class="form-select" name="status">
                    <option value="已计划">已计划</option>
                    <option value="进行中">进行中</option>
                    <option value="已完成">已完成</option>
                    <option value="已取消">已取消</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary">保存</button>
            <a href="{{ url_for('trainings') }}" class="btn btn-secondary">取消</a>
        </form>
    </div>
</div>
{% endblock %}
EOF

cp templates/trainings/add.html templates/trainings/edit.html

echo "✅ 所有模板文件创建完成！"
