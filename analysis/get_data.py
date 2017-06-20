from __future__ import print_function, division
# from yahoo_finance import Share
# from yahoo_finance import Currency
from poloniex import Poloniex
from datetime import datetime, timedelta
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

end = datetime.now()
start = datetime(2016, 8, 19)

end_time = time.mktime(end.timetuple())
start_time = time.mktime(start.timetuple())


def get_crypto_data(ticker=''):
    return polo.returnChartData(ticker,
                                period=86400,
                                start=start_time,
                                end=end_time)


tickers = [
    'BTC_AMP',
    'BTC_ARDR',
    'BTC_BCN',
    'BTC_BCY',
    'BTC_BELA',
    'BTC_BLK',
    'BTC_BTCD',
    'BTC_BTM',
    'BTC_BTS',
    'BTC_BURST',
    'BTC_CLAM',
    'BTC_DASH',
    'BTC_DCR',
    'BTC_DGB',
    'BTC_DOGE',
    'BTC_EMC2',
    'BTC_ETC',
    'BTC_ETH',
    'BTC_EXP',
    'BTC_FCT',
    'BTC_FLDC',
    'BTC_FLO',
    'BTC_GAME',
    'BTC_GNO',
    'BTC_GNT',
    'BTC_GRC',
    'BTC_HUC',
    'BTC_LBC',
    'BTC_LSK',
    'BTC_LTC',
    'BTC_MAID',
    'BTC_NAUT',
    'BTC_NAV',
    'BTC_NEOS',
    'BTC_NMC',
    'BTC_NOTE',
    'BTC_NXC',
    'BTC_NXT',
    'BTC_OMNI',
    'BTC_PASC',
    'BTC_PINK',
    'BTC_POT',
    'BTC_PPC',
    'BTC_RADS',
    'BTC_REP',
    'BTC_RIC',
    'BTC_SBD',
    'BTC_SC',
    'BTC_SJCX',
    'BTC_STEEM',
    'BTC_STR',
    'BTC_STRAT',
    'BTC_SYS',
    'BTC_VIA',
    'BTC_VRC',
    'BTC_VTC',
    'BTC_XBC',
    'BTC_XCP',
    'BTC_XEM',
    'BTC_XMR',
    'BTC_XPM',
    'BTC_XRP',
    'BTC_XVC',
    'BTC_ZEC']
# Crypto Currencies
polo = Poloniex(timeout=10)
hist = {}
hist_date = {}
days_passed = int((end - start).days) + 1
for ticker in tickers:
    print('processing ticker: ' + ticker)
    hist[ticker] = get_crypto_data(ticker)
    hist_date[ticker] = np.array([day['date'] for day in hist[ticker]])
    print('days_passed:' + str(days_passed))
    print('len(hist_date[ticker]):' + str(len(hist_date[ticker])))
    fill = np.full((days_passed-len(hist_date[ticker]), 1), np.inf)
    hist[ticker] = np.append(fill, np.array([day['weightedAverage'] for day in hist[ticker]]))
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

# print(btc)

dates = pd.date_range(start=start, end=end)
print('size_of_dates:' + str(dates.shape))
ticks = np.transpose(np.vstack([hist[ticker] for ticker in tickers]))
df = pd.DataFrame(ticks, index=dates, columns=tickers)
df.to_csv(path_or_buf='/tmp/random_df.csv')

# for day in hist['USDT_BTC']:
#     print(str(day['date']) + " " + str(day['weightedAverage']))

