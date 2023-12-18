import sqlite3

# 配置
db_path = 'file_hashes.db'  # SQLite数据库文件路径

# 创建SQLite数据库连接
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 用户输入要搜索的原始文件名
search_name = input("请输入要搜索的原始文件名: ")

# 从���据库中搜索原始文件名对应的哈希值
cursor.execute('SELECT original_name, hashed_name FROM file_hashes WHERE original_name = ?', (search_name,))
row = cursor.fetchone()

if row:
    original_name, hashed_name = row
    print(f"原始文件名: {original_name}")
    print(f"对应的哈希值: {hashed_name}")
else:
    print("没有找到对应的哈希值。")

# 关闭数据库连接
conn.close()
