# -*- coding: utf-8 -*-
import requests
import scrapy
import time
from bs4 import BeautifulSoup
from scrapy_boss_job.items import ScrapyBossJobItem

class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/job_detail/?query=%E6%B5%8B%E8%AF%95&scity=101010100']

    def parse(self, response):
        # 1)拼接访问职位详细信息url
        # 1.1)获取职位信息
        job_lists = response.xpath("//div[@class='job-list']/ul/li")

        header = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, sdch',
            'accept-language': 'zh-CN,zh;q=0.8',
            'cache-control': 'no-cache',
            'cookie': '_uab_collina=154090582136258670548877; __c=1546326908; __g=-; lastCity=101010100; __l=l=%2Fwww.zhipin.com%2F&r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DeX2Mlqr8Pb1ou3MSd3EYmhl9ui4MM7T85stLcjNTn7hcOnoX4a8M9-zzji_KhMwa%26wd%3D%26eqid%3Db1c280bd00060203000000035c2b1376; __a=18247292.1540905819.1544448183.1546326908.115.5.24.115; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1544339000,1544448184,1546326907; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1546339873; toUrl=https%3A%2F%2Fwww.zhipin.com%2Fjob_detail%2F132c9497aed0b5da1HV_2dq6EFE%7E.html%3Fka%3Dsearch_list_1_blank%26lid%3D1geJXaYQuSB.search; JSESSIONID=""',
            'pragma': 'no-cache',
            'referer': 'https://www.zhipin.com/job_detail/132c9497aed0b5da1HV_2dq6EFE~.html?ka=search_list_1_blank&lid=1geJXaYQuSB.search',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
            'x-requested-with': 'XMLHttpRequest',
        }

        # 获取职位信息列表中当前条
        for job in job_lists:
            # 加载数据保存项
            job_item = ScrapyBossJobItem()
            # 数据解析
            urls = job.xpath(".//div[@class='job-primary']/div[@class='info-primary']/h3/a/@href").extract_first()
            kas = job.xpath(".//div[@class='job-primary']/div[@class='info-primary']/h3/a/@ka").extract_first()
            lids = job.xpath(".//div[@class='job-primary']/div[@class='info-primary']/h3/a/@data-lid").extract_first()
            # 职位拼接
            url = 'https://www.zhipin.com' + ''.join(urls) + '?ka=' + ''.join(kas) + '&lid=' + ''.join(lids)
            print(url)
            response = requests.get(url,headers = header)  # 发送请求
            soup = BeautifulSoup(response.text, 'lxml')
            # 组装属性
            position = soup.select('.name > h1')
            salary = soup.select('.badge')
            counts = soup.select('.job-primary .info-primary > p')
            skill_label = soup.select('.job-tags > span')
            welfare_label = soup.select('.job-sec > .job-tags > span')
            job_description = soup.select('.job-sec > .text')
            company_namex = soup.select('.info-company > .name > a')
            xwork_address = soup.select('.location-address')

            for position, salary, skill_label, welfare_label, job_description, company_namex, xwork_address in zip(position, salary, skill_label, welfare_label, job_description, company_namex, xwork_address):
                job_item['position'] = position.get_text()
                job_item['salary'] = salary.get_text().strip()
                job_item['need'] = counts[0].get_text()
                job_item['skill_label'] = skill_label.get_text().strip()
                job_item['welfare_label'] = welfare_label.get_text().strip()
                job_item['job_description'] = job_description.get_text().strip()
                job_item['company_name'] = company_namex.get_text().strip()
                job_item['work_address'] = xwork_address.get_text().strip()
                # 累了你就歇一会
                time.sleep(100)
                # 提交管道
                yield job_item
        # 下一页数据
        next_link = response.xpath("//div[@class='job-list']/div[@class='page']/a[@class='next']/@href")
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://www.zhipin.com/job_detail/?query=%E6%B5%8B%E8%AF%95&scity=101010100" + next_link,
                                 callback=self.parse)

