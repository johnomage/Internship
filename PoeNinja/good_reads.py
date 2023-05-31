import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

class GoodReadsSpider(scrapy.Spider):

    name = "goodreads"
    df = pd.DataFrame()

    # requests
    def start_requests(self):
        url = "https://www.goodreads.com/quotes?page=1"
        yield scrapy.Request(url, callback=self.parse) # callback caches the response from each url
    
    # response
    def parse(self, response):
        for texts in response.xpath("//div[@class='quote']"):
            data = {
                "quote_text": texts.xpath(".//div/div/text()").get().strip().replace("”", "").replace("“", ""),
                "author": texts.xpath(".//div/div/span/text()").get().strip(),
                "tags": texts.xpath(".//div/div/div/a/text()").getall()[:-1], # excluding "likes"
                "likes": texts.xpath(".//div/div/div[@class='right']/a/text()").get().strip().replace("”", "").replace("“", "")             
            }

            self.df = self.df.append(data, ignore_index=True)
            yield data

        # Scrape next page
        next_page = response.xpath("//a[@class='next_page']/@href").get()
        
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse) # callback caches the response from each url
        
    
    def to_dataframe(self, response):
        return pd.DataFrame(list(self.parse(response)))

    

process = CrawlerProcess({"FEED_URI": "file:///data/goodreads.csv"})
process.crawl(GoodReadsSpider)
process.start()


# goodreads = GoodReadsSpider()
# print(goodreads.df)
