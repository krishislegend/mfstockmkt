"""
common/volatility.py

(c) 2015-2017 Marshall Farrier
license http://opensource.org/licenses/MIT

Calculate volatility
"""

from argparse import ArgumentParser
import math

import numpy as np
import pandas as pd
import pandas_datareader as web


class InsufficientData(Exception):
    pass


def get(eqdata, window=1, selection='Adj Close'):
    return math.sqrt(window) * get_daily(eqdata, selection)

def get_daily(eqdata, selection='Adj Close'):
    growthdata = _get_growth_data(eqdata, selection)
    return _get_daily(growthdata)

def show(n_sessions, _volatility, ave_daily_return, price):
    price = float(price)
    diff = price * _volatility
    mean_price = price + .5 * ave_daily_return * price * n_sessions
    suffix = '' if n_sessions == 1 else 's'
    print('Volatility over {} session{} : {:.2f} pct'.format(n_sessions, suffix, _volatility * 100.))
    print('Expected return over {} session{} : {:.2f} pct'.format(n_sessions, suffix, ave_daily_return * 100. * n_sessions))
    print('Reference price: $ {:.2f}'.format(price))
    print('Range of 1 std up or down with growth adjustment:')
    print('Low price: $ {:.2f}'.format(mean_price - diff))
    print('High price: $ {:.2f}'.format(mean_price + diff))

def _get(growthdata, window=1):
    return math.sqrt(window) * _get_daily(growthdata)

def _get_daily(growthdata):
    return float(np.std(growthdata.values, dtype=np.float64))

def _get_growth_data(eqdata, selection):
    growthdata = pd.DataFrame(index=eqdata.index[1:], 
            columns=['Growth'], dtype=np.float64)
    growthdata.loc[:, 'Growth'] = (eqdata.loc[:, selection].values[1:] /
            eqdata.loc[:, selection].values[:-1])
    return growthdata

def _get_eqdata(**kwargs):
    eqdata = web.DataReader(kwargs['equity'], 'yahoo', start=kwargs['start'])
    return eqdata

def _get_start():
    return pd.to_datetime('today') - pd.DateOffset(years=1) - pd.DateOffset()

def _get_cli_args():
    parser = ArgumentParser()
    parser.add_argument('equity')
    parser.add_argument('-w', '--window', help='sessions (not days) in volatility window', type=int, default=21)
    return vars(parser.parse_args())


if __name__ == '__main__':
    kwargs = _get_cli_args()
    kwargs['start'] = _get_start()
    eqdata = _get_eqdata(**kwargs)
    if eqdata.index[0] > kwargs['start'] + 5 * pd.DateOffset():
        raise InsufficientData("insufficient data for equity '{}'".format(kwargs['equity']))
    selection = 'Adj Close'
    growthdata = _get_growth_data(eqdata, selection)
    _volatility = _get(growthdata, kwargs['window'])
    ave_daily_return = float(np.mean(growthdata.values, dtype=np.float64)) - 1.
    show(kwargs['window'], _volatility, ave_daily_return, eqdata.loc[:, 'Adj Close'].values[-1])

