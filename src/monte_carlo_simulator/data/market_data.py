

from pandas import DataFrame
from numbers import Number


class MarketData:

    def __init__(self):
        self._market_data: DataFrame = None
        self._rfr_data: DataFrame = None
        self._market_returns: Number = None
        self._risk_free_rate: Number = None

    @property
    def market_data(self):
        return self._market_data    

    @property
    def rfr_data(self):
        return self._rfr_data

    @property
    def market_returns(self):
        return self._market_returns

    @property
    def risk_free_rate(self):
        return self._risk_free_rate

    @market_data.setter    
    def market_data(self, market_data: DataFrame):
        if not isinstance(market_data, DataFrame):
            raise ValueError("Market data must be a pandas DataFrame object")
        self._market_data = market_data
    
    @rfr_data.setter    
    def rfr_data(self, rfr_data: DataFrame):
        if not isinstance(rfr_data, DataFrame):
            raise ValueError("Risk free rate data must be a pandas DataFrame object")
        self._rfr_data = rfr_data

    @market_returns.setter    
    def market_returns(self, market_returns: Number):
        if not isinstance(market_returns, Number):
            raise ValueError("Market returns must be a numeric data type")
        self._market_returns = market_returns
    
    @risk_free_rate.setter    
    def risk_free_rate(self, risk_free_rate: Number):
        if not isinstance(risk_free_rate, Number):
            raise ValueError("Risk-free rate must be a numeric data type")
        self._risk_free_rate = risk_free_rate