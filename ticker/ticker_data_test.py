from os import times
import sqlite3
from ticker_data import TickerData

def test_crud():
    con = sqlite3.connect(":memory:")

    ticker_data = TickerData(con)
    ticker_data.create_table()

    fake_data = [
        ("2021-10-14 00:00:00", "BTC", 60000.0),
        ("2021-10-14 12:00:00", "BTC", 67000.0),
        ("2021-10-15 00:00:00", "BTC", 59000.0),
        ("2021-10-15 11:00:00", "BTC", 63000.0)
    ]

    ticker_data.insert_rates(fake_data)
    rates = ticker_data.retrieve_rates("BTC")
    print(rates)
    assert rates == {"symbol": 'BTC', "open_price": 60000.0, "close_price": 63000.0}
    
    ticker_data.purge_rates("2021-10-15 00:00:00")

    rates = ticker_data.retrieve_rates("BTC")
    print(rates)
    assert rates == {"symbol": 'BTC', "open_price": 59000.0, "close_price": 63000.0}

    con.close()

if __name__ == "__main__":
    test_crud()