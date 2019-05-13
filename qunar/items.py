# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QunarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CityItem(scrapy.Item):
    name = scrapy.Field()		# 城市名称
    url = scrapy.Field()		# 城市对应url



class ScenicItem(scrapy.Item):
    sightId = scrapy.Field()        # 识别码
    province = scrapy.Field()		# 省
    city = scrapy.Field()			# 市
    name = scrapy.Field()			# 景点名称
    url = scrapy.Field()			# 景点URL
    address = scrapy.Field()		# 景点地点
    grade = scrapy.Field()			# 景点评分
    describe = scrapy.Field()		# 景点描述
    price = scrapy.Field()			# 最低价
    tickets = scrapy.Field()        # 门票
    comment = scrapy.Field()        # 评论



class TicketsItem(scrapy.Item):
    name = scrapy.Field()           # 门票名称
    type = scrapy.Field()           # 门票类型
    state = scrapy.Field()          # 门票说明
    price = scrapy.Field()          # 价钱
    bookingSites = scrapy.Field()   # 预订网站
    bookingUrl = scrapy.Field()     # 网站URL