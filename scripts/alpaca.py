import config
import alpaca_trade_api as tradeapi
import psycopg2
import psycopg2.extras
import json

#
# This script downloads a list of assets (us_equity) from using Alpaca API
#

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

api = tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.API_URL)

# obtain account information
account = api.get_account()
# print("account = ")
# print(account)

assets = api.list_assets()

i = 0
for asset in assets:
    #print(type(asset))
    print(asset)
    asset_class = getattr(asset, 'class')
    print(asset_class)
    i += 1
    if i  == 3:
        break

# for asset in assets:
#     asset_class = getattr(asset, 'class')
#     print(f"Inserting stock {asset.name} {asset.symbol} {asset_class}")
#     cursor.execute("""
#         INSERT INTO ptf.stock (name, symbol, exchange, is_etf, status, class)
#         VALUES (%s, %s, %s, false, %s, %s)
#     """, (asset.name, asset.symbol, asset.exchange, asset.status, asset_class))
#
# connection.commit()