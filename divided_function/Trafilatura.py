import trafilatura

successful_cnt = 0
failed_cnt = 0

texts = set()

# 读取文件并提取域名
with open('../sorted_result.txt', 'r') as f:
    for line in f:
        url = "https://" + line.strip()
        tmp_downloaded = trafilatura.fetch_url(url)
        if str(trafilatura.extract(tmp_downloaded)) != "None":
            print(trafilatura.extract(tmp_downloaded))
            texts.add(str(trafilatura.extract(tmp_downloaded)))
            successful_cnt += 1
        else:
            print(f"Failed to download {url}")
            failed_cnt += 1

        print(">>>>>>>>>>>>>>>>> 计数环节 >>>>>>>>>>>>>>>>>")
        print("successful = ", successful_cnt)
        print("failed = ", failed_cnt)

with open('../long_text.txt', 'w') as f:
    for text in texts:
        f.write(text + '\n')
