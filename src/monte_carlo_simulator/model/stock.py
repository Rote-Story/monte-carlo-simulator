
from pandas import Series
from numbers import Number

from .financial_asset import FinancialAsset

class Stock(FinancialAsset):
    """
    Stock data class for storing and validating fetched 
    data. Inherits from AssetData class to add stock-specific
    information.
    """
    def __init__(self):
        super().__init__()
        self._his_div: Series = None
        self._div_growth_rate: Number = None

    @property
    def his_div(self) -> Series:
        return self._his_div
    
    @property
    def div_growth_rate(self) -> Number:
        return self._div_growth_rate

    @his_div.setter 
    def his_div(self, his_div: Series) -> None:
        if not isinstance(his_div, Series):
            raise ValueError('Historic dividends must be a pandas.Series object')
        self._his_div = his_div

    @div_growth_rate.setter
    def div_growth_rate(self, div_growth_rate: Number) -> None:
        if not isinstance(div_growth_rate, Number) or div_growth_rate < 0:
            raise ValueError('Dividend growth rate must be a positive numeric type')
        self._div_growth_rate = div_growth_rate