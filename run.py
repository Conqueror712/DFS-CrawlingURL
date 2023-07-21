import os

# 列出所有的.py文件
files = [file for file in os.listdir('.') if file.endswith('.py')]

# 按文件名排序
files.sort()

# 删除run.py
files.pop()

# 逐一运行所有的.py文件
for file in files:
    os.system('python {}'.format(file))
