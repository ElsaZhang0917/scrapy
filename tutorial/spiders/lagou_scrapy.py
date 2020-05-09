# /usr/bin/python 3.7
# -*-coding:utf-8*-

"""
@author: Qiandan Zhang
"""

import scrapy
from tutorial.items import CompanyItem
import requests
import re
from tutorial.get_ip import Proxy
import time
import random
import csv


# proxy = Proxy()
# proxy.get_ip()


def get_detail_url():
    for finance in range(1, 9):
        for recruit in range(1, 7):
            for area in range(24, 34):
                detail_url = 'https://www.lagou.com/gongsi/3-{}-{}-{}'.format(finance, area, recruit)
                headers = {
                    'User-Agent':
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/80.0.3987.163 Safari/537.36",
                    'Accept':
                        "application/json, text/javascript, */*; q=0.01",
                    'Referer': detail_url}

                page_parse(detail_url, headers)
    print('Successfully get all company links!')


def page_parse(url, headers):
    s = requests.session()
    s.get(url, headers=headers, timeout=3)
    cookie = s.cookies

    all_pages = set()
    for page in range(1, 21):
        first = 'true' if page == 1 else 'false'
        form_data = {'pn': page, 'first': first, 'sortField': 0, 'havemark': 0}

        response = s.post(url, data=form_data, headers=headers, cookies=cookie, timeout=3)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        page_links = re.findall(r'<h3 class="company-name wordCut"><a href=\"(.*\d+).html\" target=', response.text)
        page_links = set(page_links)
        all_pages = all_pages | page_links

    all_pages = list(map(lambda x: [x], all_pages))
    with open('all_pages_sh.csv', mode="a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        for page in all_pages:
            writer.writerow(page)


# get_detail_url()


class LagouScrapy(scrapy.Spider):
    name = 'lagou'
    allow_domains = ['lagou.com']
    urls = []
    with open('all_pages_sh.csv', mode="r") as f:
        for url in f.readlines():
            urls.append(url.strip())
    urls = list(set(urls))
    start_urls = list(map(lambda x: x + '.html', urls))

    def start_requests(self):
        for url in self.start_urls:
            # time.sleep(random.randint(0, 3))
            headers = {
                'User-Agent':
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/80.0.3987.163 Safari/537.36",
                'Accept':
                    "application/json, text/javascript, */*; q=0.01",
                'Referer': url}
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        item = CompanyItem()
        item['company_name'] = response.xpath('//h1[@class="company_main_title"]//@title').extract_first()
        base_info = response.xpath('//div[@id="basic_container"]//li')
        for info in base_info:
            if info.xpath('.//i[@class="type"]'):
                item['field'] = info.xpath('.//span/text()').extract_first()
            if info.xpath('.//i[@class="process"]'):
                item['finance_status'] = info.xpath('.//span/text()').extract_first()
            if info.xpath('.//i[@class="number"]'):
                item['recruit'] = info.xpath('.//span/text()').extract_first()
            if info.xpath('.//i[@class="address"]'):
                item['city'] = info.xpath('.//span/text()').extract_first()

        item['location'] = response.xpath('//li[@class="mlist_ul_li mlist_li_open"]/p[@class="mlist_li_desc"]/text()'). \
            extract_first().strip()
        business_info = response.xpath('//div[@class="company_bussiness_info_container"]/div[@class="info_item"]')
        for info in business_info:
            if info.xpath('.//div[@class="info_item_title"]//span/text()').extract_first() == '注册资本':
                item['registered_capital'] = info.xpath('.//div[@class="content"]/text()').extract_first()
                break
        if item['location']:
            lng, lat = self.get_info(item['location'])
            item['longitude'] = lng
            item['latitude'] = lat

        yield item

    def get_info(self, address):
        """

        :param address:
        :return:
        """
        url = 'https://restapi.amap.com/v3/geocode/geo?'
        key = '66ab94c72d7c7fb36830b694679e8c14'
        link = '{}address={}&key={}&city=755'.format(url, address, key)

        try:
            response = requests.get(link)
            if response.status_code == 200:
                results = response.json()
                if results['status'] == '1':
                    loc = results['geocodes'][0]['location']
                    lng, lat = loc.split(',')[0], loc.split(',')[1]
                    return lng, lat
        except:
            print('!!!')
            time.sleep(1)
            pass

