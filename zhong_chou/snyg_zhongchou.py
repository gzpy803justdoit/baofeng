import re
import requests
import lxml
import json

from lxml import etree

if __name__ == '__main__':
    for i in range(1, 12):
        url = "https://zc.suning.com/project/browseList.htm?c=01&pageNumber=%d" % i
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
        }
        response = requests.get(url, headers=header).content.decode('utf-8')
        my_tree = lxml.etree.HTML(response)

        flag = 0
        info_list = my_tree.xpath('//div[@class="item-list"]//li')
        for info in info_list:
            # 项目名称
            name = info.xpath('.//p[@class="item-name"]/@title')[0]
            # 项目状态
            item_status = info.xpath('.//div[@class="item-status"]/text()')
            if len(item_status) == 0:
                item_status = "即将开始"
                flag = 1  # 代表是项目即将开始
            else:
                item_status = item_status[0].strip()
                if len(item_status) == 4:
                    flag = 2  # 代表项目成功
                else:
                    flag = 3  # 众筹中
            # 关注度
            if flag == 3:
                follow = info.xpath('.//div[@class="item-num"][1]/span[2]/b/text()')[0]
            else:
                follow = info.xpath('.//div[@class="item-num"][1]/span[1]/b/text()')[0]
            # 剩余天数
            if flag == 3:
                fr_ = info.xpath('.//div[@class="item-num"][1]/span[1]/b/text()')  # 剩余天数
                fr = "剩余" + re.compile("\d+").findall(fr_[0])[0] + "天"  # 用正则表达是匹配出期中的数字
            else:
                fr = 0
            # 支持度
            if flag == 1:
                support = 0
            elif flag == 2:
                support = info.xpath('.//div[@class="item-num"][1]/span[2]/b/text()')[0]
            else:
                support = info.xpath('.//div[@class="item-num"][1]/span[3]/b/text()')[0]
            # 已筹集 达成比例
            if flag == 1:
                item_num = 0
                item_finish = 0
            else:
                item_num = info.xpath('.//div[@class="item-num"][2]/span[2]/strong/text()')[0]
                item_finish = info.xpath('.//div[@class="item-num"][2]/span[1]/strong/text()')[0]
                # 将所有数据放在字典中写入json文件
                crowd_funding = dict(zip(['name', 'item_status', 'follow', 'fr', 'support', 'item_num', 'item_finish'],
                                         [name, item_status, follow, fr, support, item_num, item_finish]))
                json_str = json.dumps(crowd_funding)
                if i == 1:
                    with open('./data/苏宁易购众筹科技.json', 'w') as f1:
                        f1.write("[\n")
                else:
                    with open('./data/苏宁易购众筹科技.json', 'a') as f2:
                        f2.write(json_str + ',\n')

    with open('./data/苏宁易购众筹科技.json', 'a') as f_:
        f_.write("]")
