import re
import sys
import requests

try:
    import tldextract
except:
    print('module tldextract not fount \nyou can try pip install tldextract')
    sys.exit()


def domain_get():
    # 接收要爬取的网站URL
    URL = input("请输入要爬取的网站URL：")
    if '//' not in URL:
        URL = 'https://' + URL
    try:
        kv = {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/70.0.3538.77 Safari/537.36'}
        requests.head(URL, headers=kv)
        return URL
    except:
        print("Your URL is incorrect!")
        return domain_get()


class spider():
    def __init__(self, domain, key, depth):
        self.domain = domain  # 爬取的域名
        self.depth = depth  # 爬取的深度
        self.URLs_all = set([])  # 爬取的结果
        self.key = key  # 顶级域名，用于排除外链

    def page_spider(self, URL):
        # 爬取URL中的所有链接
        try:
            kv = {
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/70.0.3538.77 Safari/537.36'}
            r = requests.get(URL, headers=kv, timeout=2)
            r.encoding = r.apparent_encoding
            page_text = r.text
            page_links = re.findall(r'(?<=href=\").*?(?=\")|(?<=href=\').*?(?=\')', page_text)

        except:
            return set([])
        # 接下来对爬取的链接进行处理

        # 1、先去除不同域的链接
        URL_list = set([])
        for URL in page_links:
            if self.key in URL:
                URL_list.add(URL)

        # 2、再对链接进行去重处理
        URL_list = set(URL_list) - self.URLs_all
        self.URLs_all.update(URL_list)
        return URL_list  # 返回集合

    def run(self):
        # URL_list = set([self.domain])  # 第一次爬取原始URL的链接
        URL_list = {self.domain}  # 第一次爬取原始URL的链接
        while self.depth >= 1:  # 每一次深度的爬取都会爬取URL_list的所有链接
            print("正在进行倒数第%d轮爬取，这大概需要一段时间，请耐心等待..." % self.depth)
            URL_list_tmp = set([])
            for URL in URL_list:
                URL_list_tmp.update(self.page_spider(URL))
            URL_list = URL_list_tmp
            self.depth = self.depth - 1

        file = open('result.txt', 'w')
        for URL in self.URLs_all:
            file.write(URL)
            file.write('\n')
        file.close()


if __name__ == '__main__':
    domain = domain_get()
    print('好的，我们将从这个站点开始爬取:', domain)

    # 以下代码是用于排除外链的（爬取的URL不包含key的都会被舍弃），如果需要请启用并加以修改，并注意修改下面的key="" --> key=key
    '''
    key_tmp = tldextract.extract(domain)
    key = key_tmp.subdomain + '.' + key_tmp.domain + '.' + key_tmp.suffix
    print('key:', key)
    '''
    print('>>>>>> [开始爬取] >>>>>>')
    spider = spider(domain=domain, key="", depth=3)
    spider.run()
    print('>>>>>> Finished! 结果已保存至result.txt中 >>>>>>')
