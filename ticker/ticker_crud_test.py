import sqlite3
from ticker import INSERT_RATES_SQL, RETRIEVE_RATES_SQL, CREATE_TABLE_SQL, PURGE_RATES_SQL
def test_crud():
    con = sqlite3.connect(":memory:")
    cur = con.cursor()

    cur.execute(CREATE_TABLE_SQL)

    fake_data = [
        ("2021-10-14 00:00:00", "BTC", 60000.0),
        ("2021-10-14 12:00:00", "BTC", 67000.0),
        ("2021-10-15 00:00:00", "BTC", 59000.0),
        ("2021-10-15 11:00:00", "BTC", 63000.0)
    ]

    cur.executemany(INSERT_RATES_SQL, fake_data)

    cur.execute(RETRIEVE_RATES_SQL, ["BTC"])
    print(cur.fetchall())

    cur.execute(PURGE_RATES_SQL, ["2021-10-15 00:00:00"])
    cur.execute(RETRIEVE_RATES_SQL, ["BTC"])
    print(cur.fetchall())
    con.commit()
    con.close()

if __name__ = "main":
    test_crud()