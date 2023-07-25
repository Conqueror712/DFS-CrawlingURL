import requests
import json
import time

# 打开文件
with open('sorted_result.txt', 'r') as f:
    # 循环读取每一行
    for line in f:
        domain = line.strip()  # 去掉行尾的换行符
        # 构造请求参数
        params = {'domains': domain}

        # 发送HTTP请求
        response = requests.get('https://apistore.aizhan.com/baidurank/siteinfos/'
                                '2067c8d0d686ee9f08116b72ea7218ff', params=params)

        # 处理响应结果
        if response.status_code == 200:
            # 反序列化JSON
            result = json.loads(response.text)

            # 访问Python对象的属性或者键值对
            if result['status'] == 'success':
                success_data = result['data']['success']
                for item in success_data:
                    print(
                          "站点域名：", item['domain'],
                          "\n站点PC端百度权重：",  item['pc_br'],
                          "\n站点移动端百度权重：", item['m_br'],
                          "\n站点点击权重：", item['ip'],
                          "\n站点PC端点击权重：", item['pc_ip'],
                          "\n站点移动端点击权重：", item['m_ip'],
                          "\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
                    )
            else:
                print('请求失败，错误信息：', result['msg'])
        else:
            print('请求失败，状态码：', response.status_code)

        # 等待0.5秒
        time.sleep(0.5)
