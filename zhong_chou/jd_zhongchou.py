import json
import requests
import lxml

from lxml import etree

if __name__ == '__main__':
    crowd_funding = []
    for i in range(1, 101):
        url = "https://z.jd.com/bigger/search.html?categoryId=10&from=header&page=%d" % i
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
        }
        response = requests.get(url, headers=header).content.decode('utf-8')
        my_tree = lxml.etree.HTML(response)
        info_list1 = my_tree.xpath('//ul[@class="infos clearfix"]//li[@class="info type_now"]')  # 众筹中
        info_list2 = my_tree.xpath('//ul[@class="infos clearfix"]//li[@class="info type_future"]')  # 预热中
        info_list3 = my_tree.xpath('//ul[@class="infos clearfix"]//li[@class="info type_succeed"]')  # 众筹成功
        info_list4 = my_tree.xpath('//ul[@class="infos clearfix"]//li[@class="info type_xm"]')  # 项目成功
        type_info = []

        for info1 in info_list1:
            one_url = "https://z.jd.com" + info1.xpath('./a[1]/@href')[0]
            img = info1.xpath('.//a[1]/img/@data-original')[0]
            name = info1.xpath('.//h4[@class="link-tit"]/@title')[0]
            # 已达
            fore1 = info1.xpath('.//li[@class="fore1"]/p[1]/text()')[0]
            # 已筹
            fore2 = info1.xpath('.//li[@class="fore2"]/p[1]/text()')[0]
            # 剩余时间
            fore3 = info1.xpath('.//li[@class="fore3"]/p[1]/text()')[0]
            type_now = dict(zip(['name', 'img', 'get_percentage', 'get_money', 'need_time', 'url'],
                                [name, img, fore1, fore2, fore3, one_url]))
            type_info.append(type_now)

        for info2 in info_list2:
            one_url = "https://z.jd.com" + info2.xpath('./a[1]/@href')[0]
            img = info2.xpath('.//a[1]/img/@data-original')[0]
            name = info2.xpath('.//h4[@class="link-tit"]/@title')[0]
            # 已达
            fore1 = info2.xpath('.//li[@class="fore1"]/p[1]/text()')[0]
            # 已筹
            fore2 = info2.xpath('.//li[@class="fore2"]/p[1]/text()')[0]
            # 剩余时间
            fore3 = info2.xpath('.//li[@class="fore3"]/p[1]/text()')[0]
            type_future = dict(zip(['name', 'img', 'get_percentage', 'get_money', 'need_time', 'url'],
                                   [name, img, fore1, fore2, fore3, one_url]))
            type_info.append(type_future)

        for info3 in info_list3:
            one_url = "https://z.jd.com" + info3.xpath('./a[1]/@href')[0]
            img = info3.xpath('.//a[1]/img/@data-original')[0]
            name = info3.xpath('.//h4[@class="link-tit"]/@title')[0]
            # 已达
            fore1 = info3.xpath('.//li[@class="fore1"]/p[1]/text()')[0]
            # 已筹
            fore2 = info3.xpath('.//li[@class="fore2"]/p[1]/text()')[0]
            # 剩余时间
            fore3 = info3.xpath('.//li[@class="fore3"]/p[1]/text()')[0]
            type_succeed = dict(zip(['name', 'img', 'get_percentage', 'get_money', 'need_time', 'url'],
                                    [name, img, fore1, fore2, fore3, one_url]))
            type_info.append(type_succeed)

        for info4 in info_list4:
            one_url = "https://z.jd.com" + info4.xpath('./a[1]/@href')[0]
            img = info4.xpath('.//a[1]/img/@data-original')[0]
            name = info4.xpath('.//h4[@class="link-tit"]/@title')[0]
            # 已达
            fore1 = info4.xpath('.//li[@class="fore1"]/p[1]/text()')[0]
            # 已筹
            fore2 = info4.xpath('.//li[@class="fore2"]/p[1]/text()')[0]
            # 剩余时间
            fore3 = info4.xpath('.//li[@class="fore3"]/p[1]/text()')[0]
            type_xm = dict(zip(['name', 'img', 'get_percentage', 'get_money', 'need_time', 'url'],
                               [name, img, fore1, fore2, fore3, one_url]))
            type_info.append(type_xm)

        # 注意extend和 append的区别
        crowd_funding.extend(type_info)
        print(len(crowd_funding))

    # 将该列表打印出json文本
    json_str = json.dumps(crowd_funding)
    with open('./data/京东众筹科技.json', 'w') as f_:
        f_.write(json_str)
        print('OK---' + '导出成功！！！')
