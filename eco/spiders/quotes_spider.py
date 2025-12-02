from scrapy_redis.spiders import RedisSpider

from eco.items import EcoItem


class QuotesSpiderSpider(RedisSpider):
    name = "quotes_spider"
    redis_key = 'quotes_spider:start_urls'


    def parse(self, response):
        # 每条名言都在 <div class="quote">...</div>
        for quote in response.css('div.quote'):
            item = EcoItem()
            item['text'] = quote.css('span.text::text').get()
            item['author'] = quote.css('small.author::text').get()
            item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield item

        # 想翻页可继续，今天先只跑第一页
        # 下一页链接： <li class="next"><a href="/page/2/">Next</a></li>
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
