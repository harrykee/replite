# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#将抓取到的数据存到数据库当中

class DoubanPipeline(object):
    def __init__(self):
        #连接数据库
        self.connect = pymysql.connect(
                host='localhost',
                db ='douban',
                user = 'root',
                password = 'root',
                port = 3306,
                charset ='utf8',
                use_unicode = True)
        self.cursor = self.connect.cursor();

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                    """select * from dbook where ISBN=%s""",item['ISBN'])
            repetition =self.cursor.fetchone()
            if repetition:
                pass
            else:
                #插入数据库相应的数据
                self.cursor.execute( """insert into dbook(ISBN,title,rate,author,score,press,pretime,price,number) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (item['ISBN'],
                        item['title'],
                        item['rate'],
                        item['author'],
                        item['score'],
                        item['press'],
                        item['pretime'],
                        item['price'],
                        item['number'])
                        )
            self.connect.commit()

        except Exception as error:
            print(error)

        return item
