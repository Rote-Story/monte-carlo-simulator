

from pandas import DataFrame
from numbers import Number


class RiskFreeRateData:

    def __init__(self):
        self._his_data: DataFrame = None
        self._rfr_symbol: str = None
        self._risk_free_rate: Number = None
        self._daily_risk_free_rate: Number = None 

    @property
    def his_data(self) -> DataFrame:
        return self._his_data    
    
    @property
    def rfr_symbol(self) -> str:
        return self._rfr_symbol

    @property
    def risk_free_rate(self) -> Number:
        return self._risk_free_rate

    @property
    def daily_risk_free_rate(self) -> Number:
        return self._daily_risk_free_rate

    @his_data.setter    
    def his_data(self, his_data: DataFrame) -> None:
        if not isinstance(his_data, DataFrame):
            raise ValueError("Historic risk-free rate data must be a pandas DataFrame object")
        self._his_data = his_data

    @rfr_symbol.setter    
    def rfr_symbol(self, rfr_symbol: str) -> None:
        if not isinstance(rfr_symbol, str):
            raise ValueError("Risk-free rate symbol must be a string object")
        elif str.isspace(rfr_symbol):
            raise ValueError("Risk-free rate symbol must not be blank")
        elif len(rfr_symbol) == 0:
            raise ValueError("Risk-free rate symbol must not be empty")
        self._rfr_symbol = rfr_symbol
    
    @risk_free_rate.setter    
    def risk_free_rate(self, risk_free_rate: Number) -> None:
        if not isinstance(risk_free_rate, Number):
            raise ValueError("Risk-free rate must be a numeric data type")
        self._risk_free_rate = risk_free_rate

    @daily_risk_free_rate.setter    
    def daily_risk_free_rate(self, daily_risk_free_rate: Number) -> None:
        if not isinstance(daily_risk_free_rate, Number):
            raise ValueError("Daily risk-free rate must be a numeric data type")
        self._daily_risk_free_rate = daily_risk_free_rate