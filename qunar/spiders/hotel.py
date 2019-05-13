# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from qunar.items import CityItem

class HotelSpider(scrapy.Spider):
    # 爬虫名称
    name = 'hotel'
    # 爬虫的可信域名
    allowed_domains = ['bnb.qunar.com']
    # 爬虫的url集合
    start_urls = ['http://bnb.qunar.com/hotcity.jsp']

    def parse(self, response):
        '''
        解析html获取所需数据
        '''

        # 爬取下来的html代码
        html = response.text
        soup = BeautifulSoup(html, "html5lib")
        # 获取包裹所有数据的div
        div_b_allcity = soup.find('div', class_='b_allcity')
        # 实列化一个item
        item = CityItem()
        # 判断是否存在此盒子
        #（其实这里也可以不用加这个判断，因为它是肯定存在的，我这里加上去算是培养自己一个习惯吧，去获取的内容都进行判断，防止内容标签不存在而产生错误）
        if div_b_allcity is not None:
            # 找到所有class="e_city_name clr_after"的div 
            # (其实，这里可以直接写成“for li_item in div_b_allcity.find_all('li'):”找到所有li,这里分开写是为了可以更直观的理解)
            for div_cityItem in div_b_allcity.find_all('div'):
                # 跟上面判断一样
                if div_cityItem is not None:
                    ul = div_cityItem.find('ul')
                    if ul is not None:
                        for li_item in ul.find_all('li'):
                            # 跟上面判断一样
                            if li_item is not None:
                                # 获取城市名称
                                item['name'] = li_item.find('a').get_text()
                                # 获取城市对应url
                                item['url'] = li_item.find('a').get('href')
                                # print(item)
                                # 返回数据
                                yield item

