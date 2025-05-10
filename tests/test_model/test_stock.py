
from unittest.mock import Mock
from pandas import DataFrame, Series
import numpy as np
from pandas.testing import assert_series_equal
import unittest
from yfinance import Ticker

from monte_carlo_simulator.model.stock import Stock
from tests.test_model.test_financial_asset import TestFinancialAsset

class TestStockData(TestFinancialAsset, unittest.TestCase):

    def setUp(self):
        self.financial_asset = Stock()
        self.mock_ticker = Mock(spec=Ticker)
        self.test_dataframe = DataFrame(np.linspace(-10.0, 10.0, num=10))
        self.test_zeros_dataframe = DataFrame(np.zeros((2, 2)))
        self.test_series = Series([1, 2, 3, 4, 5, 6, 7, 8])
        self.test_zeros_series = Series([0, 0, 0, 0])


    # test his_div
    def test_his_div_dataframe_input(self):
        self.financial_asset.his_div = self.test_series
        assert_series_equal(self.test_series, self.financial_asset.his_div)
    
    def test_his_div_dataframe_input_zeros(self):
        self.financial_asset.his_div = self.test_zeros_series
        assert_series_equal(self.test_zeros_series, self.financial_asset.his_div)

    def test_his_div_list_input(self):
        try:
            self.financial_asset.his_div = [[0, 0, 0, 0], [0, 0, 0, 0]]
        except ValueError as e:
            self.assertEqual(str(e), 'Historic dividends must be a pandas.Series object')
    
    def test_his_div_dict_input(self):
        try:
            self.financial_asset.his_div = {'zero': 0, 'one': 1}
        except ValueError as e:
            self.assertEqual(str(e), 'Historic dividends must be a pandas.Series object')
    
    def test_his_div_int_input(self):
        try:
            self.financial_asset.his_div = 0
        except ValueError as e:
            self.assertEqual(str(e), 'Historic dividends must be a pandas.Series object')

    def test_his_div_float_input(self):
        try:
            self.financial_asset.his_div = 0.0
        except ValueError as e:
            self.assertEqual(str(e), 'Historic dividends must be a pandas.Series object')

    def test_his_div_none_input(self):
        try:
            self.financial_asset.his_div = None
        except ValueError as e:
            self.assertEqual(str(e), 'Historic dividends must be a pandas.Series object')

    # test div_growth_rate
    def test_div_growth_rate_float_input(self):
        self.financial_asset.div_growth_rate = 0.15
        self.assertEqual(0.15, self.financial_asset.div_growth_rate)

    def test_div_growth_rate_int_input(self):
        self.financial_asset.div_growth_rate = 0
        self.assertEqual(0, self.financial_asset.div_growth_rate)

    def test_div_growth_rate_negative_int_input(self):
        try:
            self.financial_asset.div_growth_rate = -1
        except ValueError as e:
            self.assertEqual(str(e), 'Dividend growth rate must be a positive numeric type')
    
    def test_div_growth_rate_negative_float_input(self):
        try:
            self.financial_asset.div_growth_rate = -1.15
        except ValueError as e:
            self.assertEqual(str(e), 'Dividend growth rate must be a positive numeric type')

    def test_div_growth_rate_list_input(self):
        try:
            self.financial_asset.div_growth_rate = [[0, 0, 0, 0], [0, 0, 0, 0]]
        except ValueError as e:
            self.assertEqual(str(e), 'Dividend growth rate must be a positive numeric type')
    
    def test_div_growth_rate_dict_input(self):
        try:
            self.financial_asset.div_growth_rate = {'zero': 0, 'one': 1}
        except ValueError as e:
            self.assertEqual(str(e), 'Dividend growth rate must be a positive numeric type')

    def test_div_growth_rate_str_input(self):
        try:
            self.financial_asset.div_growth_rate = '0.15'
        except ValueError as e:
            self.assertEqual(str(e), 'Dividend growth rate must be a positive numeric type')

    def test_div_growth_rate_none_input(self):
        try:
            self.financial_asset.div_growth_rate = None
        except ValueError as e:
            self.assertEqual(str(e), 'Dividend growth rate must be a positive numeric type')


if __name__ == '__main__':
    unittest.main()