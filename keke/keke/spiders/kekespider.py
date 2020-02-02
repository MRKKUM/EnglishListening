# -*- coding: utf-8 -*-
import scrapy
from keke.items import KekeItem

class KekespiderSpider(scrapy.Spider):
    name = 'kekespider'
    allowed_domains = ['www.kekenet.com']
    start_urls = ['http://www.kekenet.com/Article/chuji/List_292.shtml']

    # 开始访问
    def start_request(self):
        yield scrapy.Request(self.start_urls, callback=self.parse,dont_filter=True)

    # 一级页面
    def parse(self, response):
        for msg in response.xpath('//ul[@id="menu-list"]/li'):
            inurl = msg.xpath('h2 / a[2]/@href').extract()
            yield scrapy.Request(inurl[0], callback=self.parse1)
        nowIndex = response.xpath('//div[@class="lastPage_left"]/div[@class="page th"]/b/text()').extract()
        print(nowIndex)
        next_page = 'http://www.kekenet.com/Article/chuji/List_{0}.shtml'.format(str(int(nowIndex[0])-2))
        print(next_page)
        if next_page:
            request_url = next_page
            print(request_url)
            yield scrapy.Request(request_url, callback=self.parse)

    # 二级访问
    def parse1(self,response):
        src = response.xpath('//div[@class="lastPage_left"]/div[3]/span/a/@href').extract()
        src = response.urljoin(src[0])
        print("二级界面"+src)
        yield scrapy.Request(src, callback=self.parse2)

    # 三级访问
    def parse2(self, response):
        item= KekeItem()
        item['file_name'] = response.xpath('//div[@class="lastPage_left"]/div[@class="list_box_2"]/ul[1]/table[1]/tr[1]/td[2]/a/text()').extract();
        item['src'] = response.xpath('//div[@class="lastPage_left"]/div[@class="list_box_2"]/ul[1]/table[1]/tr[4]/td[1]/a/@href').extract()
        yield item