import os

# 基础配置
class Config:
    # 密钥（用于session加密）
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hr_system.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 文件上传配置
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大上传16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'xls', 'xlsx'}
    
    # 分页配置
    ITEMS_PER_PAGE = 10
    
    # 应用名称
    APP_NAME = '高校教职工人事信息管理系统'
