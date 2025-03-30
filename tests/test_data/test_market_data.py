
import unittest
from pandas import DataFrame
from pandas.testing import assert_frame_equal
import numpy as np

from monte_carlo_simulator.data.market_data import MarketData

class TestMarketData(unittest.TestCase):

    test_market_data = MarketData()
    test_dataframe1 = DataFrame(np.linspace(0.0, 3.0, num=5))
    test_dataframe2 = DataFrame(np.zeros((4, 4)))

    # test market_data attributes
    def test_market_data_dataframe_input(self):
        self.test_market_data.market_data = self.test_dataframe1
        assert_frame_equal(self.test_dataframe1, self.test_market_data.market_data)

    def test_market_data_dataframe_input(self):
        self.test_market_data.market_data = self.test_dataframe2
        assert_frame_equal(self.test_dataframe2, self.test_market_data.market_data)

    def test_market_data_list_input(self):
        try:
            self.test_market_data.market_data = [[0, 0, 0, 0], [0, 0, 0, 0]]
        except ValueError as e:
            self.assertEqual(str(e), "Market data must be a pandas DataFrame object")
    
    def test_market_data_dict_input(self):
        try:
            self.test_market_data.market_data = {"zero": 0, "one": 1}
        except ValueError as e:
            self.assertEqual(str(e), "Market data must be a pandas DataFrame object")
    
    def test_market_data_int_input(self):
        try:
            self.test_market_data.market_data = 0
        except ValueError as e:
            self.assertEqual(str(e), "Market data must be a pandas DataFrame object")

    def test_market_data_float_input(self):
        try:
            self.test_market_data.market_data = 0.0
        except ValueError as e:
            self.assertEqual(str(e), "Market data must be a pandas DataFrame object")

    def test_market_data_none_input(self):
        try:
            self.test_market_data.market_data = None
        except ValueError as e:
            self.assertEqual(str(e), "Market data must be a pandas DataFrame object")

    # test rfr_data attributes
    def test_rfr_data_dataframe_input(self):
        self.test_market_data.rfr_data = self.test_dataframe1
        assert_frame_equal(self.test_dataframe1, self.test_market_data.rfr_data)

    def test_rfr_data_dataframe_input(self):
        self.test_market_data.rfr_data = self.test_dataframe2
        assert_frame_equal(self.test_dataframe2, self.test_market_data.rfr_data)

    def test_rfr_data_list_input(self):
        try:
            self.test_market_data.rfr_data = [[0, 0, 0, 0], [0, 0, 0, 0]]
        except ValueError as e:
            self.assertEqual(str(e), "Risk free rate data must be a pandas DataFrame object")
    
    def test_rfr_data_dict_input(self):
        try:
            self.test_market_data.rfr_data = {"zero": 0, "one": 1}
        except ValueError as e:
            self.assertEqual(str(e), "Risk free rate data must be a pandas DataFrame object")
    
    def test_rfr_data_int_input(self):
        try:
            self.test_market_data.rfr_data = 0
        except ValueError as e:
            self.assertEqual(str(e), "Risk free rate data must be a pandas DataFrame object")

    def test_rfr_data_float_input(self):
        try:
            self.test_market_data.rfr_data = 0.0
        except ValueError as e:
            self.assertEqual(str(e), "Risk free rate data must be a pandas DataFrame object")

    def test_rfr_data_none_input(self):
        try:
            self.test_market_data.rfr_data = None
        except ValueError as e:
            self.assertEqual(str(e), "Risk free rate data must be a pandas DataFrame object")

    # test market_returns attributes
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

    # test risk_free_rate attributes
    def test_risk_free_rate_dataframe_input(self):
        self.test_market_data.risk_free_rate = 0.15
        self.assertEqual(0.15, self.test_market_data.risk_free_rate)
    
    def test_risk_free_rate_dataframe_input(self):
        self.test_market_data.risk_free_rate = 0
        self.assertEqual(0, self.test_market_data.risk_free_rate)

    def test_risk_free_rate_list_input(self):
        try:
            self.test_market_data.risk_free_rate = [[0, 0, 0, 0], [0, 0, 0, 0]]
        except ValueError as e:
            self.assertEqual(str(e), "Risk-free rate must be a numeric data type")
    
    def test_risk_free_rate_dict_input(self):
        try:
            self.test_market_data.risk_free_rate = {"zero": 0, "one": 1}
        except ValueError as e:
            self.assertEqual(str(e), "Risk-free rate must be a numeric data type")

    def test_risk_free_rate_str_input(self):
        try:
            self.test_market_data.risk_free_rate = "0.15"
        except ValueError as e:
            self.assertEqual(str(e), "Risk-free rate must be a numeric data type")

    def test_risk_free_rate_none_input(self):
        try:
            self.test_market_data.risk_free_rate = None
        except ValueError as e:
            self.assertEqual(str(e), "Risk-free rate must be a numeric data type")


