# from PoeNinja.PoeNinja.dbConnector import DBConnector
import scrapy
from scrapy.crawler import CrawlerProcess
from items_cleaner import ItemCleaner
from scrapy.loader import ItemLoader

class GoodReadsSpider(scrapy.Spider):

    name = "goodreads"

    # requests
    def start_requests(self):
        url = "https://www.goodreads.com/quotes?page=1"
        yield scrapy.Request(url, callback=self.parse) # callback caches the response from each url
    
    # response
    def parse(self, response):
        for quote_selector in response.xpath("//div[@class='quote']"):
            loader = ItemLoader(item=ItemCleaner(), selector=quote_selector, response=response)
            loader.add_xpath("author", ".//div/div/span/text()")
            loader.add_xpath("quote_text", ".//div/div/text()")
            loader.add_xpath("tags", ".//div[@class='greyText smallText left']/a/text()")
            loader.add_xpath("likes", ".//div/div/div[@class='right']/a/text()")
            item = loader.load_item()
            item["likes"] = int(item["likes"].split()[0])


            # Store data in DB
            # db = DBConnector("mongodb://localhost:27017", "goodreads", "authorsQuotesTagsLikes")
            # collection = db.make_collection()
            # collection.insert_one(dict(item))

            yield item 

        # Scrape next page
        next_page = response.xpath("//a[@class='next_page']/@href").get()
        
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse) # callback caches the response from each url


process = CrawlerProcess()
process.crawl(GoodReadsSpider)
process.start()
