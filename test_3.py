from __future__ import print_function, division
from poloniex import Poloniex

# import numpy as np
# import cvxopt as opt
# from cvxopt import blas, solvers
import pandas as pd
import datetime
import time
# import matplotlib.pyplot as plt

tickers = ["BTC_XVC"]


def unix_to_date(unix_timestamp):
    return datetime.datetime.fromtimestamp(
        int(unix_timestamp)
    ).strftime('%Y-%m-%d %H:%M:%S')


def calc_positions(macd_short=[], macd_long=[], prices=[]):
    def short_or_long(short=0, long=0):
        if short > long:
            return "short"
        else:
            return "long"
    trades = []
    current_position = short_or_long(macd_short.value[0], macd_long.value[0])
    for tick in range(1, len(macd_long)):
        next_pos = short_or_long(macd_short.value[tick], macd_long.value[tick])
        if current_position != next_pos:
            trades.append(
                    dict(date=prices.index[tick],
                         trade=next_pos,
                         price=prices.value[tick]))
        current_position = next_pos
    return trades


if __name__ == '__main__':
    polo = Poloniex(timeout=10)
    for ticker in tickers:
        print('currency_pair: %s' % ticker)
        start = time.mktime(datetime.datetime(2012, 4, 30).timetuple())
        end = time.mktime(datetime.datetime.now().timetuple())
        """
           [{
               u'volume': u'1.43391941',
               u'quoteVolume': u'9788.07182019',
               u'high': u'0.00014674',
               u'low': u'0.00014049',
               u'date': u'1494698100',
               u'close': u'0.00014163',
               u'weightedAverage': u'0.00014649',
               u'open': u'0.00014091'
            }]
        """
        trade_hist = polo.returnChartData(ticker,
                                          period=300,
                                          start=start,
                                          end=end)
        last_timestamp = trade_hist[-1]['date']
        time_price_dict = {}
        for trade in trade_hist:
            time_price_dict[trade['date']] = trade['weightedAverage']
        prices_arr = [(k, v) for k, v in time_price_dict.iteritems()]
        prices_arr.sort(key=lambda tup: tup[0])
        df = pd.DataFrame(
                {'value': [v for k, v in prices_arr]},
                index=[pd.to_datetime(key, unit='s')
                       for key in [k for k, v in prices_arr]])
        prices = df.rolling('300s').mean()
        macd_short = df.rolling('7400s').mean()
        macd_long = df.rolling('86400s').mean()
        # ax = macd_short.plot(kind='line')
        # ax = macd_long.plot(ax=ax)
        # ax = prices.plot(ax=ax)
        # plt.plot(stds, means, 'o', markersize=5)
        # plt.ylabel('mean')
        # plt.xlabel('std')
        # plt.title('Momentum')
        # plt.show(block=True)
        trades = calc_positions(macd_short, macd_long, df)
        total_gain = 0
        for t in range(2, len(trades)):
            gain = float(trades[t]['price']) - float(trades[t-1]['price'])
            print('gain %f' % gain)
            total_gain += gain
        print(total_gain)
