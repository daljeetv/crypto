from __future__ import print_function, division
# from yahoo_finance import Share
# from yahoo_finance import Currency
from poloniex import Poloniex
from datetime import timedelta
import pandas as pd
import portfolioopt as pfopt

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
df = pd.read_csv(filepath_or_buffer='/tmp/random_df.csv')
df = df[tickers].convert_objects(convert_numeric=True)
returns = df.pct_change(1)
avg_rets = returns.mean()
cov_mat = returns.cov()


def section(caption):
    print('\n\n' + str(caption))
    print('-' * len(caption))


def print_portfolio_info(returns, avg_rets, weights):
    """
    Print information on expected portfolio performance.
    """
    ret = (weights * avg_rets).sum()
    std = (weights * returns).sum(1).std()
    sharpe = ret / std
    print("Optimal weights:\n{}\n".format(weights))
    print("Expected return:   {}".format(ret))
    print("Expected variance: {}".format(std**2))
    print("Expected Sharpe:   {}".format(sharpe))


# Define some target return, here the 70% quantile of the average returns
target_ret = avg_rets.quantile(0.9)
weights = pfopt.min_var_portfolio(cov_mat)
print_portfolio_info(returns, avg_rets, weights)

section("Markowitz portfolio (long only, target return: {:.5f})".format(target_ret))
weights = pfopt.markowitz_portfolio(cov_mat, avg_rets, target_ret)
print_portfolio_info(returns, avg_rets, weights)

section("Tangency portfolio (long only)")
weights = pfopt.tangency_portfolio(cov_mat, avg_rets)
weights = pfopt.truncate_weights(weights)   # Truncate some tiny weights
print_portfolio_info(returns, avg_rets, weights)
