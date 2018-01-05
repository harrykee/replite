import scrapy
import re
from bs4 import BeautifulSoup
from douban.items import DoubanItem

class DbSpider(scrapy.Spider):
    name ='douban'
    allowed_domains = ["douban.com"]
    start_urls =["https://www.douban.com/doulist/43430373"]
   
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
                score =book.select('.rating span')[2].text.lstrip('(').strip('人评价)')#使用beautifulsoup的strip去掉不需要的内容
                author =book.select('.abstract')[0].text
                title=title.replace(' ','').replace('\n','')
                author =author.replace('\n\r','').replace(' ','')
                aa=re.split('[\n]+',author)
                urlb =book.select('.title a')[0]['href']
                
                item['title'] = title
                item['rate'] = rate
                item['author'] = aa[1][3:] #去掉（作者：）三个字
                item['score'] =score
                item['press'] =aa[2][4:]
                item['pretime'] = aa[3][4:]
                #爬取书名链接的其他信息，使用parse_book函数实现，需要将item传过去
                yield scrapy.http.Request(urlb,callback=self.parse_book,meta=item)
            #获取下一页的链接
            nextPage = selector.xpath('//span[@class="next"]/link/@href').extract()
            if nextPage:  #判断是否为最后一条链接
                next =nextPage[0]
                #重复爬取链接中的图书信息
                yield scrapy.http.Request(next,callback=self.parse)

    #该函数用于爬取图书的详细信息，包括ISBN，价格，页数等，本例子中只爬取这三项
    def parse_book(self,response):
        item=response.meta #获取传过来的item
        #图书的价格等信息不在标签内，使用的获取信息方法
        ISBN=response.xpath(u'//span[.//text()[normalize-space(.)="ISBN:"]]/following::text()[1]').extract()[0]
        price=response.xpath(u'//span[.//text()[normalize-space(.)="定价:"]]/following::text()[1]').extract()[0]
        number=response.xpath(u'//span[.//text()[normalize-space(.)="页数:"]]/following::text()[1]').extract()[0]
        #去掉内容中带有的空格
        ISBN=ISBN.replace(' ','')
        price =price.replace(' ','')
        number = number.replace(' ','')
        item['ISBN']=ISBN
        item['price']=price
        item['number']=number
        yield item
