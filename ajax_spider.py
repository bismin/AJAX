# -*- coding: utf-8 -*-
import scrapy
from ..items import WordpressItem
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
import json
class AjaxSpiderSpider(scrapy.Spider):
    name = 'ajax_spider'
    start_urls=["https://pythonhelp.wordpress.com/"]
    flag=1
    page=1
    def parse(self, response):
    	if self.flag:
    		sel= Selector(text=response.body)

    		self.flag=0
    	else:
    		data=json.loads(response.body)
    		b=data.get('html','')
    		if b:
    			sel=Selector(text=b)
    		else :
    			sel=''
    	if sel:
    		jobs=sel.xpath('//h1[@class="entry-title"]')
    		item=WordpressItem()
    		for job in jobs:
    			post=job.xpath('a/text()').extract_first('')
    			item['post']=post
    			yield item
    			self.page=self.page+1
    			yield FormRequest("https://pythonhelp.wordpress.com/?infinity=scrolling",formdata={'action':'infinite_scroll','page':str(self.page),'currentday':'18.09.16','order':'DESC','last_post_date':'2016-09-18 09:11:24',},callback=self.parse)