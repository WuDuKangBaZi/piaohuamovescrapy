# -*- coding: utf-8 -*-

import scrapy
import  requests
import logging

from bs4 import BeautifulSoup

from piaohua.items import  PiaohuaItem
from lxml import etree
import mysql.connector
# 获取各个分类的页面
urls = []
#获取页面的所有视频详细
# 这个方法 返回的 应该是 所有的详细页面 传入参数应该为 get_urllist() 这个方法里面的urls
#
logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename='new.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
def get_info_(url):
    html = requests.get(url,verify=False)
    etree_html = etree.HTML(html.text)
    items = etree_html.xpath('//div[@class="pic"]/a/@href')
    global urls
    for uls in items:
        logging.info("Movelink:=======>https://www.piaohua.com" + uls)
        urls.append("https://www.piaohua.com" + uls)
    new_links = etree_html.xpath('//li[@class="pages-next"]/a/@href')
    if new_links and len(new_links) > 0 :
        #链接list化
        new_link = new_links[0]
        print(new_link)
        tmp_url = url.split('/')
        tmp_url.pop()
        str = "/".join(tmp_url)
        new_links = str+"/"+new_link
        get_info_(new_links)

def get_urllist():
    uuss = []
   #获取每日推荐更新 以每天都要跑。。。
    res = requests.get("https://www.piaohua.com",timeout=6)
    res.raise_for_status()
    res.encoding=res.apparent_encoding
    soup = BeautifulSoup(res.text, 'html.parser')
    # 非法URL 1
    invalidLink1 = '#'
    # 非法URL 2
    invalidLink2 = 'javascript:void(0)'
    # 集合
    result = set()
    # 计数器
    mycount = 0
    # 查找文档中所有a标签
    for k in soup.find_all('a'):
        # print(k)
        # 查找href标签
        link = k.get('href')
        # 过滤没找到的
        if (link is not None):
            # 过滤非法链接
            if link == invalidLink1:
                pass
            elif link == invalidLink2:
                pass
            # elif link.find("javascript:") != -1:
            #     pass
            elif link.find("html") == -1:
                pass
            elif link.find("index.html") != -1:
                pass
            else:
                mycount = mycount + 1
                # print(mycount,link)
                logging.info("每日更新链接:"+link)
                result.add("https://www.piaohua.com" + link)
                uuss.append("https://www.piaohua.com" + link)



    #urls.append("https://www.piaohua.com")
    # print("All Page link:"+"".join(urls))
    return uuss

#主要被start_urls调用的
def get_urls():
    logger = logging.getLogger(__name__)
    uuss = get_urllist()
    for uus in uuss:
        logger.info(uus)
        get_info_(uus)
    return urls

class PiaohuamoveSpider(scrapy.Spider):
    logging.info("开始每日刷新")
    name = 'piaohuamove'
    allowed_domains = ['www.piaohua.com']
    start_urls = get_urllist()
    logging.info("Start:",start_urls)

    def parse(self, response):
        print("in Parse")
        item =PiaohuaItem()
        #print(response.xpath('//div[@class="m-text1"]').extract())
        for movelist in response.xpath('//div[@class="m-text1"]'):
            #名字
            item['movename'] = movelist.css('h1 *::text').extract()[0]
            #详细链接
            #item['movedownlink']  =  movelist.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[4]/a/text()').extract()
            movelink = movelist.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[4]/a/text()').extract()
            if(movelink == ""):
                movelink = movelist.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[3]/table[1]/tbody/tr/td/a').extract()
                if(movelink == ''):
                    movelink = movelist.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[3]/table[2]/tr/td/a').extract()
            item['movedownlink'] = movelink
            #更新链接
            item['in_time'] = movelist.xpath('/html/body/div[3]/div[2]/div/div[2]/div[2]/div[1]/span[2]').extract()[0].replace('发布时间：','').replace('<span>','').replace('</span>','')
           # item['in_time'] = in_time.
            logging.info(item)
            yield item





