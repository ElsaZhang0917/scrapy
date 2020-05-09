# /usr/bin/python 3.7
# -*-coding:utf-8*-


"""
@author: Qiandan Zhang
"""

from tutorial.items import ResidentialItem
import scrapy
import re
import requests
import time


class HouseSpider(scrapy.Spider):
    name = "house_gz"
    allowed_domains = ["gz.lianjia.com"]
    start_urls = [
        "https://gz.lianjia.com/xiaoqu/"
    ]
    base_url = "https://gz.lianjia.com"

    def parse(self, response):
        district_list = response.xpath('//div[@data-role="ershoufang"]//div//a')

        for district in district_list:
            district_url = district.xpath('.//@href').extract_first()

            district_link = self.base_url + district_url
            yield scrapy.Request(url=district_link, callback=self.district_parse)

    def district_parse(self, response):
        area_list = response.xpath('//div[@data-role="ershoufang"]//div//a')
        for area in area_list:
            title = area.xpath('./@title').extract()
            # 如果title不为空，则是罗湖区等第一层筛选
            if title:
                continue

            area_url = area.xpath('.//@href').extract_first()
            area_link = self.base_url + area_url
            yield scrapy.Request(url=area_link, callback=self.area_parse)

    def area_parse(self, response):
        residential_list = response.xpath('//li[@class="clear xiaoquListItem"]')

        for residential in residential_list:
            residential_link = residential.xpath('./div[@class="info"]/div[@class="title"]/a/@href').extract_first()
            residential_on_sale = \
                residential.xpath('./div[@class="xiaoquListItemRight"]/div[@class="xiaoquListItemSellCount"]/a/span'). \
                    re_first(r">(.*)<")
            item = ResidentialItem()
            item['num_second_hand'] = residential_on_sale
            item['link'] = residential_link
            yield scrapy.Request(url=residential_link, callback=self.residential_parse, meta={'item': item})

        # add next page
        num_page = int(response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data'). \
                       re_first(r"totalPage\":(\d+),"))
        cur_page = int(response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data'). \
                       re_first(r"curPage\":(\d+)"))
        if cur_page < num_page:
            base_link = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-url').extract_first()
            next_link = self.base_url + base_link.format(page=cur_page + 1)
            yield scrapy.Request(url=next_link, callback=self.area_parse)

    def residential_parse(self, response):
        item = response.meta['item']
        loc_list = response.xpath('//div[@class="fl l-txt"]/a').re(r">(.*)<")
        item['district'] = loc_list[2].replace('小区', '')
        item['area'] = loc_list[3].replace('小区', '')
        item['house_name'] = loc_list[4]
        item['address'] = response.xpath('//div[@class="detailDesc"]').re_first(r">(.*)<"). \
            replace('(', '').replace(')', '')
        item['avg_price'] = response.xpath('//span[@class="xiaoquUnitPrice"]').re_first(r">(.*)<")
        detail_info = response.xpath('//span[@class="xiaoquInfoContent"]').re(r">(.*)<")

        build_year = re.findall(r"(\d+)", detail_info[0])
        if build_year:
            item['build_year'] = build_year[0]
        else:
            item['build_year'] = '暂无信息'

        item['builder_type'] = detail_info[1]
        item['builder'] = detail_info[4]
        num_building = re.findall(r"(\d+)", detail_info[5])
        if num_building:
            item['num_building'] = num_building[0]
        else:
            item['num_building'] = '暂无信息'

        num_house = re.findall(r"(\d+)", detail_info[6])
        if num_building:
            item['num_house'] = num_house[0]
        else:
            item['num_house'] = '暂无信息'

        # item['longitude'], item['latitude'] = self.get_info(item['address'])

        yield item

    def get_info(self, address):
        """

        :param address:
        :return:
        """
        url = 'https://restapi.amap.com/v3/geocode/geo?'
        key = '66ab94c72d7c7fb36830b694679e8c14'
        link = '{}address={}&key={}&city=021'.format(url, address, key)

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
