import time

import scrapy
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
import pandas as pd


class CoindeskScraper(scrapy.Spider):
    name = 'coindesk'

    def start_requests(self):
        url = 'https://www.coindesk.com/tag/bitcoin/572'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        items = []
        for selector in response.xpath('//*[@id="fusion-app"]/div[2]//main/div/div/div[2]'):
            item = {
                'heading': selector.xpath('.//h6/a[@target="_self"]/text()').get(),
                'subheading': selector.xpath('.//span[@class="content-text"]/text()').get(),
                'datetime': selector.xpath('.//div[@class="timing-data"]//text()').getall()[0:20:2]
            }

            items.append(item)
        df = pd.DataFrame(items)
        df.to_csv("coindesk.csv", index=False)
            # yield item
        time.sleep(.5)
        # next_page = response.xpath('//a[@aria-label="Next page"]/@href').get()
        # next_page = response.xpath("//a[contains(@rel,'next')]/@href").get()
        next_page = response.xpath("//a[contains(@rel,'prev')]/@href")

        if next_page:
            next_page_link = response.urljoin(next_page)
            print('\n----------------', next_page, '------------------------\n\n')
            yield scrapy.Request(url=next_page_link, callback=self.parse)



def run_spider():
    process = CrawlerProcess()
    process.crawl(CoindeskScraper)
    process.start()

if __name__ == '__main__':
    run_spider()

# headings = [heading.text for heading in driver.find_elements(By.XPATH, '//h6/a[@target="_self"]')]
# span_texts = [span.text for span in driver.find_elements(By.XPATH, '//span[@class="content-text"]')]
# datetimes = [datetime.text for datetime in driver.find_elements(By.XPATH,
#                                                                 '//div[@class="timing-data"]')]



