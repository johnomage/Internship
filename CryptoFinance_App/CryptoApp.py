"""
This program requires that MongoDB Compass or Client is installed on local machine.
"""

from CryptoFinance.CryptoScraper import Scraper, CacheExplorer

# data manipulator
# import numpy as np
import pandas as pd



currencies = ["XRP", "ETH", "TRX", "USDT", "BTC", "BNB"]

# currency = input("Enter currency: ").upper()

period = input("Enter period (e.g. max, 2d, 1mo, 3mo, 10y): ")


def scrape_currency():
    for currency in currencies:
        stored_data = Scraper(currency, period)
        stored_data.cache_currency()


def retrieve_data():
    while True:
        currency = input("Enter currency: ").upper()
        if currency not in currencies:
            print(f"Please enter any currency in {currencies}")
        else:
            break
    cache_explorer = CacheExplorer(currency=currency, period="now")
    return cache_explorer.get_currency_history()


scrape_currency()

data = retrieve_data()
# data.set_index("_id", inplace=True)
data.index = pd.to_datetime(data.index)
print(data)
