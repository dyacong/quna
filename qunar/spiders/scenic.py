# -*- coding: utf-8 -*-
import re
import json
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from qunar.items import ScenicItem
from qunar.items import TicketsItem


class ScenicSpider(scrapy.Spider):
    name = 'scenic'
    allowed_domains = ['piao.qunar.com']
    # 景点门票url前缀，获取下一页需要
    starturl = 'http://piao.qunar.com'
    # 爬取评论url，这里评论是直接找去接口获得的，这样的做法也是比较有效率的。
    comment_url = 'http://piao.qunar.com/ticket/detailLight/sightCommentList.json'


    def __init__(self):
        '''
        设置爬虫时的头部请求信息
        '''
        self.headers = {
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding':'gzip, deflate',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            }

    def start_requests(self):
        '''
        重组url
        '''
        # 根据输入获取你要爬取不懂地方的景点门票信息，什么都不输入表示爬取全国景点信息
        print('爬取城市景点：')
        city = input()
        self.url = 'http://piao.qunar.com/ticket/list.htm?keyword='+ city +'&region='+ city +'&from=mpshouye_hotcity'
        yield Request(self.url, self.parse)


    def parse(self, response):
        '''
        获取景点url
        '''
        html = response.text
        soup = BeautifulSoup(html, "html5lib")
        content = soup.find('div', class_='result_list')
        for item_div in content.find_all('div', class_='sight_item_detail'):
            url = self.starturl + item_div.find('h3').find('a').get('href')
            # 进入详情页，爬取我们所需信息
            yield Request(url, self.Scenic_Info)
        # 判断是否有下一页
        if soup.find('a', class_='next') is not None:
            page = soup.find('a', class_='next').get('data-pager-pageno')
            yield Request(self.url + '&page='+ page, self.parse)




    def Scenic_Info(self, response):
        '''
        获取景点基本信息
        '''
        html = response.text
        soup = BeautifulSoup(html, "html5lib")
        item = ScenicItem()
        # 获取景点名称
        if soup.find('span', class_='mp-description-name') is not None:
            item['name'] = soup.find('span', class_='mp-description-name').get_text()
            print('景点名称:' + item['name'])

        # 获取景点地点
        if soup.find('span', class_='mp-description-address') is not None:
            item['address'] = soup.find('span', class_='mp-description-address').get_text()
            print('景点地点:' + item['address'])

        # 获取景点介绍
        if soup.find('div', class_='mp-description-onesentence') is not None:
            item['describe'] = soup.find('div', class_='mp-description-onesentence').get_text()
            print('景点介绍:' + item['describe'])

        # 获取景点评分
        if soup.find('span', id='mp-description-commentscore') is not None:
            item['grade'] = soup.find('span', id='mp-description-commentscore').find('span').get_text()
            print('景点评分:' + item['grade'])

        # 获取景点最低价钱
        if soup.find('span', class_='mp-description-qunar-price') is not None:
            item['price'] = soup.find('span', class_='mp-description-qunar-price').find('em').get_text()
            print('最低价钱:' + item['price'])

        # 获取省份和城市
        scripts = soup.find_all('script')
        if scripts is not None:
            for script in scripts:
                if script.get_text() is not '':
                    content = script.get_text().replace(' ', '').replace('\n', '');
                    pattern = re.compile('"locInfo":(.*?),"sightInfo":(.*?),"spotAnnouncement"', re.S)
                    pattern_items = re.findall(pattern, content)
                    for pattern_item in pattern_items:
                        locInfo = json.loads(pattern_item[0])
                        sightInfo = json.loads(pattern_item[1])
                        item['sightId'] = sightInfo['sightId']
                        item['city'] = locInfo['city']
                        item['province'] = locInfo['province']
                        print('sightId:' + item['sightId'])
                        print('city:' + item['city'])
                        print('province:' + item['province'])

        # 获取门票信息
        tickets_node = soup.find_all('div', class_='mp-tickettype')
        if tickets_node is not None:
            tickets = TicketsItem()
            for ticket_node in tickets_node:
                head = ticket_node.find('div', class_='mp-tickettype-head')
                if head is not None:
                    ticket_type = head.get('data-catename')
                    if ticket_type is not None:
                        # 门票类型
                        tickets['type'] = ticket_type
                        ticket_content = ticket_node.find_all('div', class_='mp-tickettype-group')
                        if ticket_content is not None:
                            for content in ticket_content:
                                infos_node = content.find_all('div', class_='mp-ticket')
                                if infos_node is not None:
                                    for info_node in infos_node:

                                        # 预订网站
                                        if info_node.find('span', class_='mp-supplier-logo') is not None:
                                            tickets['bookingSites'] = info_node.find('span', class_='mp-supplier-logo').get_text()
                                            print('预订网站:' + tickets['bookingSites'])

                                        # 门票名称
                                        if info_node.find('div', class_='mp-ticket-title') is not None:
                                            tickets['name'] = info_node.find('div', class_='mp-ticket-title').get_text()
                                            print('门票名称:' + tickets['name'])

                                        # 门票说明
                                        if info_node.find('div', class_='mp-ticket-tags') is not None:
                                            spans = info_node.find('div', class_='mp-ticket-tags').find_all('span')
                                            state = ''
                                            for span in spans:
                                                if span.get('data-c') is not None:
                                                    state += span.get('data-c') +'\t'
                                            tickets['state'] = state.replace('\t', ' ').replace('<br/>', ' ').split(' ')
                                            print('state:' + tickets['state'])

                                        if info_node.find('div', class_='mp-group-price') is not None:
                                            # 价钱
                                            if info_node.find('div', class_='mp-group-price').find('em', class_='mp-ticket-bluetxt') is not None:
                                                tickets['price'] = info_node.find('div', class_='mp-group-price').find('em', class_='mp-ticket-bluetxt').find('strong').get_text()
                                                print('价钱:' + tickets['price'])

                                            # 网站URL
                                            if info_node.find('div', class_='mp-group-price') is not None:
                                                tickets['bookingUrl'] = info_node.find('div', class_='mp-group-price').find('a').get('href')
                                                print('网站URL:' + tickets['bookingUrl'])
                                item['tickets'] = tickets
        # 获取评论
        try:
            '''
            通过识别码获取该景点的相关评论，其中：
            sightId：景点的识别码
            index：实际页码
            page：页面显示的页码数，不过直接使用接口爬取，这个就可以不需要了，带与不带对结果没有影响
            pageSize：没有显示数，评论太多了，这里我选择只爬取前100条
            tagType：指评论的类型，0表示全部，具体可以将URL直接放进浏览器，返回数据有都有写出来，我就不一一写出了。
            '''
            url = self.comment_url + '?sightId=' + item['sightId'] + '&index=1&page=1&pageSize=100&tagType=0'
            yield Request(url=url, meta={'item': item}, callback=self.comment_Info)
        except:
            # 这里我一直不太明白为什么老是出现空的对象，我愚钝的理解可能是因为scrapy速度太快了。
            print(item)



    def comment_Info(self, response):
        '''
        获取评论信息
        '''
        item = response.meta['item']
        comment_content = json.loads(response.text)
        data = comment_content['data']
        commentList = data['commentList']
        comment_data = ''
        for comment in commentList:
            comment_data += comment['content']
        item['comment'] = self.cleaning_data(comment_data)
        print(item)



    def cleaning_data(self, data):
        '''
        对数据进行清洗，将标点符号等对词频统计造成影响的因素剔除
        '''
        pattern = re.compile(r'[一-龥]+')
        return re.findall(pattern, data)