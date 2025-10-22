#!/usr/bin/env python3
"""初始化学院和考核标准数据"""

from app import app, db
from models import College, EvaluationStandard


def init_colleges_and_standards():
    """初始化学院和考核标准"""
    with app.app_context():
        print("开始初始化学院和考核标准...")
        
        # 检查是否已有学院数据
        if College.query.first():
            print("学院数据已存在，跳过初始化")
            return
        
        # 创建学院
        colleges_data = [
            {
                'name': '文学院',
                'code': 'WXY',
                'dean': '张教授',
                'description': '文学院负责文学、语言学等人文学科的教学与研究'
            },
            {
                'name': '教育学院',
                'code': 'JYX',
                'dean': '李教授',
                'description': '教育学院负责教育学、心理学等教育类学科的教学与研究'
            },
            {
                'name': '计算机学院',
                'code': 'JSJ',
                'dean': '王教授',
                'description': '计算机学院负责计算机科学、软件工程等学科的教学与研究'
            },
            {
                'name': '数学学院',
                'code': 'SXX',
                'dean': '赵教授',
                'description': '数学学院负责数学、统计学等学科的教学与研究'
            }
        ]
        
        colleges = {}
        for college_data in colleges_data:
            college = College(**college_data)
            db.session.add(college)
            colleges[college_data['code']] = college
            print(f"  创建学院：{college_data['name']}")
        
        db.session.flush()  # 获取college ID
        
        # 为文学院创建考核标准（重视教学和论文发表）
        wxY_standards = [
            {
                'item_name': '教学质量评价',
                'item_type': '教学',
                'weight': 1.2,
                'description': '学生教学评价、督导评价等'
            },
            {
                'item_name': '论文发表',
                'item_type': '科研',
                'weight': 1.5,
                'description': '核心期刊、权威期刊论文发表数量和质量'
            },
            {
                'item_name': '课程建设',
                'item_type': '教学',
                'weight': 1.0,
                'description': '精品课程、在线课程建设'
            },
            {
                'item_name': '社会服务',
                'item_type': '服务',
                'weight': 0.8,
                'description': '学术讲座、文化传播活动等'
            }
        ]
        
        for std_data in wxY_standards:
            std = EvaluationStandard(
                college_id=colleges['WXY'].id,
                **std_data
            )
            db.session.add(std)
        print(f"  为文学院创建 {len(wxY_standards)} 项考核标准")
        
        # 为教育学院创建考核标准（重视教学和教改项目）
        jyx_standards = [
            {
                'item_name': '教学质量评价',
                'item_type': '教学',
                'weight': 1.3,
                'description': '学生教学评价、同行评价'
            },
            {
                'item_name': '教改项目',
                'item_type': '教学',
                'weight': 1.2,
                'description': '教学改革项目、教材编写等'
            },
            {
                'item_name': '科研项目',
                'item_type': '科研',
                'weight': 1.0,
                'description': '教育科研项目、课题研究'
            },
            {
                'item_name': '学生指导',
                'item_type': '服务',
                'weight': 1.0,
                'description': '学生科研指导、实习指导等'
            }
        ]
        
        for std_data in jyx_standards:
            std = EvaluationStandard(
                college_id=colleges['JYX'].id,
                **std_data
            )
            db.session.add(std)
        print(f"  为教育学院创建 {len(jyx_standards)} 项考核标准")
        
        # 为计算机学院创建考核标准（重视算法科研和项目开发）
        jsj_standards = [
            {
                'item_name': '算法研究',
                'item_type': '科研',
                'weight': 1.8,
                'grade_a_score': 95,
                'grade_b_score': 85,
                'grade_c_score': 75,
                'grade_d_score': 65,
                'description': '算法创新、论文发表（CCF A/B类）'
            },
            {
                'item_name': '项目开发',
                'item_type': '科研',
                'weight': 1.5,
                'description': '软件项目开发、系统实现'
            },
            {
                'item_name': '教学质量',
                'item_type': '教学',
                'weight': 1.0,
                'description': '课程教学、实验指导'
            },
            {
                'item_name': '竞赛指导',
                'item_type': '服务',
                'weight': 1.2,
                'description': 'ACM、互联网+等竞赛指导'
            }
        ]
        
        for std_data in jsj_standards:
            std = EvaluationStandard(
                college_id=colleges['JSJ'].id,
                **std_data
            )
            db.session.add(std)
        print(f"  为计算机学院创建 {len(jsj_standards)} 项考核标准（特别重视算法研究）")
        
        # 为数学学院创建考核标准（重视理论研究）
        sxx_standards = [
            {
                'item_name': '理论研究',
                'item_type': '科研',
                'weight': 1.6,
                'description': '数学理论研究、SCI论文发表'
            },
            {
                'item_name': '教学质量',
                'item_type': '教学',
                'weight': 1.2,
                'description': '数学课程教学、教学创新'
            },
            {
                'item_name': '交叉应用',
                'item_type': '科研',
                'weight': 1.0,
                'description': '数学在其他领域的应用研究'
            },
            {
                'item_name': '学术交流',
                'item_type': '服务',
                'weight': 0.8,
                'description': '学术会议、讲座等'
            }
        ]
        
        for std_data in sxx_standards:
            std = EvaluationStandard(
                college_id=colleges['SXX'].id,
                **std_data
            )
            db.session.add(std)
        print(f"  为数学学院创建 {len(sxx_standards)} 项考核标准")
        
        db.session.commit()
        print("✅ 学院和考核标准初始化完成！")
        print("\n创建的学院：")
        for code, college in colleges.items():
            print(f"  - {college.name} ({code})")


if __name__ == '__main__':
    init_colleges_and_standards()
