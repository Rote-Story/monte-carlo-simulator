
from pandas import DataFrame
import numpy as np
from pandas.testing import assert_frame_equal
import unittest

from monte_carlo_simulator.data_classes.stock_data import StockData
from tests.test_data.test_asset_data import TestAssetData

class TestStockData(TestAssetData, unittest.TestCase):

    test_stock_data = StockData()
    test_dataframe = DataFrame(np.linspace(-10.0, 10.0, num=10))
    test_zeros_dataframe = DataFrame(np.zeros((2, 2)))

    # test his_div
    def test_his_div_dataframe_input(self):
        self.test_stock_data.his_div = self.test_dataframe
        assert_frame_equal(self.test_stock_data.his_div, self.test_dataframe)
    
    def test_his_div_dataframe_input(self):
        self.test_stock_data.his_div = self.test_zeros_dataframe
        assert_frame_equal(self.test_zeros_dataframe, self.test_stock_data.his_div)

    def test_his_div_list_input(self):
        try:
            self.test_stock_data.his_div = [[0, 0, 0, 0], [0, 0, 0, 0]]
        except ValueError as e:
            self.assertEqual(str(e), "Historic dividends must be a DataFrame object")
    
    def test_his_div_dict_input(self):
        try:
            self.test_stock_data.his_div = {"zero": 0, "one": 1}
        except ValueError as e:
            self.assertEqual(str(e), "Historic dividends must be a DataFrame object")
    
    def test_his_div_int_input(self):
        try:
            self.test_stock_data.his_div = 0
        except ValueError as e:
            self.assertEqual(str(e), "Historic dividends must be a DataFrame object")

    def test_his_div_float_input(self):
        try:
            self.test_stock_data.his_div = 0.0
        except ValueError as e:
            self.assertEqual(str(e), "Historic dividends must be a DataFrame object")

    def test_his_div_none_input(self):
        try:
            self.test_stock_data.his_div = None
        except ValueError as e:
            self.assertEqual(str(e), "Historic dividends must be a DataFrame object")

    # test div_growth_rate
    def test_div_growth_rate_float_input(self):
        self.test_stock_data.div_growth_rate = 0.15
        self.assertEqual(0.15, self.test_stock_data.div_growth_rate)

    def test_div_growth_rate_int_input(self):
        self.test_stock_data.div_growth_rate = 0
        self.assertEqual(0, self.test_stock_data.div_growth_rate)

    def test_div_growth_rate_negative_int_input(self):
        try:
            self.test_stock_data.div_growth_rate = -1
        except ValueError as e:
            self.assertEqual(str(e), "Dividend growth rate must be a positive numeric type")
    
    def test_div_growth_rate_negative_float_input(self):
        try:
            self.test_stock_data.div_growth_rate = -1.15
        except ValueError as e:
            self.assertEqual(str(e), "Dividend growth rate must be a positive numeric type")

    def test_div_growth_rate_list_input(self):
        try:
            self.test_stock_data.div_growth_rate = [[0, 0, 0, 0], [0, 0, 0, 0]]
        except ValueError as e:
            self.assertEqual(str(e), "Dividend growth rate must be a positive numeric type")
    
    def test_div_growth_rate_dict_input(self):
        try:
            self.test_stock_data.div_growth_rate = {"zero": 0, "one": 1}
        except ValueError as e:
            self.assertEqual(str(e), "Dividend growth rate must be a positive numeric type")

    def test_div_growth_rate_str_input(self):
        try:
            self.test_stock_data.div_growth_rate = "0.15"
        except ValueError as e:
            self.assertEqual(str(e), "Dividend growth rate must be a positive numeric type")

    def test_div_growth_rate_none_input(self):
        try:
            self.test_stock_data.div_growth_rate = None
        except ValueError as e:
            self.assertEqual(str(e), "Dividend growth rate must be a positive numeric type")


if __name__ == "__main__":
    unittest.main()