import trafilatura
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import codecs

successful_cnt = 0
failed_cnt = 0
texts = set()

# 读取文件并提取域名
with open('sorted_result.txt', 'r') as f:
    for line in f:
        is_suc = 0  # 默认没有成功的网站
        url = "https://" + line.strip()
        tmp_downloaded = trafilatura.fetch_url(url)
        if str(trafilatura.extract(tmp_downloaded)) != "None":
            print(trafilatura.extract(tmp_downloaded))
            texts.add(str(trafilatura.extract(tmp_downloaded)))
            successful_cnt += 1
            is_suc = 1
        else:
            print(f"Failed to download {url}")
            failed_cnt += 1

        print(">>>>>>>>>>>>>>>>> 计数环节 >>>>>>>>>>>>>>>>>")
        print("successful = ", successful_cnt)
        print("failed = ", failed_cnt)

        # 调用第二份代码进行关键词提取和文本摘要
        if is_suc == 1:  # 有成功的网站就进行一次处理
            with codecs.open('long_text.txt', 'w', 'utf-8') as f:
                for text in texts:
                    f.write(text + '\n')

            # 读取long_text.txt并进行关键词提取和文本摘要
            with codecs.open('long_text.txt', 'r', 'utf-8') as f:
                text = f.read()
            tr4w = TextRank4Keyword()
            tr4w.analyze(text=text, lower=True, window=2)

            with codecs.open('sum_text.txt', 'a', 'utf-8') as f:
                f.write('关键词：')
                for item in tr4w.get_keywords(20, word_min_len=1):
                    # f.write(f"{item.word} {item.weight}\n")
                    f.write(f"{item.word} ")
                f.write('\n')

            with codecs.open('long_text.txt', 'r', 'utf-8') as f:
                text = f.read()
            tr4s = TextRank4Sentence()
            tr4s.analyze(text=text, lower=True, source='all_filters')

            with codecs.open('sum_text.txt', 'a', 'utf-8') as f:
                f.write('文本摘要：\n')
                for item in tr4s.get_key_sentences(num=3):
                    # f.write(f"{item.index} {item.weight} {item.sentence}\n")
                    f.write(f"{item.sentence}; ")
                f.write('\n\n')

            # 清空texts和long_text.txt
            texts.clear()
            with codecs.open('long_text.txt', 'w', 'utf-8'):
                pass

# 最后进行一次处理
if len(texts) > 0:
    with codecs.open('long_text.txt', 'w', 'utf-8') as f:
        for text in texts:
            f.write(text + '\n')

    # 读取long_text.txt并进行关键词提取和文本摘要
    with codecs.open('long_text.txt', 'r', 'utf-8') as f:
        text = f.read()
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2)

    with codecs.open('sum_text.txt', 'a', 'utf-8') as f:
        f.write('关键词：')
        for item in tr4w.get_keywords(20, word_min_len=1):
            # f.write(f"{item.word} {item.weight}\n")
            f.write(f"{item.word} ")
        f.write('\n')

    with codecs.open('long_text.txt', 'r', 'utf-8') as f:
        text = f.read()
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source='all_filters')

    with codecs.open('sum_text.txt', 'a', 'utf-8') as f:
        f.write('文本摘要：\n')
        for item in tr4s.get_key_sentences(num=3):
            # f.write(f"{item.index} {item.weight} {item.sentence}\n")
            f.write(f"{item.sentence}; ")
        f.write('\n\n')