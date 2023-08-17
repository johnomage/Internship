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
# import tensorflow as tf
# from tensorflow import keras
# from keras import layers, Sequential
# from keras.layers import Dense, LSTM, MultiHeadAttention, Dropout, LeakyReLU
# from keras.callbacks import EarlyStopping
# from keras.activations import relu,sigmoid, leaky_relu
# from keras.callbacks import EarlyStopping
#
# model = Sequential()
# from sklearn.metrics import mean_absolute_error
# from keras.losses import MeanSquaredError
# from keras.metrics import MeanAbsoluteError
# from keras.optimizers.legacy import adam
#
# early_stopping = EarlyStopping(monitor='val_loss', patience=3, mode='min')
#
#
# model.fit_generator()
# import warnings
# warnings.si
# from keras.preprocessing.sequence import TimeseriesGenerator
#
# # TimeseriesGenerator(data, target, length, batch_size)
# import numpy as np
#
# check = pd.DataFrame(np.random.randint(10, 100, (10, 3)), columns=['a', 'b', 'c'])
#
# model = Sequential()
#
# model.add(LSTM(units=128, input_shape=(23,3), activation=relu))
# model.add(LeakyReLU(alpha=0.3))
# model.add(Dropout(rate=0.2))



