
CREATE_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS rates_usd
               (timestamp text, symbol text, price real)
"""

RETRIEVE_RATES_SQL = """
    SELECT m.symbol, min.price, max.price FROM
    (SELECT symbol, MIN(timestamp) as min_timestamp, MAX(timestamp) as max_timestamp FROM rates_usd) as m
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
