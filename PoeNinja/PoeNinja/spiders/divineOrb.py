import scrapy
from datetime import datetime as dt
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest



class PoeNinja(scrapy.Spider):
    name = "poe_ninja"

    def start_requests(self):
        url = "https://poe.ninja/challenge/currency/divine-orb"
        yield SplashRequest(url, callback=self.parse, endpoint="render.html", args={"wait": 3})

    # def parse(self, response, **kwargs):
    #     # for orb_selector in response.xpath("//div/div[2]/div[1]"):
    #     # for orb in response.css("div:nth-child(2) > div.layout-stack"):
    #         return {"transaction_type": response.css("div div h2::text").get(),
    #                "symbols": response.css("div div span span::text").get(),
    #                "symbol_values": response.css("div div span div span::text").get(),
    #                "date": dt.today().strftime("%y-%m-%d"), "time": dt.today().strftime("%H:%M:%S")}
    def parse(self, response):
        divcss = response.css("div:nth-child(2) > div.layout-stack").extract()
        divs = response.xpath('//div/div/h2/text()').extract()
        print("\n\nThese are the div tags:\n=======================",divcss)
        for div in divs:
            yield {
                'data': div.strip()
            }

        spans = response.xpath('//div/div/span/text()').extract()
        for span in spans:
            yield {
                'data': span.strip()
            }
# process = CrawlerProcess()
# process.crawl(PoeNinja)
# process.start()
