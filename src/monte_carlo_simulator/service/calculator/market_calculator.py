

import pandas as pd
import numpy as np
from numbers import Number

from monte_carlo_simulator.service.util.price_col_checker import price_col_checker


def calc_market_returns(market_data: pd.DataFrame) -> float:
    """
    Calculates the annual returns of a market index like the S&P 500.

    Parameters: market_data - a pd.DataFrame containing historical market returns

    Returns: The annual returns of the chosen market index
    """
    # Verify market_data is a DataFrame 
    if (not isinstance(market_data, pd.DataFrame)):
        raise TypeError(f'"market_data" parameter must be a DataFrame, not {type()}')

    # Identify if 'Adj Close' is an available column or just 'Close'
    close_column = price_col_checker(market_data)

    # Convert daily closing price data into year-end market prices
    annual_returns = market_data[close_column].iloc[:, 0] \
        .resample('YE') \
        .last()

    # Change first item to starting market value for the time period
    annual_returns.iloc[0] = market_data[close_column].iloc[0, 0]

    # Calculate yearly returns for the market as the percentage price change
    return annual_returns.pct_change().mean()

def calc_daily_market_returns(market_data: pd.DataFrame) -> float:
    """
    Calculates the daily returns of a market index like the S&P 500.

    Parameters: market_data - a pd.DataFrame containing historical market returns

    Returns: The daily returns of the chosen market index
    """
    # Verify market_data is a DataFrame 
    if (not isinstance(market_data, pd.DataFrame)):
        raise TypeError(f'"market_data" parameter must be a DataFrame, not {type(market_data)}')

    # Identify if 'Adj Close' is an available column or just 'Close'
    close_column = price_col_checker(market_data)

    # Calculate daily market returns
    return market_data[close_column].iloc[:, 0] \
        .pct_change() \
        .mean()

def calc_rfr(rfr_data: pd.DataFrame) -> float:
    """
    Calculates the risk free rate from historical interest rates of 
    low-risk securities: (^IRX: 13-week, ^FVX: 5-year, ^TNX: 10-year, 
    ^TYX: 30-year)

    Parameters: rfr_data - a pd.Dataframe containing historical risk-free asset returns

    Returns: The average risk-free rate (risk_free_rate)
    """
    # Verify rfr_data is a DataFrame 
    if (not isinstance(rfr_data, pd.DataFrame)):
        raise TypeError(f'"rfr_data" parameter must be a DataFrame, not {type(rfr_data)}')

    # Identify if 'Adj Close' is an available column or just 'Close'
    close_column = price_col_checker(rfr_data)

    # Return the average risk free rate (the interest rate for the bond)
    return rfr_data[close_column].iloc[:, 0].mean()

def calc_daily_rfr(rfr_data: pd.DataFrame) -> float:
    """
    Calculates the daily risk-free rate from historical interest
    rates of low-risk securities.

    Parameters: rfr_data - a pd.Dataframe containing historical risk-free asset returns

    Return: A float representing the daily risk-free rate
    """
    # Verify rfr_data is a DataFrame 
    if (not isinstance(rfr_data, pd.DataFrame)):
        raise TypeError(f'"rfr_data" parameter must be a DataFrame, not {type(rfr_data)}')

    # Identify if 'Adj Close' is an available column or just 'Close'
    close_column = price_col_checker(rfr_data)

    # Find the daily returns from bond rates
    return rfr_data[close_column].iloc[:, 0] \
        .apply(lambda x: (1 + x / 100) ** (1 / 365) - 1) \
        .mean()


def calc_volatility(asset_data: pd.DataFrame, standev_window: int = 30) -> np.float64:
    """
    Determines historical asset volatility with a rolling window.
    Volatility = standard deviation of returns * sqrt(horizon time periods)

    Parameters: 
        asset_data - a pd.DataFrame containing historic asset data
        standev_window - an integer representing the rolling window to calculate 
            historic volatility 
            
    Returns: An np.float64 object representing the historic volatility for the most 
        recent time period (equal to the amount of days specified by the window param)
    """
    # Verify asset_data is a DataFrame
    if not isinstance(asset_data, pd.DataFrame):
        raise TypeError(f'"asset_data" parameter must be a DataFrame, not {type(asset_data)}')
    
    # Verify that window is an integer
    if not isinstance(standev_window, int):
        if isinstance(standev_window, Number):
            if standev_window <= 0:
                raise ValueError(f'"standev_window" parameter must be a positive integer, not {standev_window}') 
            standev_window = int(standev_window)
        else:
            raise TypeError(f'"standev_window" parameter must be a positive integer, not {type(standev_window)}')

    # Identify if 'Adj Close' is an available column or just 'Close'
    close_column = price_col_checker(asset_data)
    
    # Calculate logarithmic returns
    asset_data['Log Returns'] = (asset_data[close_column].iloc[:, 0].pct_change() + 1) \
            .apply(lambda x: np.log(x))

    # Check data length to ensure it is greater than the window size
    if len(asset_data) <= standev_window:
        # Set window to maximum length allowable by the size of the data set
        standev_window = len(asset_data)

    # Calculate rolling standard deviation for most recent time period
    # Using denominator degrees of freedom of 1
    his_vol = asset_data['Log Returns'].rolling(
        window=standev_window).std(ddof=1).iloc[-1] * np.sqrt(standev_window)

    return his_vol

