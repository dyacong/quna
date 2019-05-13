# -*- coding: utf-8 -*-

from scrapy.cmdline import execute

print('1--> 景点')
print('2--> 酒店')
print('爬取类型：')
type = input()
if type == '1':
    execute(['scrapy', 'crawl', 'scenic'])
else:
    execute(['scrapy', 'crawl', 'hotel'])