import yfinance as yf

msft = yf.Ticker("MSFT")
aapl = yf.Ticker("AAPL")

ticker = aapl

start = '2024-03-15'
end = '2024-03-16'
#
# start = "2000-01-01"
# end = "2024-02-19"
df = yf.download("AAPL", start, end)

# -- get historical market data
#hist = msft.history(period="max")
hist = msft.history(period="1mo")

# -- show pandas dataframe
print(df)
# print(hist)
# -- show csv
# print(hist.to_csv())