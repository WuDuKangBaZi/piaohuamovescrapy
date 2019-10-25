# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import mysql.connector
import json
logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename='new.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
class PiaohuaPipeline(object):
    def insert(self,value):
        conn = conn = mysql.connector.connect(user="", password="",
                                              host="", port="",
                                              database="", use_unicode=True)
        # 获取游标
        c = conn.cursor();
        # 插入数据
        c.execute(value)
        conn.commit()
        logging.info("Insert Sql:"+value)
        c.close()
        conn.close()
    def select(self,value):
        conn = conn = mysql.connector.connect(user="python", password="W225y924@",
                                              host="cdb-hbfecuhb.gz.tencentcdb.com", port="10089",
                                              database="piaohuamove", use_unicode=True)
        c=conn.cursor();
        c.execute(value)
        result = c.fetchall()
        return result[0]
    def process_item(self, item, spider):
        print("in pipelines")
        ll = []
        name = "".join(item['movename'])
        for link in item['movedownlink'] :
            ll.append(link.strip())
        strs = ','.join(str(x) for x in ll)
        in_time = "".join(item['in_time'])
        s_value = "select count(1) from movelist where in_date ='"+in_time+"' and movename = '" + name+"'"
        count = self.select(s_value)[0]
        if(count == 0):
            value = "insert into movelist(movename,downloadlink,in_date) values('"+name+"','"+strs+"','"+in_time+"')"
            self.insert(value)
        else:
            logging.warning("重复内容:",in_time,name)