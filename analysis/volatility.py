from __future__ import print_function, division
# from yahoo_finance import Share
# from yahoo_finance import Currency
from poloniex import Poloniex
import datetime
import time
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

"""
Find the monthly volatilities for a variety of currencies and assets.

Securities:
btc, eth, the 10th largest alt coin,
the 100th largest alt coin,
usd, yuan, a small country currency, goog,
the 1000th largest stock, and a penny stock.

Use at least 250 data points (a year of trading days).
"""

end = datetime.datetime.now()
start = datetime.datetime(2016, 7, 16)

end_time = time.mktime(end.timetuple())
start_time = time.mktime(start.timetuple())


def get_crypto_data(ticker=''):
    return polo.returnChartData(ticker,
                                period=86400,
                                start=start_time,
                                end=end_time)

tickers = [
        'USDT_BTC',
        'BTC_DASH',
        'BTC_ETH',
       #'BTC_ETC',
        'BTC_LTC',
        'BTC_STR',
        'BTC_XEM',
        'BTC_XMR',
        'BTC_XRP']
# Crypto Currencies
polo = Poloniex(timeout=10)
hist = {}
for ticker in tickers:
    hist[ticker] = get_crypto_data(ticker)
    hist[ticker] = np.array([day['weightedAverage'] for day in hist[ticker]])
    print(ticker + " size: " + str(hist[ticker].shape))
    # print(hist[ticker])

# TODO: Add currency
# Currencies
# usd = Currency('EURUSD')
# yuan = Currency('USDCNY')
# usdpln = Currency('USDPLN')       # small country currency

# Stocks
# goog = Share('GOOG')
# ebio = Share('EBIO')              # penny stock
# xbxs = Share('XBKS')              # 1000th largest stock

# Historical data for stocks and currenciess
# goog_historic = goog.get_historical(str(start.date()), str(end.date()))
# ebio_historic = ebio.get_historical(str(start.date()), str(end.date()))
# xbxs_historic = xbxs.get_historical(str(start.date()), str(end.date()))

# usd.get_historical(str(start.date()), str(end.date()))
# yuan.get_historical(str(start.date()), str(end.date()))
# usdpln.get_historical(str(start.date()), str(end.date()))

# print(btc)
dates = pd.date_range(start=start, end=end)
ticks = np.transpose(np.vstack([hist[ticker] for ticker in tickers]))
df = pd.DataFrame(ticks, index=dates, columns=tickers)
df.to_csv(path_or_buf='/tmp/random_df.csv')

# for day in hist['USDT_BTC']:
#     print(str(day['date']) + " " + str(day['weightedAverage']))

