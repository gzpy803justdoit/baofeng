import json
import requests
import re

if __name__ == '__main__':
    for i in range(1, 164):
        # url = "https://www.taobao.com/markets/hi/list?spm=a215p.1596646.1.8.107f75e3w5nyds#type=121288001&page=163"
        url = "https://izhongchou.taobao.com/dream/ajax/getProjectList.htm?page=163&pageSize=20" + \
              "&projectType=121288001&type=6&status=&sort=1&_ksTS=1537503463309_104&callback=jsonp105"
        header = {
            "Referer": "https://www.taobao.com/markets/hi/list?spm=a215p.1596646.1.8.107f75e3w5nyds",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
        response = requests.get(url, headers=header).text
        # 正则匹配出相关数据的字典
        response_ = re.search('jsonp105[(](.*)[)]', response, re.S).group(1)
        data = json.loads(response_)['data']
        for j in range(len(data)):
            name = data[j]['name']  # 产品名称
            image = data[j]['image']  # 产品图片
            curr_money = data[j]['curr_money']  # 已筹金额
            buy_amount = data[j]['buy_amount']  # 支持人数
            finish_per = data[j]['finish_per']  # 达成率
            remain_day = data[j]['remain_day']  # 还剩多少时间
            status = data[j]['status']  # 项目状态
            target_money = data[j]['target_money']  # 预计的众筹金额
            link = data[j]['link']  # 详情页的链接

            # 将所有数据放在字典中写入json文件
            crowd_funding = dict(zip(['name', 'image', 'curr_money', 'buy_amount', 'finish_per',
                                      'remain_day', 'status', 'target_money', 'link'],
                                     [name, image, curr_money, buy_amount, finish_per,
                                      remain_day, status, target_money, 'link']))
            # 将字典转换成字符串方便写入文件中
            json_str = json.dumps(crowd_funding)
            with open('./data/淘宝众筹科技.json', 'a') as f_:
                print("正在导出第%d页第%d个项目" % (i, j + 1))
                f_.write(json_str + ',')

    print('OK---' + '导出成功！！！')
