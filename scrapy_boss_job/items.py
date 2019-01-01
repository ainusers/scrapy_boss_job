# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyBossJobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 定义要抓取的内容
    position = scrapy.Field()        #职位
    salary = scrapy.Field()         #薪资
    need = scrapy.Field()           #城市,经验,学历
    # city = scrapy.Field()           #城市
    # experience = scrapy.Field()     #经验
    # education = scrapy.Field()      #学历
    skill_label = scrapy.Field()    #技能标签
    company_name = scrapy.Field()   #公司名称
    job_description = scrapy.Field()#职位描述
    welfare_label = scrapy.Field()  #福利标签
    work_address = scrapy.Field()   #工作地址
