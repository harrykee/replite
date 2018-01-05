# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanPipeline(object):
    def __init__(self):
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
                    """select * from dbook where title=%s and author=%s and press=%s and pretime=%s""",
                    (item['title'],
                    item['author'],
                    item['score'],
                    item['pretime']
                    ))
            repetition =self.cursor.fetchone()
            if repetition:
                pass
            else:
                self.cursor.execute( """insert into dbook(title,rate,author,score,press,pretime) values(%s,%s,%s,%s,%s,%s)""",
                        (item['title'],
                        item['rate'],
                        item['author'],
                        item['score'],
                        item['press'],
                        item['pretime'])
                        )
            self.connect.commit()

        except Exception as error:
            print(error)

        return item
