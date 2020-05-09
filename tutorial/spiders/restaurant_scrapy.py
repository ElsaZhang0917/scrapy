# /usr/bin/python 3.7
# -*-coding:utf-8*-

"""
@author: Qiandan Zhang
"""

import sys
import scrapy
import time
import re
from copy import deepcopy
from fontTools.ttLib import TTFont
from lxml import etree
import random

sys.path.append("../")
from tutorial.items import RestaurantItem
from tutorial.trans_cookie import transCookie
from tutorial.get_ip import Proxy


def get_font():
    """
    解密数字
    :return:
    """
    font = TTFont('数字.woff')
    font_names = font.getGlyphOrder()
    # 这些文字就是在FontEditor软件打开字体文件后看到的文字名字
    texts = ['', '', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    font_name = {}
    # 将字体名字和它们所对应的乱码构成一个字典
    for index, value in enumerate(texts):
        a = font_names[index].replace('uni', '&#x').lower() + ";"
        font_name[a] = value
    return font_name


code = get_font()
proxy = Proxy()
proxy.get_ip()


class RestaurantScrapy(scrapy.Spider):
    name = 'restaurant'
    allowed_domains = ['dianping.com']
    start_urls = ['http://www.dianping.com/shenzhen/ch10/g508r12333o2p3']
    cookie = [
        # 's_ViewType=10; _lxsdk_cuid=16c41762058c8-011dc18a778b46-37607c05-13c680-16c41762058c8; _lxsdk=16c41762058c8-011dc18a778b46-37607c05-13c680-16c41762058c8; _hc.v=5334a01a-096f-c7b1-fac3-c8704242adf5.1564466356; Hm_lvt_e6f449471d3527d58c46e24efb4c343e=1568084367; t_lxid=171960fc2d5c8-0a8f1560c40969-396d7500-13c680-171960fc2d5c8-tid; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; fspop=test; cy=7; cye=shenzhen; dplet=229917e2f30a0a735e8db1f26585bdd6; dper=670803721757c4e3d469d5fd32049acae31d870c27bcc1d06412cb1d43930148e05758fa395173c5451d2051446dce0f9a93855d8eaf7686c322a895a2ae68c3abd9bd438ec666e8c349a1d78ac6b0183512071694e9dda190a22cebc7593b0a; ll=7fd06e815b796be3df069dec7836c3df; ua=chnbs2010; ctu=576e984bd70e8ab0a9a172f00099ac0a2f2f1e60050c726b1152125d9fb529a9; _lxsdk_s=171a0c2fac9-56a-967-5a2%7C%7C20',
        'showNav=#nav-tab|0|1; navCtgScroll=0; showNav=javascript:; navCtgScroll=0; _lxsdk_cuid=16f08272e5dc8-0a7fa797654a26-1c3f6a5a-1aeaa0-16f08272e5dc8; _lxsdk=16f08272e5dc8-0a7fa797654a26-1c3f6a5a-1aeaa0-16f08272e5dc8; _hc.v=bdf9071a-fad7-2616-2606-4e67d0f1ea2b.1576389784; cy=7; cye=shenzhen; s_ViewType=10; t_lxid=1719ac52a93c8-0e251eba695ead-396e7507-1aeaa0-1719ac52a93c8-tid; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_6884594313; ctu=81abb58f8dc816d0ae8bf04402d12ff04e0f440b174c52c74484a97684f9bf50; dplet=796057e368eead53acb31d49a54c9e6d; dper=26f7be90c8fd77a6e45b004e14cfe17bbfbd084e12d568222004e2ff18ef2adbe12007431462786c58074213decdc8605e8de92d73dca9970cd25b68253a55671bef34e9eca0d2b86efc7d94115ccac7bb032561ad3d5e0befb5c338668c4cf1; _lxsdk_s=171c91663ce-ea0-e7b-611%7C%7C23'
        ]
    cookie_dict = []
    for c in cookie:
        trans_cookie = transCookie(c)
        cookie_dict.append(trans_cookie.stringToDict())

    def parse(self, response):
        type_list = response.xpath('//div[@id="classfy"]/a')
        for tp in type_list:
            restaurant_type = tp.re_first(r"cate_(.*)_click")
            if restaurant_type in ['小吃快餐', '粥粉面', '水果生鲜']:
                continue
            type_link = tp.xpath('.//@href').extract_first()
            item = RestaurantItem()

            item['restaurant_type'] = restaurant_type

            headers = {'cookies': random.choice(self.cookie)}
            yield scrapy.Request(url=type_link, callback=self.type_parse, meta={'item': deepcopy(item)},
                                 headers=headers, dont_filter=True)

    def type_parse(self, response):
        item = response.meta['item']
        district_list = response.xpath('//div[@id="region-nav"]/a')
        for district in district_list:
            district_loc = district.xpath('.//@data-click-title').extract_first()
            if district_loc in ['坪山区', '光明区', '盐田区', '龙华区']:
                continue
            district_link = district.xpath('.//@href').extract_first()
            district_link += 'p9'

            item['district'] = district_loc
            headers = {'cookies': random.choice(self.cookie)}
            yield scrapy.Request(url=district_link, callback=self.district_parse, meta={'item': deepcopy(item)},
                                 headers=headers, dont_filter=True)

    def district_parse(self, response):
        text = response.text
        item = response.meta['item']
        # replace number
        for key in code:
            if key in text:
                text = text.replace(key, str(code[key]))
        html = etree.HTML(text)
        restaurant_list = html.xpath('//div[@class="shop-list J_shop-list shop-all-list"]//li')
        for res in restaurant_list:
            item['city'] = '深圳'
            item['restaurant_name'] = res.xpath('.//div[@class="tit"]//h4/text()')[0]
            item['address'] = res.xpath('.//div[@class="operate J_operate Hide"]//a//@data-address')[0]
            stars = res.xpath(".//div[@class='nebula_star']//text()")
            for i in stars:
                tmp = re.findall(r'\b\d+\b', i)
                if tmp:
                    item['score'] = tmp[0] + '.' + tmp[1]

            # average price
            avg = res.xpath(".//a[@data-click-name='shop_avgprice_click']//text()")
            avg_price = []
            for i in avg:
                tmp = re.findall(r'\d+', i)
                avg_price = avg_price + tmp
            item['avg_price'] = ''.join(avg_price)

            # review number
            review = res.xpath(".//a[@data-click-name='shop_iwant_review_click']//text()")
            review_num = []
            for i in review:
                tmp = re.findall(r'\d+', i)
                review_num = review_num + tmp
            item['review_num'] = ''.join(review_num)

            # taste, environment, service rating
            comment_rating = res.xpath(".//span[@class='comment-list']//text()")
            string = ''
            for i in comment_rating:
                string += i
            string = string.strip().replace(' ', '').replace('\n', ';')
            string_list = string.split(';')
            for s in string_list:
                if '口味' in s:
                    item['taste_rating'] = s.split('味')[1]
                if '环境' in s:
                    item['environment_rating'] = s.split('境')[1]
                if '服务' in s:
                    item['service_rating'] = s.split('务')[1]

            yield item

        # next page
        next_page = response.xpath('//div[@class="page"]/a[@class="next"]/@href').extract_first()
        if next_page:
            time.sleep(random.randint(1, 15))
            page_num = response.xpath('//div[@class="page"]/a[@class="next"]/@data-ga-page').extract_first()
            print('Start to scrap page {} !'.format(page_num))
            headers = {'cookies': random.choice(self.cookie)}
            yield scrapy.Request(url=next_page, callback=self.parse, headers=headers)
