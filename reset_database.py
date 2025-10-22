#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库重置脚本 - 强力版
使用方法：python reset_database.py
"""

import os
import sys
import time
import gc

def force_delete_db(db_file):
    """强制删除数据库文件"""
    max_attempts = 5
    
    for attempt in range(max_attempts):
        try:
            if os.path.exists(db_file):
                # 尝试删除
                os.remove(db_file)
                print(f"✅ 已删除旧数据库: {db_file}")
                return True
        except PermissionError:
            print(f"⚠️  尝试 {attempt + 1}/{max_attempts}: 数据库文件被占用...")
            print("   正在强制关闭所有连接...")
            
            # 强制垃圾回收，释放数据库连接
            gc.collect()
            time.sleep(1)
            
            # 尝试重命名文件（如果删除失败）
            try:
                backup_name = f"{db_file}.old.{int(time.time())}"
                os.rename(db_file, backup_name)
                print(f"✅ 已重命名为: {backup_name}")
                return True
            except:
                pass
        except Exception as e:
            print(f"❌ 删除失败: {e}")
    
    print("\n❌ 无法删除数据库文件！")
    print("\n📝 手动解决方法：")
    print("   1. 关闭所有Python进程和浏览器")
    print("   2. 手动删除文件: hr_system.db")
    print("   3. 重新运行此脚本")
    return False

def reset_database():
    """重置数据库：删除旧数据库并重新初始化"""
    db_file = 'hr_system.db'
    
    print("=" * 60)
    print("  高校人事管理系统 - 数据库重置工具（强力版）")
    print("=" * 60)
    print()
    
    # 检查数据库文件是否存在
    if os.path.exists(db_file):
        print(f"🔍 发现旧数据库文件: {db_file}")
        print(f"   文件大小: {os.path.getsize(db_file) / 1024:.2f} KB")
        print()
        confirm = input("⚠️  删除数据库将清空所有数据！确认继续吗？(输入 yes 继续): ")
        
        if confirm.lower() != 'yes':
            print("❌ 操作已取消")
            return
        
        print()
        print("🔧 正在删除旧数据库...")
        if not force_delete_db(db_file):
            sys.exit(1)
    else:
        print(f"📝 未找到旧数据库文件: {db_file}")
        print("   将创建新数据库...")
    
    print()
    print("=" * 60)
    print("  初始化新数据库")
    print("=" * 60)
    print()
    
    # 确保旧连接被清理
    gc.collect()
    time.sleep(0.5)
    
    # 导入app并初始化数据库
    try:
        print("📦 正在加载应用模块...")
        from app import app, db, init_database
        
        print("🔧 正在创建数据库表...")
        init_database()
        
        print()
        print("=" * 60)
        print("  ✅ 数据库重置完成！")
        print("=" * 60)
        print()
        print("📊 数据库信息：")
        print(f"   位置: {os.path.abspath(db_file)}")
        if os.path.exists(db_file):
            print(f"   大小: {os.path.getsize(db_file) / 1024:.2f} KB")
        print()
        print("👤 默认管理员账户：")
        print("   用户名: admin")
        print("   密码: admin123")
        print()
        print("🚀 启动命令：")
        print("   python app.py")
        print("   或运行: 启动脚本.bat (Windows) / bash 启动脚本.sh (Mac/Linux)")
        print()
        print("=" * 60)
        
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        print("\n请检查：")
        print("  1. 是否安装了所有依赖: pip install -r requirements.txt")
        print("  2. 是否在正确的目录: 应该在项目根目录")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        print("\n详细错误信息：")
        import traceback
        traceback.print_exc()
        print("\n可能的解决方法：")
        print("  1. 检查 models.py 是否有语法错误")
        print("  2. 确保所有依赖已安装")
        print("  3. 查看上方的详细错误信息")
        sys.exit(1)

if __name__ == '__main__':
    reset_database()
