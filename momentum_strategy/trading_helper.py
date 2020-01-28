import pandas as pd
import numpy as np


def get_tickers(markets):
  prices = []
  for market in markets:
      data = pd.read_csv('./tickerData/' + market + '.txt')
      data['ticker'] = market
      data['DATE'] =  pd.to_datetime(data['DATE'], format='%Y%m%d')
      prices.append(data)
  prices = pd.concat(prices, sort = True)
  prices = prices.reset_index(drop=True)
  prices.columns = ['close', 'high', 'low', 'open', 'vol', 'p', 'date', 'ticker']
  return prices

def get_ohlcv(prices):
  open_prices = prices.pivot(index='date', columns='ticker', values='open')
  high_prices = prices.pivot(index='date', columns='ticker', values='high')
  low_prices = prices.pivot(index='date', columns='ticker', values='low')
  close_prices = prices.pivot(index='date', columns='ticker', values='close')
  volume = prices.pivot(index='date', columns='ticker', values='vol')
  return open_prices, high_prices, low_prices, close_prices, volume
  
def resample_prices(prices, freq='D'):
    """
    Resample close prices for each ticker at specified frequency.
    
    Parameters
    ----------
    close_prices : DataFrame
        Close prices for each ticker and date
    freq : str
        What frequency to sample at
        For valid freq choices, see http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
    
    Returns
    -------
    prices_resampled : DataFrame
        Resampled prices for each ticker and date
    """
    
    return prices.resample(freq).last()



def compute_log_returns(prices):
    """
    Compute log returns for each ticker.
    
    Parameters
    ----------
    prices : DataFrame
        Prices for each ticker and date
    
    Returns
    -------
    log_returns : DataFrame
        Log returns for each ticker and date
    """
    returns = (prices - prices.shift(1) )/prices.shift(1)
    return np.log(1 + returns)

def shift_returns(returns, shift_n):
    """
    Generate shifted returns
    
    Parameters
    ----------
    returns : DataFrame
        Returns for each ticker and date
    shift_n : int
        Number of periods to move, can be positive or negative
    
    Returns
    -------
    shifted_returns : DataFrame
        Shifted returns for each ticker and date
    """
    
    return returns.shift(shift_n)

def get_top_n(prev_returns, top_n):
    """
    Select the top performing stocks
    
    Parameters
    ----------
    prev_returns : DataFrame
        Previous shifted returns for each ticker and date
    top_n : int
        The number of top performing stocks to get
    
    Returns
    -------
    top_stocks : DataFrame
        Top stocks for each ticker and date marked with a 1
    """
    return prev_returns.apply(lambda x: x >= pd.Series.nlargest(x, top_n).min(), axis=1).astype('int64')

def portfolio_returns(df_long, df_short, lookahead_returns, n_stocks):
    """
    Compute expected returns for the portfolio, assuming equal investment in each long/short stock.
    
    Parameters
    ----------
    df_long : DataFrame
        Top stocks for each ticker and date marked with a 1
    df_short : DataFrame
        Bottom stocks for each ticker and date marked with a 1
    lookahead_returns : DataFrame
        Lookahead returns for each ticker and date
    n_stocks: int
        The number number of stocks chosen for each month
    
    Returns
    -------
    portfolio_returns : DataFrame
        Expected portfolio returns for each ticker and date
    """
    # TODO: Implement Function
    
    return (df_long - df_short) * lookahead_returns / n_stocks