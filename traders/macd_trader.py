from __future__ import print_function, division
from poloniex import Poloniex
import pandas as pd
import datetime
import time

tickers = ["BTC_XVC"]


def calc_positions(macd_short=[], macd_long=[], prices=[]):
    def short_or_long(short=0, long=0):
        return "short" if short > long else "long"
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


def get_trade_hist(ticker=""):
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
        start = time.mktime(datetime.datetime(2012, 4, 30).timetuple())
        end = time.mktime(datetime.datetime.now().timetuple())
        return polo.returnChartData(ticker,
                                    period=300,
                                    start=start,
                                    end=end)


if __name__ == '__main__':
    polo = Poloniex(timeout=10)
    for ticker in tickers:
        print('currency_pair: %s' % ticker)
        trade_hist = get_trade_hist(ticker=ticker)
        time_price_dict = {}
        for trade in trade_hist:
            time_price_dict[trade['date']] = trade['weightedAverage']
        prices_arr = [(k, v) for k, v in time_price_dict.iteritems()]
        prices_arr.sort(key=lambda tup: tup[0])
        df = pd.DataFrame(
                {'value': [v for k, v in prices_arr]},
                index=[pd.to_datetime(key, unit='s')
                       for key in [k for k, v in prices_arr]])
        macd_short = df.rolling('7400s').mean()
        macd_long = df.rolling('86400s').mean()
        trades = calc_positions(macd_short, macd_long, df)
        total_gain = 0
        for t in range(2, len(trades)):
            gain = float(trades[t]['price']) - float(trades[t-1]['price'])
            total_gain += gain
        print(total_gain)
