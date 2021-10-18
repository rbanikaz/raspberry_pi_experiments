
class TickerData():
    connection = None

    def __init__(self, connection):
        self.connection = connection

    def create_table(self):
        cur = self.connection.cursor()
        cur.execute(CREATE_TABLE_SQL)
        self.connection.commit()


    def retrieve_rates(self, symbol):
        cur = self.connection.cursor()
        cur.execute(RETRIEVE_RATES_SQL, [symbol])
        result = cur.fetchone()
        return {
            "symbol": result[0],
            "open_price": result[1],
            "close_price": result[2]
        }


    def insert_rates(self, data):
        cur = self.connection.cursor()
        cur.executemany(INSERT_RATES_SQL, data)
        self.connection.commit()


    def purge_rates(self, date):
        cur = self.connection.cursor()
        cur.execute(PURGE_RATES_SQL, [date])
        self.connection.commit()




CREATE_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS rates_usd
               (timestamp text, symbol text, price real)
"""

RETRIEVE_RATES_SQL = """
    SELECT m.symbol, min.price, max.price FROM
    (SELECT symbol, MIN(timestamp) as min_timestamp, MAX(timestamp) as max_timestamp FROM rates_usd group by 1) as m
    JOIN rates_usd min ON min.symbol = m.symbol AND min.timestamp = m.min_timestamp
    JOIN rates_usd max ON max.symbol = m.symbol AND max.timestamp = m.max_timestamp
    WHERE m.symbol = ?
"""

INSERT_RATES_SQL = """
    INSERT INTO rates_usd VALUES (?, ?, ?)
"""

PURGE_RATES_SQL = """
    DELETE FROM rates_usd WHERE timestamp < ?
"""
