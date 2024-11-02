import time
import random
import requests
import scrapy
import json
import re
import hmac
import hashlib
from mySpider.items import MyspiderItem
from mySpider.util.checkJSON import checkJSON


class QccSpider(scrapy.Spider):
    name = "qcc"
    allowed_domains = ["www.qcc.com"]

    start_urls = ['https://www.qcc.com/api/search/searchMulti']

    # 登录失效更换cookie
    cookie = ''

    def get_pid_tid(self):
        url = 'https://www.qcc.com/web/search/advance?hasState=true'

        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': self.cookie,
            'referer': 'https://www.qcc.com/',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'''
        }

        res = requests.get(url, headers=headers, allow_redirects=False).text
        try:
            pid = re.findall("pid='(.*?)'", res)[0]
            tid = re.findall("tid='(.*?)'", res)[0]
        except:
            pid = ''
            tid = ''

        return pid, tid

    def seeds_generator(self, s):
        seeds = {
            "0": "W",
            "1": "l",
            "2": "k",
            "3": "B",
            "4": "Q",
            "5": "g",
            "6": "f",
            "7": "i",
            "8": "i",
            "9": "r",
            "10": "v",
            "11": "6",
            "12": "A",
            "13": "K",
            "14": "N",
            "15": "k",
            "16": "4",
            "17": "L",
            "18": "1",
            "19": "8"
        }
        seeds_n = 20

        if not s:
            s = "/"
        s = s.lower()
        s = s + s

        res = ''
        for i in s:
            res += seeds[str(ord(i) % seeds_n)]
        return res

    def a_default(self, url: str = '/', data=None):
        if data is None:
            data = {}
        url = url.lower()
        dataJson = json.dumps(data, ensure_ascii=False, separators=(',', ':')).lower()

        hash = hmac.new(
            bytes(self.seeds_generator(url), encoding='utf-8'),
            bytes(url + dataJson, encoding='utf-8'),
            hashlib.sha512
        ).hexdigest()
        return hash.lower()[8:28]

    def r_default(self, url: str = '/', data=None, tid: str = ''):
        if data is None:
            data = {}
        url = url.lower()
        dataJson = json.dumps(data, ensure_ascii=False, separators=(',', ':')).lower()

        payload = url + 'pathString' + dataJson + tid
        key = self.seeds_generator(url)

        hash = hmac.new(
            bytes(key, encoding='utf-8'),
            bytes(payload, encoding='utf-8'),
            hashlib.sha512
        ).hexdigest()
        return hash.lower()

    def make_request(self, data, pid, tid):
        url = 'https://www.qcc.com/api/search/searchMulti'
        headers = {'accept': 'application/json, text/plain, */*', 'accept-encoding': 'gzip, deflate, br',
                   'accept-language': 'zh-CN,zh;q=0.9', 'content-length': '141', 'content-type': 'application/json',
                   'cookie': self.cookie, 'origin': 'https://www.qcc.com',
                   'referer': 'https://www.qcc.com/web/search/advance?hasState=true', 'sec-fetch-dest': 'empty',
                   'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin',
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
                   'x-requested-with': 'XMLHttpRequest', 'x-pid': pid}

        req_url = '/api/search/searchmulti'

        key = self.a_default(req_url, data)
        val = self.r_default(req_url, data, tid)
        headers[key] = val

        # 将 cookie 字符串转换为字典
        cookies = {}
        for cookie_pair in self.cookie.split('; '):
            key, value = cookie_pair.split('=')
            cookies[key] = value

        res = requests.post(url=url, headers=headers, json=data, cookies=cookies, allow_redirects=False).text
        return res

    def parse(self, response):
        # 更换筛选条件
        data = {"pageIndex":1,"pageSize":20,"isAgg":"false","isTable":True,"filter":"{\"i\":[\"J\"],\"et\":[\"002006\"],\"f\":[\"JU\"]}","minLength":1}

        pid, tid = self.get_pid_tid()
        # 任务失败更换起始值
        for i in range(1, 251):
            data['pageIndex'] = i
            res = self.make_request(data, pid, tid)
            myJson = json.loads(res)
            time.sleep(random.randint(3, 5))
            for mylist in myJson["Result"]:
                print(mylist)
                print(myJson["Paging"]["PageIndex"])
                item = MyspiderItem()
                item["Name"] = mylist["Name"] if checkJSON().isExtend(mylist, "Name") else ""  # 公司名称
                item["Status"] = mylist["Status"] if checkJSON().isExtend(mylist, "Status") else ""  # 登记状态
                item["ShortStatus"] = mylist["ShortStatus"] if checkJSON().isExtend(mylist,
                                                                                    "ShortStatus") else ""  # 状态简称
                item["RegistCapi"] = mylist["RegistCapi"] if checkJSON().isExtend(mylist, "RegistCapi") else ""  # 注册资本
                item["StartDate"] = mylist["StartDate"] if checkJSON().isExtend(mylist, "StartDate") else ""  # 成立日期
                item["CreditCode"] = mylist["CreditCode"] if checkJSON().isExtend(mylist,
                                                                                  "CreditCode") else ""  # 统一社会代码
                item["Address"] = mylist["Address"] if checkJSON().isExtend(mylist, "Address") else ""  # 公司地址
                item["Province"] = mylist["Area"]["Province"] if checkJSON().isExtend(mylist, "Province") else ""  # 省份
                item["City"] = mylist["Area"]["City"] if checkJSON().isExtend(mylist, "City") else ""  # 城市
                item["Industry"] = mylist["Industry"]["Industry"] if checkJSON().isExtend(mylist,
                                                                                          "Industry") else ""  # 行业
                item["SubIndustry"] = mylist["Industry"]["SubIndustry"] if checkJSON().isExtend(mylist,
                                                                                                "SubIndustry") else ""  # 子行业
                item["KeyNo"] = mylist["KeyNo"] if checkJSON().isExtend(mylist, "KeyNo") else ""  # 企业编码
                item["Scale"] = mylist["Scale"] if checkJSON().isExtend(mylist, "Scale") else ""  # 企业类型
                item["Scope"] = mylist["Scope"] if checkJSON().isExtend(mylist, "Scope") else ""  # 经营描述
                item["RiskFlag"] = list(map(lambda x: x["Name"], mylist["TagsInfoV2"])) if checkJSON().isExtend(mylist,
                                                                                                                "ShortName") else ""  # 风险类型
                item["QccAnIndustry"] = mylist["QccIndustry"]["An"] if checkJSON().isExtend(mylist,
                                                                                            "An") else ""  # 企查查an分类
                item["QccBnIndustry"] = mylist["QccIndustry"]["Bn"] if checkJSON().isExtend(mylist,
                                                                                            "Bn") else ""  # 企查查bn分类
                item["QccCnIndustry"] = mylist["QccIndustry"]["Cn"] if checkJSON().isExtend(mylist,
                                                                                            "Cn") else ""  # 企查查cn分类
                item["QccDnIndustry"] = mylist["QccIndustry"]["Dn"] if checkJSON().isExtend(mylist,
                                                                                            "Dn") else ""  # 企查查dn分类
                yield item
