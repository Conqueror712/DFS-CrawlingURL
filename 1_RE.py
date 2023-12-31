import re

# 定义正则表达式
pattern = r'https?://([\w.-]+)/?'

# 读取文件并提取域名
domains = set()
with open('result.txt', 'r') as f:
    for line in f:
        match = re.match(pattern, line)
        if match:
            domains.add(match.group(1))

# 对域名列表进行字典序排序
sorted_domains = sorted(domains)

# 将结果写入文件
with open('sorted_result.txt', 'w') as f:
    for domain in sorted_domains:
        f.write(domain + '\n')
        print(domain)
