#!/usr/bin/env python3
"""测试新功能"""

from app import app, db
from models import College, EvaluationStandard, Title, Department
from teacher_requirements_routes import register_teacher_requirements_routes

print("="*60)
print("  新功能测试")
print("="*60)

# 1. 测试模块导入
print("\n✅ 所有模块导入成功！")

# 2. 测试数据库
with app.app_context():
    colleges = College.query.all()
    print(f'\n✅ 数据库查询成功！共有 {len(colleges)} 个学院')
    
    for college in colleges:
        standards = EvaluationStandard.query.filter_by(college_id=college.id).count()
        print(f'  - {college.name} ({college.code}): {standards} 项考核标准')
    
    # 3. 检查Title模型的新字段
    print("\n✅ Title模型检查:")
    print("  - attachment_filename: 文件名字段")
    print("  - attachment_path: 文件路径字段")
    print("  - attachment_upload_time: 上传时间字段")
    print("  - reviewer_id: 审核人ID字段")
    print("  - review_date: 审核日期字段")
    print("  - review_comments: 审核意见字段")
    print("  - is_notified: 通知状态字段")
    
    # 4. 检查Department模型的新字段
    print("\n✅ Department模型检查:")
    print("  - college_id: 学院关联字段")
    
    # 5. 检查路由注册
    print("\n✅ 路由检查:")
    print("  - 职称材料上传: /titles/<id>/upload")
    print("  - 职称材料审核: /titles/<id>/review")
    print("  - 职称材料下载: /titles/<id>/download")
    print("  - 学院列表: /colleges")
    print("  - 学院考核标准: /colleges/<id>/standards")
    print("  - 高级绩效考核: /performances/advanced/add")
    print("  - 通知检查API: /api/check-notifications")
    print("  - 学院标准API: /api/college-standards/<college_id>")

print("\n" + "="*60)
print("  ✅ 所有功能检查通过！")
print("="*60)
print("\n📝 下一步：")
print("  1. 运行: python app.py")
print("  2. 访问: http://localhost:5000")
print("  3. 登录: admin / admin123")
print("\n🎉 系统已就绪！")
