
from numbers import Number
from yfinance import Ticker
from pandas import DataFrame
class AssetData:

    def __init__(self):
        self._asset_ticker: Ticker = None
        self._period: str = None
        self._asset_symbol: str = None
        self._his_data: DataFrame = None
        self._his_vol: Number = None
        self._beta: Number = None
        self._expected_returns: Number = None
        self._daily_expected_returns: Number = None
        
    @property
    def asset_info(self) -> Ticker:
        return self._asset_info

    @property
    def period(self) -> str:
        return self._period

    @property
    def asset_symbol(self) -> str:
        return self._asset_symbol

    @property
    def his_data(self) -> DataFrame:
        return self._his_data

    @property
    def his_vol(self) -> Number:
        return self._his_vol
    
    @property
    def beta(self) -> Number:
        return self._beta    

    @property
    def expected_returns(self) -> Number:
        return self._expected_returns

    @property
    def daily_expected_returns(self) -> Number:
        return self._daily_expected_returns
    
    @asset_info.setter
    def asset_info(self, asset_info: Ticker) -> None:
        if not isinstance(asset_info, Ticker):
            raise ValueError("Asset info must be a yfinance.Ticker object")
        self._asset_info = asset_info

    @asset_symbol.setter
    def period(self, period: str) -> None:
        if not isinstance(period, str):
            raise ValueError("Time period must be a string object")
        self._period = period

    @asset_symbol.setter
    def asset_symbol(self, asset_symbol: str) -> None:
        if not isinstance(asset_symbol, str):
            raise ValueError("Asset symbol must be a string object")
        self._asset_symbol = asset_symbol

    @his_data.setter
    def his_data(self, his_data: DataFrame) -> None:
        if not isinstance(his_data, DataFrame):
            raise ValueError("Asset info must be a pandas.DataFrame object")
        self._his_data = his_data

    @his_vol.setter    
    def his_vol(self, his_vol: Number) -> None:
        if not isinstance(his_vol, Number) or his_vol < 0:
            raise ValueError("Historic volatility must be a positive numeric type")
        self._his_vol = his_vol
    
    @beta.setter    
    def beta(self, beta: Number) -> None:
        if not isinstance(beta, Number) or beta < 0:
            raise ValueError("Beta must be a positive numeric type")
        self._beta = beta
    
    @expected_returns.setter    
    def expected_returns(self, expected_returns: Number) -> None:
        if not isinstance(expected_returns, Number):
            raise ValueError("Expected returns must be a numeric type")
        self._expected_returns = expected_returns

    @daily_expected_returns.setter    
    def daily_expected_returns(self, daily_expected_returns: Number) -> None:
        if not isinstance(daily_expected_returns, Number):
            raise ValueError("Expected returns must be a numeric type")
        self._daily_expected_returns = daily_expected_returns