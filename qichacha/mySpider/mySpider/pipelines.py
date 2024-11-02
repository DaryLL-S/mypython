# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from idlelib.iomenu import encoding

# useful for handling different item types with a single interface
import pandas as pd


class MyspiderPipeline:
    headers = ['Name', 'Status', 'ShortStatus',
               'RegistCapi', 'StartDate', 'CreditCode',
               'Address', 'Province', 'City',
               'Industry', 'SubIndustry', 'KeyNo',
               'Scale', 'Scope', 'RiskFlag', 'QccAnIndustry',
               'QccBnIndustry', 'QccCnIndustry', 'QccDnIndustry']
    df = pd.DataFrame(data=None, columns=headers)

    def __init__(self):
        pass

    def process_item(self, item, spider):
        data = dict(item)
        self.df = self.df._append(data, ignore_index=True)

        return item

    def close_spider(self, spider):
        self.df.to_csv('data.csv', encoding='utf-8', mode='a+', index=False)
        self.df = None
        print('data.csv文件写入完成')
