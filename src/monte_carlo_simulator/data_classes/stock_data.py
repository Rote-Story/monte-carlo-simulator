
from pandas import DataFrame
from numbers import Number

from .asset_data import AssetData

class StockData(AssetData):
    """
    Stock data class for storing and validating fetched 
    data. Inherits from AssetData class to add stock-specific
    information.
    """
    def __init__(self):
        super().__init__()
        self._his_div: DataFrame = None
        self._div_growth_rate: Number = None

    @property
    def his_div(self) -> DataFrame:
        return self._his_div
    
    @property
    def div_growth_rate(self) -> Number:
        return self._div_growth_rate

    @his_div.setter 
    def his_div(self, his_div: DataFrame) -> None:
        if not isinstance(his_div, DataFrame):
            raise ValueError("Historic dividends must be a DataFrame object")
        self._his_div = his_div

    @div_growth_rate.setter
    def div_growth_rate(self, div_growth_rate: Number) -> None:
        if not isinstance(div_growth_rate, Number) or div_growth_rate < 0:
            raise ValueError("Dividend growth rate must be a positive numeric type")
        self._div_growth_rate = div_growth_rate