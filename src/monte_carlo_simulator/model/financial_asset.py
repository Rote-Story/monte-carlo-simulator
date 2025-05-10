
from numbers import Number
from yfinance import Ticker
from pandas import DataFrame

from monte_carlo_simulator.const import TIME_PERIODS


class FinancialAsset:

    def __init__(self):
        self._asset_ticker: Ticker = None
        self._period: str = None
        self._asset_symbol: str = None
        self._asset_data: DataFrame = None
        self._his_vol: Number = None
        self._beta: Number = None
        self._expected_returns: Number = None
        self._exp_ret_flag: str = None

    @property
    def asset_ticker(self) -> Ticker:
        return self._asset_ticker

    @property
    def period(self) -> str:
        return self._period

    @property
    def asset_symbol(self) -> str:
        return self._asset_symbol

    @property
    def asset_data(self) -> DataFrame:
        return self._asset_data

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
    def exp_ret_flag(self) -> str:
        return self._exp_ret_flag

    @asset_ticker.setter
    def asset_ticker(self, asset_ticker: Ticker) -> None:
        if not isinstance(asset_ticker, Ticker):
            raise TypeError('Asset ticker must be a yfinance.Ticker object')
        self._asset_ticker = asset_ticker

    @period.setter
    def period(self, period: str) -> None:
        # Time period combobox entry is restricted to TIME_PERIODS values
        if type(period) != str:
            raise TypeError(f'Time period must be a string in the list of valid time periods, {period} is not')
        elif period not in TIME_PERIODS.values():
            raise ValueError(f'Time period must be in the list of valid time periods, {period} is not')
        self._period = period

    @asset_symbol.setter
    def asset_symbol(self, asset_symbol: str) -> None:
        if type(asset_symbol) != str:
            raise TypeError('Asset symbol must be a string object')
        self._asset_symbol = asset_symbol

    @asset_data.setter
    def asset_data(self, asset_data: DataFrame) -> None:
        if not isinstance(asset_data, DataFrame):
            raise TypeError('Asset data must be a pandas.DataFrame object')
        self._asset_data = asset_data

    @his_vol.setter    
    def his_vol(self, his_vol: Number) -> None:
        if not isinstance(his_vol, Number):
            raise TypeError('Historic volatility must be a positive numeric type')
        elif his_vol < 0:
            raise ValueError('Historic volatility must be positive')
        self._his_vol = his_vol
    
    @beta.setter    
    def beta(self, beta: Number) -> None:
        if not isinstance(beta, Number):
            raise TypeError('Beta must be a positive numeric type')
        elif beta < 0:
            raise ValueError('Beta must be positive')
        self._beta = beta
    
    @expected_returns.setter    
    def expected_returns(self, expected_returns: Number) -> None:
        if not isinstance(expected_returns, Number):
            raise TypeError('Expected returns must be a numeric type')
        self._expected_returns = expected_returns

    @exp_ret_flag.setter    
    def exp_ret_flag(self, exp_ret_flag: str) -> None:
        if type(exp_ret_flag) != str:
            raise TypeError('Expected returns flag must be a string type')
        self._exp_ret_flag = exp_ret_flag
