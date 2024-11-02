# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    Name = scrapy.Field()  # 公司名称
    Status = scrapy.Field()  # 登记状态
    ShortStatus = scrapy.Field() # 状态简称
    RegistCapi = scrapy.Field()  # 注册资本
    StartDate = scrapy.Field()  # 成立日期
    CreditCode = scrapy.Field() # 统一社会代码
    Address = scrapy.Field() # 公司地址
    Province = scrapy.Field() # 省份
    City = scrapy.Field() # 城市
    Industry = scrapy.Field() # 行业
    SubIndustry = scrapy.Field() # 子行业
    KeyNo = scrapy.Field() # 企业编码
    Scale = scrapy.Field() # 企业类型
    Scope = scrapy.Field() # 经营描述
    RiskFlag = scrapy.Field() # 风险类型
    QccAnIndustry = scrapy.Field() # 企查查an分类
    QccBnIndustry = scrapy.Field() # 企查查bn分类
    QccCnIndustry = scrapy.Field() # 企查查cn分类
    QccDnIndustry = scrapy.Field() # 企查查dn分类
    pass
