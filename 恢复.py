import os
import sqlite3

# 配置
directory = '/path/to/your/hashed/files'  # 被哈希处理的文件夹路径
db_path = 'file_hashes.db'  # SQLite数据库文件路径

# 创建SQLite数据库连接
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 从数据库中获取哈希值和原始文件名的映射
cursor.execute('SELECT original_name, hashed_name FROM file_hashes')
rows = cursor.fetchall()

# 重命名文件
for row in rows:
    original_name, hashed_name = row
    hashed_file_path = os.path.join(directory, hashed_name)
    original_file_path = os.path.join(directory, original_name)
    
    # 检查哈希文件是否存在
    if os.path.isfile(hashed_file_path):
        # 重命名文件
        os.rename(hashed_file_path, original_file_path)
    else:
        print(f"文件 {hashed_name} 未找到，无法恢复到 {original_name}")

# 关闭数据库连接
conn.close()

print('文件恢复完成。')
