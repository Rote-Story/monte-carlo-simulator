

from pandas import DataFrame
from numbers import Number


class MarketIndex:

    def __init__(self):
        self._market_data: DataFrame = None
        self._market_symbol: str = None
        self._market_returns: Number = None

    @property
    def market_data(self) -> DataFrame:
        return self._market_data    
    
    @property
    def market_symbol(self) -> str:
        return self._market_symbol    

    @property
    def market_returns(self) -> Number:
        return self._market_returns

    @market_data.setter    
    def market_data(self, market_data: DataFrame) -> None:
        if not isinstance(market_data, DataFrame):
            raise TypeError('Market data must be a pandas DataFrame object')
        self._market_data = market_data
    
    @market_symbol.setter    
    def market_symbol(self, market_symbol: str) -> None:
        if type(market_symbol) != str:
            raise TypeError('Market symbol must be a string object')
        elif str.isspace(market_symbol):
            raise ValueError('Market symbol must not be blank')
        elif len(market_symbol) == 0:
            raise ValueError('Market symbol must not be empty')
        self._market_symbol = market_symbol

    @market_returns.setter    
    def market_returns(self, market_returns: Number) -> None:
        if not isinstance(market_returns, Number):
            raise TypeError('Market returns must be a numeric data type')
        self._market_returns = market_returns
