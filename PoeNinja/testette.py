import scrapy
from scrapy.crawler import CrawlerProcess
import db_connector


text_list = []


class GoodReadsSpider(scrapy.Spider):
    name = "goodreads"

    # requests
    def start_requests(self):
        url = "https://developer.edamam.com/edamam-docs-nutrition-api#/" # "https://poe.ninja/challenge/currency/divine-orb"

        # traverse the urls
        yield scrapy.Request(url=url, callback=self.parse)  # callback caches the response from each url

    # response
    def parse(self, response):
        for text in response.selector.xpath("//td/span[@class='caps']"):
            extracted_text = text.xpath(".//text()").get()
            text_list.append(extracted_text)
            yield extracted_text


process = CrawlerProcess()
process.crawl(GoodReadsSpider)
process.start()

print("\n\n=============================================================\n")
print(text_list)
print("\n")