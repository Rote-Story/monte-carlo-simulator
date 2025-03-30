
from numbers import Number
from yfinance import Ticker

class AssetData:

    def __init__(self):
        self._asset_info: Ticker = None
        self._his_vol: Number = None
        self._beta: Number = None
        self._expected_returns: Number = None
        
    @property
    def asset_info(self):
        return self._asset_info

    @property
    def his_vol(self):
        return self._his_vol
    
    @property
    def beta(self):
        return self._beta    

    @property
    def expected_returns(self):
        return self._expected_returns
    
    @asset_info.setter
    def asset_info(self, asset_info: Ticker):
        if not isinstance(asset_info, Ticker):
            raise ValueError("Stock info must be a yfinance.Ticker object")
        self._asset_info = asset_info

    @his_vol.setter    
    def his_vol(self, his_vol: Number):
        if not isinstance(his_vol, Number) or his_vol < 0:
            raise ValueError("Historic volatility must be a positive numeric type")
        self._his_vol = his_vol
    
    @beta.setter    
    def beta(self, beta: Number):
        if not isinstance(beta, Number) or beta < 0:
            raise ValueError("Beta must be a positive numeric type")
        self._beta = beta
    
    @expected_returns.setter    
    def expected_returns(self, expected_returns: Number):
        if not isinstance(expected_returns, Number):
            raise ValueError("Expected returns must be a numeric type")
        self._expected_returns = expected_returns