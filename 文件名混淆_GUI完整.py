import os
import hashlib
import sqlite3
import threading
from tkinter import Tk, Label, Entry, Button, Text, END, messagebox, filedialog

# 配置
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
conn.close()

# 计算文件名的SHA512哈希值（加盐）
def hash_filename(filename, salt):
    hasher = hashlib.sha512()
    hasher.update(salt.encode('utf-8'))
    hasher.update(filename.encode('utf-8'))
    return hasher.hexdigest()

# 批量重命名文件
def batch_rename(directory, salt):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            hashed_name = hash_filename(filename, salt)
            new_file_path = os.path.join(root, hashed_name)
            os.rename(file_path, new_file_path)
            cursor.execute('INSERT INTO file_hashes (original_name, hashed_name) VALUES (?, ?)', (filename, hashed_name))
            conn.commit()
    conn.close()
    messagebox.showinfo("完成", "文件重命名和数据库更新完成。")

# 恢复文件名
def restore_filenames(directory):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT original_name, hashed_name FROM file_hashes')
    rows = cursor.fetchall()
    for row in rows:
        original_name, hashed_name = row
        for root, dirs, files in os.walk(directory):
            if hashed_name in files:
                hashed_file_path = os.path.join(root, hashed_name)
                original_file_path = os.path.join(root, original_name)
                os.rename(hashed_file_path, original_file_path)
                break
    conn.close()
    messagebox.showinfo("完成", "文件恢复完成。")

# 搜索文件名
def search_filename():
    search_keyword = entry_search.get().lower()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT original_name, hashed_name FROM file_hashes WHERE lower(original_name) LIKE ?', ('%' + search_keyword + '%',))
    rows = cursor.fetchall()
    conn.close()
    text_result.delete(1.0, END)
    if rows:
        for original_name, hashed_name in rows:
            text_result.insert(END, f"原始文件名: {original_name}\n")
            text_result.insert(END, f"对应的哈希值: {hashed_name}\n")
    else:
        messagebox.showinfo("结果", "没有找到包含关键字的文件。")

# 使用线程执行任务
def run_threaded(task, *args):
    threading.Thread(target=task, args=args).start()

# 选择文件夹路径
def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_dir.delete(0, END)
        entry_dir.insert(END, directory)

# 创建GUI
root = Tk()
root.title("文件名哈希工具")

Label(root, text="文件夹路径:").grid(row=0, column=0, sticky="e")
entry_dir = Entry(root, width=50)
entry_dir.grid(row=0, column=1, padx=5, pady=5)
Button(root, text="选择", command=select_directory).grid(row=0, column=2, padx=5, pady=5)

Label(root, text="加盐值:").grid(row=1, column=0, sticky="e")
entry_salt = Entry(root, width=50)
entry_salt.grid(row=1, column=1, padx=5, pady=5)
entry_salt.insert(END, salt)

Button(root, text="批量重命名文件", command=lambda: run_threaded(batch_rename, entry_dir.get(), entry_salt.get())).grid(row=2, column=0, columnspan=3, pady=5)

Button(root, text="恢复文件名", command=lambda: run_threaded(restore_filenames, entry_dir.get())).grid(row=3, column=0, columnspan=3, pady=5)

Label(root, text="搜索文件名关键字:").grid(row=4, column=0, sticky="e")
entry_search = Entry(root, width=50)
entry_search.grid(row=4, column=1, padx=5, pady=5)

Button(root, text="搜索", command=search_filename).grid(row=5, column=0, columnspan=3, pady=5)

text_result = Text(root, height=10, width=50)
text_result.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
#另外采取Veracrypt是个不错的选择
