

from pandas import DataFrame
from numbers import Number


class MarketData:

    def __init__(self):
        self._his_data: DataFrame = None
        self._market_symbol: str = None
        self._market_returns: Number = None
        self._daily_market_returns: Number = None

    @property
    def his_data(self) -> DataFrame:
        return self._his_data    
    
    @property
    def market_symbol(self) -> str:
        return self._market_symbol    

    @property
    def market_returns(self) -> Number:
        return self._market_returns

    @property
    def daily_market_returns(self) -> Number:
        return self._daily_market_returns

    @his_data.setter    
    def his_data(self, his_data: DataFrame) -> None:
        if not isinstance(his_data, DataFrame):
            raise ValueError("Market data must be a pandas DataFrame object")
        self._his_data = his_data
    
    @market_symbol.setter    
    def market_symbol(self, market_symbol: str) -> None:
        if not isinstance(market_symbol, str):
            raise ValueError("Market symbol must be a string object")
        elif str.isspace(market_symbol):
            raise ValueError("Market symbol must not be blank")
        elif len(market_symbol) == 0:
            raise ValueError("Market symbol must not be empty")
        self._market_symbol = market_symbol

    @market_returns.setter    
    def market_returns(self, market_returns: Number) -> None:
        if not isinstance(market_returns, Number):
            raise ValueError("Market returns must be a numeric data type")
        self._market_returns = market_returns

    @daily_market_returns.setter    
    def daily_market_returns(self, daily_market_returns: Number) -> None:
        if not isinstance(daily_market_returns, Number):
            raise ValueError("Daily market returns must be a numeric data type")
        self._daily_market_returns = daily_market_returns