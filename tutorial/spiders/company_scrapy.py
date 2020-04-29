# /usr/bin/python 3.7
# -*-coding:utf-8*-


import sys
import scrapy
import re
import time
import numpy as np

sys.path.append("../")
from tutorial.items import CompanyItem


class CompanyScrapy(scrapy.Spider):
    name = 'company'
    allowed_domains = ["liepin.com"]
    start_urls = [
                  "https://www.liepin.com/company/converge/1/",
                  "https://www.liepin.com/company/converge/2/"
                  "https://www.liepin.com/company/converge/3/",
                  "https://www.liepin.com/company/converge/4/",
                  "https://www.liepin.com/company/converge/5/",
                  "https://www.liepin.com/company/converge/6/"
        ]
    header = {'User-Agent':
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=self.header)

    def parse(self, response):
        company_list = response.xpath('//ul[@class="clearfix"]/li/a/@href').extract()
        for company in company_list:
            # time.sleep(np.random.randint(low=1, high=3))
            yield scrapy.Request(url=company, dont_filter=True, callback=self.company_parse, headers=self.header)

        # next page
        time.sleep(np.random.randint(low=1, high=10))
        pages = response.xpath('//div[@class="pagerbar"]/a')
        for page in pages:
            if page.xpath('.//text()').extract_first() == '下页':
                next_link = 'https://www.liepin.com' + page.xpath('.//@href').extract_first()
                r = re.compile('curPage=(.*)')
                page_num = r.findall(next_link)[0]
                print('Start to scrapy page {}'.format(page_num))
                yield scrapy.Request(url=next_link, dont_filter=True, callback=self.parse, headers=self.header)

    def company_parse(self, response):
        if response.xpath('//title/text()').extract()[0] == '猎聘:LiePin.com':
            raise Exception

        detail_info = response.xpath('//div[@class="name-and-welfare"]')
        company_name = detail_info.xpath('.//h1/text()').extract_first()
        city = detail_info.xpath('.//a[@class="comp-summary-tag-dq"]/text()').extract_first()
        field = detail_info.xpath('.//a[@data-selector="comp-industry"]/text()').extract_first()
        base_info = detail_info.xpath('.//a[@href="javascript:;"]/text()').extract()
        if city:
            base_info.remove(city)
        if '关注' in base_info:
            base_info.remove('关注')
        if '更多' in base_info:
            base_info.remove('更多')

        # 区分雇员人数和融资状况
        recruit = ''
        for i in base_info:
            temp = re.findall(r"\d+", i)
            if temp:
                recruit = i

        if recruit in base_info:
            base_info.remove(recruit)

        finance_status = ''
        if base_info:
            finance_status = base_info[0]

        if all(list(map(lambda x: x not in city, ['北京', '上海', '深圳', '广州']))):
            raise KeyError
        location = response.xpath('//ul[@class="new-compintro"]/li/text()').extract_first()
        lng, lat = response.xpath('//ul[@class="new-compintro"]/li/@data-point').extract_first().split(',')
        lng = np.round(float(lng), 6)
        lat = np.round(float(lat), 6)
        registered_capital = response.xpath('//ul[@class="new-compdetail"]/li/text()').extract()[1].split('：')[1]

        # create target item
        item = CompanyItem()
        item['city'] = city
        item['company_name'] = company_name
        item['finance_status'] = finance_status
        item['registered_capital'] = registered_capital
        item['recruit'] = recruit
        item['field'] = field
        item['location'] = location
        item['latitude'] = lat
        item['longitude'] = lng

        yield item
