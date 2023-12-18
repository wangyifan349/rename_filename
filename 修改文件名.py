import os
import hashlib
import sqlite3

# 配置
directory = 'H:\\混淆目录'  # 要处理的文件夹路径
salt = 'your_salt_here'  # 加盐
db_path = 'file_hashes.db'  # SQLite数据库文件路径

# 创建SQLite数据库和表
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS file_hashes (
    original_name TEXT,
    hashed_name TEXT
)
''')
conn.commit()

# 计算文件名的SHA512哈希值（加盐）
def hash_filename(filename, salt):
    hasher = hashlib.sha512()
    hasher.update(salt.encode('utf-8'))
    hasher.update(filename.encode('utf-8'))
    return hasher.hexdigest()

# 遍历目录中的所有文件
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        # 计算哈希值
        hashed_name = hash_filename(filename, salt)
        new_file_path = os.path.join(directory, hashed_name)
        
        # 重命名文件
        os.rename(file_path, new_file_path)
        
        # 将原始文件名和哈希值插入数据库
        cursor.execute('INSERT INTO file_hashes (original_name, hashed_name) VALUES (?, ?)', (filename, hashed_name))
        conn.commit()

# 关闭数据库连接
conn.close()

print('文件重命名和数据库更新完成。')
