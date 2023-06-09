import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime as dt
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["poe_ninja"]
collection = db["divine_orb1"]

def scrape(url):
    # Create driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # run driver without launching Chrome browser.
    driver = webdriver.Chrome(options=options)

    # Get website
    url = "https://poe.ninja/challenge/currency/divine-orb"
    driver.get(url) # get response from url

    # Fetch the root elements
    elements = driver.find_elements(By.XPATH, "//section/div/div/div[2]/div[1]")

    divine_orb_data = {}

    for element in elements:
        html_content = element.get_attribute('outerHTML')
        soup = BeautifulSoup(html_content, 'lxml')

        # Print all drop down elements text
        # find transaction types: Buy and Sell
        print("Extracting transaction types...")
        transaction_types = [trx.text for trx in soup.select('div > div > h2')]
        sleep(.5)
        print("Done!")
        if len(transaction_types) == 0:
            print(
                '\033[91m' + f"Failed to cache transaction type. Trying again\n----------------------------------------------" + "\033[37m")
            scrape()  # Retry the loop if transaction_types is empty
        sleep(1.5)

        # find symbols: divine and chaos orbs
        print("Extracting symbols...")
        symbols = [s.text for s in soup.select("span span._text_91ms6_1")]
        sleep(.5)
        print("Done!")
        sleep(1.5)

        # find current symbol values
        print("Extracting symbol values...")
        symbol_values = [float(sm.text) for sm in soup.select("div span div span")]
        sleep(.5)

        print("Done!")
        sleep(1)

        print("Loading for pipeline..")

        divine_orb_data["transaction_types"] = transaction_types
        divine_orb_data["symbol"] = symbols
        divine_orb_data["symbol_values"] = symbol_values
        divine_orb_data["date"] = dt.now().strftime("%Y-%m-%d")
        divine_orb_data["time"] = dt.now().strftime("%H:%M:%S")
        sleep(1)
        break

        # Close driver
    driver.quit()
    return divine_orb_data

def cache(url):
    while True:
        data = scrape(url)
        if data["transaction_types"] is None:
            print("Retrying++++++++++++++++++++++++++")
            continue
        collection.insert_one(data)
        print("\033[32m" + f"{url} successfully scraped.\nData cached in database."
                           f" Collections: {collection.count_documents({})}" + "\033[37m")
        break

cache("https://poe.ninja/challenge/currency/divine-orb")
