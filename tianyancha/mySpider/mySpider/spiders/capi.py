import requests
import scrapy
from lxml import etree


class CapiSpider(scrapy.Spider):
    name = "capi"
    allowed_domains = ["capi.tianyancha.com"]
    # start_urls = ["https://capi.tianyancha.com/cloud-tempest/web/searchCompanyV4"]
    # payload = {
    #     "filterJson": "{\"economicTypeMethod\":{\"key\":\"economicTypeMethod\",\"items\":[{\"value\":\"1\"}]},\"institutionTypeMethod\":{\"key\":\"institutionTypeMethod\",\"items\":[{\"value\":\"1\"}]},\"word\":{\"key\":\"word\",\"items\":[{\"value\":\"\"}]},\"areaCode\":{\"key\":\"areaCode\",\"items\":[{\"value\":\"00530000V2020\",\"childList\":[{\"value\":\"00530100V2020\"}]}]}}",
    #     "searchType": 1, "sessionNo": "1729691994.90375883", "allowModifyQuery": 1,
    #     "reportInfo": {"page_id": "SearchResult", "page_name": "主搜搜索结果页", "tab_id": "company",
    #                    "tab_name": "公司", "search_session_id": "1729691994.90375883", "distinct_id": "271654935"},
    #     "pageNum": 1, "pageSize": 20}

    start_urls = ['https://www.tianyancha.com/nsearch?key=%E6%B7%B1%E5%9C%B3%E5%B8%82%E6%8E%92%E6%8E%92%E7%BD%91%E6%8A%95%E8%B5%84%E7%AE%A1']
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,es-ES;q=0.5,es;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically

    'DNT': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',}

    cookies = {
        'ssuid': '7989567500',
        'jsid': 'SEO-BING-ALL-SY-000001',
        'TYCID': '88f37310898011ef970de512ec5708f5',
        'Hm_lvt_e92c8d65d92d534b0fc290df538b4758': '1728837063',
        '_ga': 'GA1.2.2109916224.1728837063',
        'CUID': '93a403aa8e602941b2bb2c481a1db90a',
        'tyc-user-phone': '%255B%252213163426219%2522%252C%2522188%25202334%25200959%2522%255D',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22271654935%22%2C%22first_id%22%3A%2219286b80ebac89-013c78852982007-4c657b58-3686400-19286b80ebb2500%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkyODZiODBlYmFjODktMDEzYzc4ODUyOTgyMDA3LTRjNjU3YjU4LTM2ODY0MDAtMTkyODZiODBlYmIyNTAwIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMjcxNjU0OTM1In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22271654935%22%7D%2C%22%24device_id%22%3A%2219286b80ebac89-013c78852982007-4c657b58-3686400-19286b80ebb2500%22%7D',
        'tyc-user-info': '%7B%22state%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22mobile%22%3A%2218823340959%22%2C%22userId%22%3A%22271654935%22%7D',
        'tyc-user-info-save-time': '1729691892057',
        'auth_token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgyMzM0MDk1OSIsImlhdCI6MTcyOTY5MTg5MSwiZXhwIjoxNzMyMjgzODkxfQ.XsTaoMNvNuqQC7EPoIY_C_17RKnwJ9jSMx8GZYnoujY_6c_LkGjXm0xrP5Wi-WChwLrUAfydSOvkJ5IysB_pJA',
        'HWWAFSESTIME': '1730305475180',
        'HWWAFSESID': 'f9da116fbc943b7bff9',
        'csrfToken': 'ectY6KG3X-hvg6P3nT7RUShz',
        'bannerFlag': 'true',
        'searchSessionId': '1730306692.10298397',
    }

    params = {
        'key': '深圳市排排网投资管',
    }

    def parse(self, response):
        self.mytest()


    def mytest(self):
        response = requests.get('https://www.tianyancha.com/nsearch', params=self.params, cookies=self.cookies,
                                headers=self.headers)
        response.encoding = 'utf-8'
        response = response.text.replace('<em>', '')
        # print(response.text)
        html = etree.HTML(response)
        companyList = html.xpath(
            '//*[@id="page-container"]/div/div/div/div/div/div/div/div/div/div/div/a/span//text()')
        print(companyList)
