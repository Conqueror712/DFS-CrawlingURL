import trafilatura
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import csv
import time

successful_cnt = 0
failed_cnt = 0

# 读取文件并提取域名
with open('ans1.csv', 'r', encoding='gbk', errors="replace") as f:
    reader = csv.reader(f)
    next(reader)  # 跳过标题行
    with open('new_ans1.csv', 'w', encoding='gbk', errors="replace", newline='') as fw:
        writer = csv.writer(fw)
        writer.writerow(['域名', '原始提取结果', '关键词', '文本摘要'])
        for row in reader:
            is_suc = 0  # 默认没有成功的网站
            url = "https://" + row[0]
            start_time = time.time()  # 记录当前时间戳
            tmp_downloaded = trafilatura.fetch_url(url)
            end_time = time.time()  # 记录下载完成时间戳
            if str(trafilatura.extract(tmp_downloaded)) != "None":
                print("OK")
                original_text = str(trafilatura.extract(tmp_downloaded))
                successful_cnt += 1
                is_suc = 1
            else:
                if end_time - start_time > 5:
                    print(f"Download timeout for {url}")
                    failed_cnt += 1
                    original_text = "ERROR"
                else:
                    print(f"Failed to download {url}")
                    continue

            # 进行关键词提取和文本摘要
            print("now = ", row)
            start_time = time.time()  # 记录当前时间戳
            tr4w = TextRank4Keyword()
            tr4w.analyze(text=original_text, lower=True, window=2)

            keywords = []
            for item in tr4w.get_keywords(20, word_min_len=1):
                keywords.append(item.word)

            tr4s = TextRank4Sentence()
            tr4s.analyze(text=original_text, lower=True, source='all_filters')

            summary = []
            for item in tr4s.get_key_sentences(num=3):
                summary.append(item.sentence)
            end_time = time.time()  # 记录处理完成时间戳

            # 判断处理是否超时
            if end_time - start_time > 5:
                print(f"Processing timeout for {url}")
                failed_cnt += 1
                continue

            # 写入新的CSV文件
            writer.writerow([row[0], original_text, ' '.join(keywords), '; '.join(summary)])
