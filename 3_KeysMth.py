import csv

# 读取关键词与类别的映射
keyword_map = {}
with open('keyword_map.csv', mode='r', encoding='gbk') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if len(row) == 2:
            keyword_map[row[0]] = row[1]
        else:
            print(f"错误：行数据列数不为 2：{row}")

# 用于存储每个文本的关键词列表
all_keywords = []

# 读取文本文件
with open('sum_text.txt', mode='r', encoding='utf-8') as f:
    current_keywords = []  # 当前文本的关键词列表
    for line in f:
        line = line.strip()  # 去掉行末的换行符等空白字符
        if line.startswith('关键词：'):
            # 如果遇到了新的关键词行，则将之前的关键词列表加入到 all_keywords 中，并清空当前列表
            all_keywords.append(current_keywords)
            current_keywords = []
            # 将新的关键词行解析出来，加入到当前列表中
            keywords = line[4:].split()
            current_keywords.extend(keywords)
        elif line.startswith('文本摘要：'):
            # 如果遇到了文本摘要行，则将之前的关键词列表加入到 all_keywords 中，并清空当前列表
            all_keywords.append(current_keywords)
            current_keywords = []
        else:
            # 如果遇到了其他行则跳过
            continue

# 将每个文本的关键词列表与 map 中的类别进行匹配，分类每个文本
for keywords in all_keywords:
    categories = []
    for keyword in keywords:
        if keyword in keyword_map:
            category = keyword_map[keyword]
            if category not in categories:
                categories.append(category)
                if len(categories) == 2:
                    break
    if len(categories) == 2:
        print('该文本属于 "{}" 类'.format(' & '.join(categories)))
    elif len(categories) == 1:
        print('该文本属于 "{}" 类'.format(categories[0]))
    else:
        print('该文本属于 "其他" 类')

#
# # 将字典中的数据写入CSV文件
# with open('keyword_map.csv', mode='a', newline='', encoding='gbk') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Keyword', 'Category'])  # 写入首行
#     for keyword, category in keywords.items():
#         writer.writerow([keyword, category])
