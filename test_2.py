from __future__ import print_function, division
from poloniex import Poloniex

polo = Poloniex()
import numpy as np
import cvxopt as opt
from cvxopt import blas, solvers
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt

# print(polo.returnTicker())

tickers = ["BTC_XVC",
           "BTC_PINK",
           "BTC_SYS",
           "BTC_EMC2",
           "BTC_RADS",
           "BTC_SC",
           "BTC_MAID",
           "BTC_GNT",
           "BTC_BCN",
           "BTC_REP",
           "BTC_BCY",
           "BTC_GNO",
           # "XMR_NXT",
           "USDT_ZEC",
           "BTC_FCT",
           "USDT_ETH",
           "USDT_BTC",
           "BTC_LBC",
           "BTC_DCR",
           "USDT_ETC",
           "BTC_AMP",
           "BTC_XPM",
           "BTC_NXT",
           "BTC_VTC",
           "ETH_STEEM",
           "XMR_BLK",
           "BTC_PASC",
           "XMR_ZEC",
           "BTC_GRC",
           "BTC_NXC",
           "BTC_BTCD",
           "BTC_LTC",
           "BTC_DASH",
           "BTC_NAUT",
           "ETH_ZEC",
           "BTC_ZEC",
           "BTC_BURST",
           "BTC_BELA",
           "BTC_STEEM",
           "BTC_ETC",
           "BTC_ETH",
           "BTC_HUC",
           "BTC_STRAT",
           "BTC_LSK",
           "BTC_EXP",
           "BTC_CLAM",
           "ETH_REP",
           "XMR_DASH",
           "USDT_DASH",
           "BTC_BLK",
           "BTC_XRP",
           "USDT_NXT",
           "BTC_NEOS",
           "BTC_BTS",
           "BTC_DOGE",
           "ETH_GNT",
           "BTC_SBD",
           "ETH_GNO",
           "BTC_XCP",
           "USDT_LTC",
           "BTC_BTM",
           "USDT_XMR",
           "ETH_LSK",
           "BTC_OMNI",
           "BTC_NAV",
           "BTC_FLDC",
           "BTC_XBC",
           "BTC_DGB",
           "BTC_NOTE",
           "XMR_BTCD",
           "BTC_VRC",
           "BTC_RIC",
           "XMR_MAID",
           "BTC_STR",
           "BTC_POT",
           "BTC_XMR",
           "BTC_SJCX",
           "BTC_VIA",
           "BTC_XEM",
           "BTC_NMC",
           "ETH_ETC",
           "XMR_LTC",
           "BTC_ARDR",
           "BTC_FLO",
           # "USDT_XRP",
           "BTC_GAME",
           "BTC_PPC",
           "XMR_BCN",
           "USDT_STR"
           ]


def unix_to_date(unix_timestamp):
    return datetime.datetime.fromtimestamp(
        int(unix_timestamp)
    ).strftime('%Y-%m-%d %H:%M:%S')


def calculate_change(ticker):
    start = time.mktime(datetime.datetime(2016, 6, 30).timetuple())
    end = time.mktime(datetime.datetime.now().timetuple())
    print("ticker", ticker)
    trade_hist = polo.returnChartData(ticker, period=900, start=start,
                                      end=end)
    print(ticker, "#", len(trade_hist))
    weighted_avg = [a['weightedAverage'] for a in trade_hist]
    perc_chg = [((float(x) - float(weighted_avg[i - 1])) / float(
        weighted_avg[i - 1]))
                for i, x in enumerate(weighted_avg)][1:]
    chg = [(float(x) - float(weighted_avg[i - 1]))
           for i, x in enumerate(weighted_avg)][1:]
    date_arr = [a['date'] for a in trade_hist][1:]
    has_err = False if len(trade_hist) == 29459 else True
    return np.array(perc_chg), np.array(chg), np.array(date_arr), has_err


def random_portfolio(returns):
    def rand_weights(n):
        # Produces n random weights that sum to 1
        k = np.random.rand(n)
        return k / sum(k)

    '''
    Returns the mean and standard deviation of returns for a random portfolio
    '''
    p = np.asmatrix(np.mean(returns, axis=1))
    w = np.asmatrix(rand_weights(returns.shape[0]))
    C = np.asmatrix(np.cov(returns))

    mu = w * p.T
    sigma = np.sqrt(w * C * w.T)

    # This recursion reduces outliers to keep plots pretty
    if sigma > 2:
        return random_portfolio(returns)
    return mu, sigma


percent_change_arr = []
for ticker in tickers:
    percent_change, change, dates, err = calculate_change(ticker)
    if not err:
        percent_change_arr.append(percent_change)
n_portfolios = 500
means, stds = np.column_stack([
                                  random_portfolio(
                                      np.array(percent_change_arr))
                                  for _ in range(n_portfolios)
                                  ])
plt.plot(stds, means, 'o', markersize=5)
plt.ylabel('mean')
plt.xlabel('std')
plt.title('Mean and standard deviation of returns of randomly generated portfolios')
plt.show()
