import config
import psycopg2
import psycopg2.extras
import yfinance as yf
from datetime import datetime, timedelta
#
# -- This script inserts in the DB table sharedata the shares prices (daily)
# -- It should be scheduled every market day
#
connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

with connection.cursor() as c:
    c.execute('SELECT MAX(t."idtickISINShare"),t."TICKER",MAX(s."date") FROM ptf.tickerisinshare t\
	           LEFT JOIN ptf.sharedata s ON t."idtickISINShare" = s."idtickISINShare" GROUP BY t."TICKER"')
    data = c.fetchall()
    c.close()

for row in data:
    idtickISINShare = row[0]
    ticker = row[1]
    last_upd_dt = row[2]
    if last_upd_dt is None: continue
    start_dt = last_upd_dt + timedelta(days=1)
    end_dt = datetime.now()
    # print("start_dt = ")
    # print(start_dt)
    # print("end_dt = ")
    # print(end_dt)
    df = yf.download(ticker, start_dt, end_dt, interval="1d")
    df = df.reset_index()
    # print(type(df))
    # print(df.iloc[0,0])
    # print(df.iloc[0, 1])
    # print(df.iloc[0, 2])
    # print(df.iloc[0, 3])
    # print(df.iloc[0, 4])
    # print(df.iloc[0, 5])
    # print(df.iloc[0, 6])
    print("df = ")
    print(df)
    #
    dt = df.iloc[0,0]
    print(type(dt))
    open = df.iloc[0,1]
    print(type(open))
    high = df.iloc[0,2]
    low = df.iloc[0,3]
    close = df.iloc[0,4]
    adj_close = df.iloc[0,5]
    volume = df.iloc[0,6]
    volume = int(volume)
    print(type(volume))
    with connection.cursor() as c:
        c.execute("""
            INSERT INTO ptf.sharedata ("idtickISINShare", "date", "open", "high", "low", "close", "adj_close", "volume", "ticker")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (idtickISINShare, df.iloc[0,0], df.iloc[0,1], df.iloc[0,2], df.iloc[0,3], df.iloc[0,4], df.iloc[0,5], volume, ticker))

connection.commit()