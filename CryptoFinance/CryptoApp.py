from CryptoScraper import Scraper, CacheExplorer


symbols = ["XRP", "ETH", "TRX", "USDT", "BTC", "LTC"]
def scrape_currency():

    currency = input("Enter currency: ").upper()
    if currency not in symbols:
        print(f"Please enter any currency in {symbols}")
        scrape_currency()
    period = input("Enter period (e.g. max, 2d, 1mo, 3mo, 10y): ")

    stored_data = Scraper(currency, period)
    stored_data.cache_currency()

    def retrieve_data():
        cache_explorer = CacheExplorer(currency=currency, period="now")
        crypto_data = cache_explorer.get_currency_history()
        print(crypto_data)

    response = input("\nView cached currency (y/n): ").upper()
    if response == "Y":
        retrieve_data()
    else:
        exit(0)


scrape_currency()
