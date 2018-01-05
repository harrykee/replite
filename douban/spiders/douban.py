import scrapy
import re
from bs4 import BeautifulSoup
from douban.items import DoubanItem

class DbSpider(scrapy.Spider):
    name ='douban'
    start_urls =["https://www.douban.com/doulist/43430373"]
    URL = "https://www.douban.com/doulist/43430373/?start=25&sort=seq&sub_type="

    def parse(self,response):
        item = DoubanItem()
        response.encding='utf-8'
        soup = BeautifulSoup(response.text,'html.parser')
        books= soup.select('.doulist-item')
        selector = scrapy.Selector(response)
        for book in books:
            if len(book.select('.title a'))>0:
                title =book.select('.title a')[0].text
                rate =book.select('.rating span')[1].text
                score =book.select('.rating span')[2].text.lstrip('(').strip('人评价)')
                author =book.select('.abstract')[0].text
                title=title.replace(' ','').replace('\n','')
                author =author.replace('\n\r','').replace(' ','')
                aa=re.split('[\n]+',author)
                urlb =book.select('.title a')[0]['href']
                
                item['title'] = title
                item['rate'] = rate
                item['author'] = aa[1][3:]
                item['score'] =score
                item['press'] =aa[2][4:]
                item['pretime'] = aa[3][4:]
                yield scrapy.http.Request(urlb,callback=self.parse_book,meta=item)
            nextPage = selector.xpath('//span[@class="next"]/link/@href').extract()
            if nextPage:
                next =nextPage[0]
                print(next)
                yield scrapy.http.Request(next,callback=self.parse)

    def parse_book(self,response):
        item=response.meta
        ISBN=response.xpath(u'//span[.//text()[normalize-space(.)="ISBN:"]]/following::text()[1]').extract()[0]
        price=response.xpath(u'//span[.//text()[normalize-space(.)="定价:"]]/following::text()[1]').extract()[0]
        number=response.xpath(u'//span[.//text()[normalize-space(.)="页数:"]]/following::text()[1]').extract()[0]
        ISBN=ISBN.replace(' ','')
        price =price.replace(' ','')
        number = number.replace(' ','')
        item['ISBN']=ISBN
        item['prise']=price
        item['number']=number
        yield item
        # print(ISBN)
        # print(price)
        # print(number)
