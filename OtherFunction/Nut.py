import trafilatura
from textrank4zh import TextRank4Keyword
import csv

# import codecs

# 读取关键词与类别的映射
k_map = {}
with open('keyword_map.csv', mode='r', encoding='gbk') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if len(row) == 2:
            k_map[row[0]] = row[1]
        else:
            print(f"错误：行数据列数不为 2：{row}")

# 用于存储每个文本的关键词列表
all_keywords = []

# 读取文件并提取域名
with open('ans_ori.csv', 'r', encoding='gbk') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # 跳过表头行
    for row in reader:
        url = row[0]
        categories = []
        tmp_downloaded = trafilatura.fetch_url(url)
        if str(trafilatura.extract(tmp_downloaded)) != "None":
            text = str(trafilatura.extract(tmp_downloaded))
            tr4w = TextRank4Keyword()
            tr4w.analyze(text=text, lower=True, window=2)
            keywords = []
            for item in tr4w.get_keywords(20, word_min_len=1):
                keywords.append(item.word)
            all_keywords.append(keywords)

            # 将当前文本的关键词列表与 map 中的类别进行匹配，分类当前文本
            for keyword in keywords:
                if keyword in k_map:
                    category = k_map[keyword]
                    if category not in categories:
                        categories.append(category)
                        if len(categories) == 2:
                            break
            if len(categories) == 2:
                print(f"{url} 属于 \"{categories[0]} & {categories[1]}\" 类")
            elif len(categories) == 1:
                print(f"{url} 属于 \"{categories[0]}\" 类")
            else:
                print(f"{url} 属于 \"其他\" 类")
        else:
            print(f"错误：无法从 {url} 下载文本")
            categories = ["错误分类"]  # 将分类结果设为 "错误分类"

        # 将分类结果写入 ans.csv 文件的第二列
        with open('ans.csv', mode='a', encoding='gbk', newline='') as csvfile2:
            writer = csv.writer(csvfile2)
            writer.writerow([url, categories])
