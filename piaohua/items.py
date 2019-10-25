# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PiaohuaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #电影名称
    movename = scrapy.Field()
    # #电影更新日期
    # reloaddate = scrapy.Field()
    #电影详细页url
   # movelink = scrapy.Field()
    #电影下载链接
    movedownlink = scrapy.Field()
    #更新日期
    in_time = scrapy.Field()