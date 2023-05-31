"""
## Scrpaing Divine Orb Price in Chaos Orbs (Buy and Sell) from Poe Ninja

**Steps**
1. Import necessary packages
2. Set up the web driver, and soup(parsed with lxml)
3. Extract the transaction types
4. Get symbols for each transaction
5. Get the values of each symbol
6. Make a dictionary of transactions type, symbols and their corresponding values
7. Cache in a DB
"""


# Import necessary packages
import pymongo
from bs4 import BeautifulSoup
from datetime import datetime
import time
from selenium import webdriver
from db_connector import DBConnector


class Scraper:
    def __init__(self, divine_url):
        self.divine_url = divine_url

    # Set up the web driver, and soup(parsed with lxml)
    def setup_driver_soup(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless") # do not launch browser
        driver = webdriver.Chrome(options=options)
        driver.get(self.divine_url)
        soup = BeautifulSoup(driver.page_source, "lxml")
        driver.quit()  # Close browser session after parsing.
        return soup

    # find all "div" tags (with "layou-stack" as class attribute) in the "main" tag
    def get_div_tag(self):
        main = self.setup_driver_soup().find_all("main")
        return [d.find("div", class_="layout-stack") for d in main]

    # Extract the transaction types ----- Buy and Sell
    def get_transaction_types(self):
        time.sleep(1.5)
        print("\nSearching div for transaction types...")
        transactions = []
        for h in self.get_div_tag():
            if h is None:
                print('\033[91m' + "None found in 'get_transaction_types' method..." + '\033[37m')
                break
            else:
                trx = h.find_all("h2")
                for buy_sell in trx:
                    transactions.append(buy_sell.text)
            print("Done!\n-------")
        return transactions

    # Get symbols for each transaction
    def get_symbols(self):
        time.sleep(1.5)
        print("\nSearching div for symbols...")
        symbols = []
        for s in self.get_div_tag():
            if s is None:
                print('\033[91m' + "None found in 'get_symbols' method..." + '\033[37m')
                break
            else:
                span = s.find_all("span", {"data-variant": "subdued"})
                for symbol in span:
                    symbols.append(symbol.text)
            print("Done!\n-------")
        return symbols

    # Get the values of each symbol
    def get_symbol_values(self):
        time.sleep(1.5)
        print("\nSearching div for symbols values...")
        values = []
        for d in self.get_div_tag():
            if d is None:
                print('\033[91m' + "None found in 'get_symbol_values' method..." + '\033[37m')
                break
            else:
                inner_div = d.find_all("div", class_="justify-center")
                for id in inner_div:
                    values.append(id.text)
                print("Done!\n-------")
        return values

    # date and time for current rates
    def get_timestamp(self):
        return datetime.today().strftime("%Y-%m-%d %H:%M:%S").split()

    # Make a dictionary of transactions type, symbols and their corresponding values
    def to_dict(self):
        transaction_types = self.get_transaction_types()
        symbols = self.get_symbols()
        symbol_values = self.get_symbol_values()
        price_dict = {}

        if (len(transaction_types) >= 2 and len(symbols) >= 4 and len(symbol_values) >= 4):
            price_dict[transaction_types[0]] = {
                symbols[0]: float(symbol_values[0]),
                symbols[1]: float(symbol_values[1]),
            }

            price_dict[transaction_types[1]] = {
                symbols[2]: float(symbol_values[2]),
                symbols[3]: float(symbol_values[3]),
            }

            price_dict["date"] = self.get_timestamp()[0]
            price_dict["time"] = self.get_timestamp()[1]
        return price_dict

    # Cache in a DB
    def save_to_db(self, price_dict_):
        client = DBConnector("mongodb://localhost:27017/", "poe_ninja", "divine_orb")
        collection = client.connect_to_db()
        print("Caching data to database...")
        collection.insert_one(price_dict_)
        print("Total documents: ", collection.count_documents({}))
        return collection


divine_url = "https://poe.ninja/challenge/currency/divine-orb"
scraper = Scraper(divine_url)


# retries if None is returned in any of the methods
attempt = 0
while attempt < 3:
    price_dict = scraper.to_dict()
    if price_dict:
        scraper.save_to_db(price_dict)
        now = datetime.now().strftime("%H:%M:%S")
        time.sleep(1)
        print(
            "\033[32m" + f"{divine_url} successfully scraped.\nData stored in database time: {now}" + "\033[37m")  # print in green reset to white.
        break
    else:
        print('\033[91m' + f"Failed to cache data: 'scraper.to_dict()' returned an empty dictionary. Attempt {attempt+1}\
              \n----------------------------------------------" + "\033[37m")  # print in red and reset to white
        attempt += 1
        time.sleep(1)
