import scrapy


class EcnomicNewsSpider(scrapy.Spider):
    name = "ecnomic_news"

    def start_requests(self):
        urls = [
            "https://www.thepaper.cn/channel_25951",
        ]
        custom_settings = {
            'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.css('.news_tu a::attr(href)').getall()
        urls = []
        for link in links:
            url = "https://www.thepaper.cn/" + link
            urls.append(url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        yield {
            'news_title': response.css('.news_title::text').get(),
            'news_source': response.css('.news_about p::text')[0].get(),
            'news_time': response.css('.news_about p::text')[1].get().strip(),
            'news_txt': ''.join(response.css('.news_txt::text').getall())
        }

class LifeNewsSpider(scrapy.Spider):
    name = "life_news"

    def start_requests(self):
        urls = [
            "https://www.thepaper.cn/channel_25953",
        ]
        custom_settings = {
            'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.css('.news_tu a::attr(href)').getall()
        urls = []
        for link in links:
            url = "https://www.thepaper.cn/" + link
            urls.append(url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        yield {
            'news_title': response.css('.news_title::text').get(),
            'news_source': response.css('.news_about p::text')[0].get(),
            'news_time': response.css('.news_about p::text')[1].get().strip(),
            'news_txt': ''.join(response.css('.news_txt::text').getall())
        }

class CurrentNewsSpider(scrapy.Spider):
    name = "current_news"

    def start_requests(self):
        urls = [
            "https://www.thepaper.cn/channel_25953",
        ]
        custom_settings = {
            'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.css('.news_tu a::attr(href)').getall()
        urls = []
        for link in links:
            url = "https://www.thepaper.cn/" + link
            urls.append(url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        yield {
            'news_title': response.css('.news_title::text').get(),
            'news_source': response.css('.news_about p::text')[0].get(),
            'news_time': response.css('.news_about p::text')[1].get().strip(),
            'news_txt': ''.join(response.css('.news_txt::text').getall())
        }


'''load_chosen.jsp?nodeids=25949&topCids=3385400,3388…3388463,3368844,&pageidx=5&lastTime=1556751771400
load_index.jsp?nodeids=25462,25488,25489,25490,254…,3574240,3569707&pageidx=3&lastTime=1559272759008
'''

class NewsSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        urls = []
        for i in range(1,25):
            urls.append("https://www.thepaper.cn/load_chosen.jsp?nodeids=25949&topCids=3668169,3668…3668577,3664549,&pageidx=" + str(i) +"&lastTime=1560384505411")
        custom_settings = {
            'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.css('.news_tu a::attr(href)').getall()
        urls = []
        for link in links:
            url = "https://www.thepaper.cn/" + link
            urls.append(url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        yield {
            'news_title': response.css('.news_title::text').get(),
            'news_source': response.css('.news_about p::text')[0].get(),
            'news_time': response.css('.news_about p::text')[1].get().strip(),
            'news_txt': ''.join(response.css('.news_txt::text').getall())
        }