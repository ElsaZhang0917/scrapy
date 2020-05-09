# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ResidentialItem(scrapy.Item):
    district = scrapy.Field()
    area = scrapy.Field()
    house_name = scrapy.Field()
    address = scrapy.Field()
    avg_price = scrapy.Field()
    build_year = scrapy.Field()
    builder_type = scrapy.Field()
    builder = scrapy.Field()
    num_building = scrapy.Field()
    num_house = scrapy.Field()
    num_second_hand = scrapy.Field()
    link = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()


class RestaurantItem(scrapy.Item):
    restaurant_name = scrapy.Field()
    restaurant_type = scrapy.Field()
    district = scrapy.Field()
    score = scrapy.Field()
    address = scrapy.Field()
    taste_rating = scrapy.Field()
    environment_rating = scrapy.Field()
    service_rating = scrapy.Field()
    avg_price = scrapy.Field()
    review_num = scrapy.Field()
    city = scrapy.Field()


class CompanyItem(scrapy.Item):
    company_name = scrapy.Field()
    finance_status = scrapy.Field()
    city = scrapy.Field()
    recruit = scrapy.Field()
    field = scrapy.Field()
    registered_capital = scrapy.Field()
    location = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
