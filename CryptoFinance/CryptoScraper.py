from datetime import datetime as dt
from time import sleep
import pandas as pd
import yfinance as yf
from pymongo.errors import DuplicateKeyError

from CrytoDatabaseConnector import DBConnector

base_currency = "GBP"
db_connector = DBConnector("mongodb://localhost:27017", "CryptoCache")


class Scraper:
    """
        Class for scraping data for a specific crypto symbol from a Yahoo Finance.

        Args:
            symbol (str): The symbol or ticker of the crypto asset to scrape data for.
            period (str, optional): The time period to scrape data for. Defaults to "1m".
            interval (str, optional): The interval at which to scrape data. Defaults to "1h".

        Attributes:
            symbol (str): The symbol of the financial asset.
            quote (str): The quote string for the symbol and base currency.
            period (str): The time period for scraping data.
            interval (str): The interval for scraping data.
            collection (pymongo.collection.Collection): The MongoDB collection for caching the scraped data.

        """
    def __init__(self, symbol, period: str = "1m", interval: str = "1h") -> None:
        self.symbol = symbol
        self.quote = "-".join([symbol, base_currency])
        self.period = period
        self.interval = interval
        self.collection = db_connector.create_collection(self.symbol)

    def cache_currency(self):
        """
          Cache the currency data by scraping it from a financial data source and storing it in the MongoDB collection.

          Returns:
              None
        """
        symbol_history = yf.Ticker(self.quote).history(period=self.period, interval=self.interval)

        try:
            # Iterate over the rows and insert documents into the collection
            for index, row in symbol_history.iterrows():
                document = row.to_dict()
                document["_id"] = str(index)
                self.collection.insert_one(document)

            print(f"{self.collection.count_documents({})} documents cached in {self.symbol} cache ")

        except DuplicateKeyError:
            print(f"Duplicate documents found in {self.symbol} cache. Resetting collection...")
            sleep(.5)
            self.__reset_collection()

        # Remove duplicates for the currency cache

    def __reset_collection(self, show_duplicates=False):
        sleep(.5)
        self.collection.delete_many({})
        print("Caching new documents...")
        self.cache_currency()


class CacheExplorer:
    """
       Class for exploring cached currency data from a MongoDB collection.

       Args:
           currency (str): The currency symbol or identifier to explore.
           period (str): The time period of the cached currency data.

       Attributes:
           currency (str): The currency symbol or identifier.
           period (str): The time period of the cached currency data.
           collection (pymongo.collection.Collection): The MongoDB collection containing the cached currency data.

       """

    def __init__(self, currency: str, period: str):
        self.currency = currency
        self.period = period
        __scraper = Scraper(self.currency, self.period)
        self.collection = __scraper.collection

    # noinspection PyMethodMayBeStatic
    def get_currency_history(self):
        return pd.DataFrame(self.collection.find({}))
