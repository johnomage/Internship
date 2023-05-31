import scrapy
from datetime import datetime as dt
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest
# from PoeNinja.db_connector import DBConnector
from pymongo import MongoClient


class PoeNinja(scrapy.Spider):
    name = "poe_ninja"

    def start_requests(self):
        url = "https://poe.ninja/challenge/currency/divine-orb"
        yield SplashRequest(url, callback=self.parse, endpoint="render.html", args={"wait": 0.5})

    def parse(self, response, **kwargs):
        for orb_selector in response.xpath(
                "//div[@style='display: grid; grid-gap: var(--s4); grid-template-columns: repeat(auto-fit, minmax(min(35ch, 100%), 1fr));']/div[1]"):
            data = {"transaction_type": orb_selector.xpath(".//h2/text()").get(),
                    "symbols": orb_selector.xpath(".//span[@data-variant='subdued']/text()").get(),
                    "symbol_values": orb_selector.xpath(".//div[@class='justify-center']/span/text()").get(),
                    "date": dt.today().strftime("%y-%m-%d"), "time": dt.today().strftime("%H:%M:%S")}

            db = MongoClient("mongodb://localhost:27017/") #("mongodb://localhost:27017/", "poe_ninja", "divine_orb")
            collection = db["POE_ninja1"]["DIvine_ORB"]
            collection.insert_one(data)


            yield data


# process = CrawlerProcess()
# process.crawl(PoeNinja)
# process.start()
