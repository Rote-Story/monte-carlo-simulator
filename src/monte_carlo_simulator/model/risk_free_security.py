

from pandas import DataFrame
from numbers import Number


class RiskFreeSecurity:

    def __init__(self):
        self._rfr_data: DataFrame = None
        self._rfr_symbol: str = None
        self._risk_free_rate: Number = None

    @property
    def rfr_data(self) -> DataFrame:
        return self._rfr_data    
    
    @property
    def rfr_symbol(self) -> str:
        return self._rfr_symbol

    @property
    def risk_free_rate(self) -> Number:
        return self._risk_free_rate

    @rfr_data.setter    
    def rfr_data(self, rfr_data: DataFrame) -> None:
        if not isinstance(rfr_data, DataFrame):
            raise TypeError('Historic risk-free rate data must be a pandas DataFrame object')
        self._rfr_data = rfr_data

    @rfr_symbol.setter
    def rfr_symbol(self, rfr_symbol: str) -> None:
        if type(rfr_symbol) != str:
            raise TypeError('Risk-free rate symbol must be a string object')
        elif str.isspace(rfr_symbol):
            raise ValueError('Risk-free rate symbol must not be blank')
        elif len(rfr_symbol) == 0:
            raise ValueError('Risk-free rate symbol must not be empty')
        self._rfr_symbol = rfr_symbol
    
    @risk_free_rate.setter    
    def risk_free_rate(self, risk_free_rate: Number) -> None:
        if not isinstance(risk_free_rate, Number):
            raise TypeError('Risk-free rate must be a numeric data type')
        self._risk_free_rate = risk_free_rate