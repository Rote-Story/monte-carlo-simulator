
import unittest
from pandas import DataFrame
from pandas.testing import assert_frame_equal
import numpy as np

from monte_carlo_simulator.data_classes.market_data import MarketData

class TestMarketData(unittest.TestCase):

    test_market_data = MarketData()
    test_dataframe = DataFrame(np.linspace(0.0, 3.0, num=5))
    test_zeros_dataframe = DataFrame(np.zeros((4, 4)))

    # Test his_data attributes
    def test_market_data_dataframe_input(self):
        self.test_market_data.his_data = self.test_dataframe
        assert_frame_equal(self.test_dataframe, self.test_market_data.his_data)

    def test_market_data_zeros_dataframe_input(self):
        self.test_market_data.his_data = self.test_zeros_dataframe
        assert_frame_equal(self.test_zeros_dataframe, self.test_market_data.his_data)

    def test_market_data_list_input(self):
        try:
            self.test_market_data.his_data = [[0, 0, 0, 0], [0, 0, 0, 0]]
        except ValueError as e:
            self.assertEqual(str(e), "Market data must be a pandas DataFrame object")
    
    def test_market_data_dict_input(self):
        try:
            self.test_market_data.his_data = {"zero": 0, "one": 1}
        except ValueError as e:
            self.assertEqual(str(e), "Market data must be a pandas DataFrame object")
    
    def test_market_data_int_input(self):
        try:
            self.test_market_data.his_data = 0
        except ValueError as e:
            self.assertEqual(str(e), "Market data must be a pandas DataFrame object")

    def test_market_data_float_input(self):
        try:
            self.test_market_data.his_data = 0.0
        except ValueError as e:
            self.assertEqual(str(e), "Market data must be a pandas DataFrame object")

    def test_market_data_none_input(self):
        try:
            self.test_market_data.his_data = None
        except ValueError as e:
            self.assertEqual(str(e), "Market data must be a pandas DataFrame object")

   # Test market_symbol attributes
    def test_market_data_valid_str_input(self):
        self.test_market_data.market_symbol = "AAPL"
        self.assertEqual("AAPL", self.test_market_data.market_symbol)

    def test_market_data_white_space_str_input(self):
        try: 
            self.test_market_data.market_symbol = "       "
        except ValueError as e:
            self.assertEqual(str(e), "Market symbol must not be blank")

    def test_market_data_empty_str_input(self):
        try: 
            self.test_market_data.market_symbol = ""
        except ValueError as e:
            self.assertEqual(str(e), "Market symbol must not be empty")

    def test_market_data_list_input(self):
        try:
            self.test_market_data.market_symbol = [[0, 0, 0, 0], [0, 0, 0, 0]]
        except ValueError as e:
            self.assertEqual(str(e), "Market symbol must be a string object")
    
    def test_market_data_dict_input(self):
        try:
            self.test_market_data.market_symbol = {"zero": 0, "one": 1}
        except ValueError as e:
            self.assertEqual(str(e), "Market symbol must be a string object")
    
    def test_market_data_int_input(self):
        try:
            self.test_market_data.market_symbol = 0
        except ValueError as e:
            self.assertEqual(str(e), "Market symbol must be a string object")

    def test_market_data_float_input(self):
        try:
            self.test_market_data.market_symbol = 0.0
        except ValueError as e:
            self.assertEqual(str(e), "Market symbol must be a string object")

    def test_market_data_none_input(self):
        try:
            self.test_market_data.market_symbol = None
        except ValueError as e:
            self.assertEqual(str(e), "Market symbol must be a string object")


    # Test market_returns attributes
    def test_market_returns_float_input(self):
        self.test_market_data.market_returns = 0.15
        self.assertEqual(0.15, self.test_market_data.market_returns)

    def test_market_returns_int_input(self):
        self.test_market_data.market_returns = 0
        self.assertEqual(0, self.test_market_data.market_returns)

    def test_market_returns_list_input(self):
        try:
            self.test_market_data.market_returns = [[0, 0, 0, 0], [0, 0, 0, 0]]
        except ValueError as e:
            self.assertEqual(str(e), "Market returns must be a numeric data type")
    
    def test_market_returns_dict_input(self):
        try:
            self.test_market_data.market_returns = {"zero": 0, "one": 1}
        except ValueError as e:
            self.assertEqual(str(e), "Market returns must be a numeric data type")

    def test_market_returns_str_input(self):
        try:
            self.test_market_data.market_returns = "0.15"
        except ValueError as e:
            self.assertEqual(str(e), "Market returns must be a numeric data type")

    def test_market_returns_none_input(self):
        try:
            self.test_market_data.market_returns = None
        except ValueError as e:
            self.assertEqual(str(e), "Market returns must be a numeric data type")

   # Test daily_market_returns attributes
    def test_market_returns_float_input(self):
        self.test_market_data.daily_market_returns = 0.15
        self.assertEqual(0.15, self.test_market_data.daily_market_returns)

    def test_market_returns_int_input(self):
        self.test_market_data.daily_market_returns = 0
        self.assertEqual(0, self.test_market_data.daily_market_returns)

    def test_market_returns_list_input(self):
        try:
            self.test_market_data.daily_market_returns = [[0, 0, 0, 0], [0, 0, 0, 0]]
        except ValueError as e:
            self.assertEqual(str(e), "Daily market returns must be a numeric data type")
    
    def test_market_returns_dict_input(self):
        try:
            self.test_market_data.daily_market_returns = {"zero": 0, "one": 1}
        except ValueError as e:
            self.assertEqual(str(e), "Daily market returns must be a numeric data type")

    def test_market_returns_str_input(self):
        try:
            self.test_market_data.daily_market_returns = "0.15"
        except ValueError as e:
            self.assertEqual(str(e), "Daily market returns must be a numeric data type")

    def test_market_returns_none_input(self):
        try:
            self.test_market_data.daily_market_returns = None
        except ValueError as e:
            self.assertEqual(str(e), "Daily market returns must be a numeric data type")

if __name__ == "__main__":
    unittest.main()
