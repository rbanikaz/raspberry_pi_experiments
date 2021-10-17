import os
import sqlite3
import requests
import time
from datetime import datetime
from datetime import timedelta

from ticker_data import TickerData

class TickerDataLoader():

    def __init__(self):
        self.crypto_symbols = ["BTC", "ETH", "DOGE", "LINK", "ADA", "FIL", "SOL", "ICP"]

    def load_ticker_data(self):
        print("===========")
        print("Start Loading Ticker Data")
        con = sqlite3.connect("ticker.db")
        ticker_data = TickerData(con)
        ticker_data.create_table()

        crypto = self.get_crypto_exchange_rates() 
        current_time = datetime.utcnow()
        crypto_rates = []

        for symbol in crypto:
            c = (current_time.strftime("%Y-%m-%d %H:%M:%S"), symbol, crypto[symbol]["exch_rate"])
            crypto_rates.append(c)

        print("Inserting Rates: " + str(crypto_rates))
        ticker_data.insert_rates(crypto_rates)

        purge_time = (current_time - timedelta(hours=12)).strftime("%Y-%m-%d %H:%M:%S")
        print("Purging Rates before " + purge_time)
        ticker_data.purge_rates(purge_time)

        print("Done Loading Ticker Data")
        print("===========")
        con.close()

    def get_crypto_exchange_rates(self):
        key = os.environ.get("COINAPI_KEY")
        resp = requests.get("https://rest.coinapi.io/v1/exchangerate/USD?apikey=" + key)
        resp.raise_for_status()
        data = resp.json()

        result = {}

        for record in data["rates"]:
            symbol = record["asset_id_quote"]
            exch_rate = 1.0 / float(record["rate"])
            if symbol in self.crypto_symbols :
                result[symbol] = {
                    "exch_rate": exch_rate
                }

        return result


if __name__ == "__main__":
    ticker_data_loader = TickerDataLoader()
    while True:
        ticker_data_loader.load_ticker_data()
        time.sleep(900)

    