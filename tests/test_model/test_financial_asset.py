
import unittest
from unittest.mock import Mock
import pandas as pd
from pandas.testing import assert_frame_equal
from yfinance import Ticker

from monte_carlo_simulator.model.financial_asset import FinancialAsset

class TestFinancialAsset(unittest.TestCase):
    

    def setUp(self):
        self.financial_asset = FinancialAsset()
        self.mock_ticker = Mock(spec=Ticker)

    # asset_ticker tests
    def test_asset_ticker_ticker_type(self):
        self.financial_asset.asset_ticker = self.mock_ticker
        self.assertIsInstance(self.financial_asset.asset_ticker, Ticker)

    def test_asset_ticker_ticker_input(self):
        self.financial_asset.asset_ticker = self.mock_ticker
        self.assertIs(self.financial_asset.asset_ticker, self.mock_ticker)

    def test_asset_ticker_str_input(self):
        try: 
            self.financial_asset.asset_ticker = '0.15'
        except TypeError as e:
            self.assertEqual(str(e), 'Asset ticker must be a yfinance.Ticker object')
    
    def test_asset_ticker_bool_input(self):
        try: 
            self.financial_asset.asset_ticker = True
        except TypeError as e:
            self.assertEqual(str(e), 'Asset ticker must be a yfinance.Ticker object')
            
    def test_asset_ticker_int_input(self):
        try: 
            self.financial_asset.asset_ticker = 100
        except TypeError as e:
            self.assertEqual(str(e), 'Asset ticker must be a yfinance.Ticker object')

    def test_asset_ticker_negative_int_input(self):
        try: 
            self.financial_asset.asset_ticker = -1
        except TypeError as e:
            self.assertEqual(str(e), 'Asset ticker must be a yfinance.Ticker object')
    
    def test_asset_ticker_float_input(self):
        try: 
            self.financial_asset.asset_ticker = 0.15
        except TypeError as e:
            self.assertEqual(str(e), 'Asset ticker must be a yfinance.Ticker object')

    def test_asset_ticker_none_input(self):
        try: 
            self.financial_asset.asset_ticker = None
        except TypeError as e:
            self.assertEqual(str(e), 'Asset ticker must be a yfinance.Ticker object')

    # Time period tests 
    def test_period_valid_input(self):
        self.financial_asset.period = '6mo'
        self.assertEqual('6mo', self.financial_asset.period)

    def test_period_str_input_not_in_time_periods(self):
        try:
            self.financial_asset.period = 'Five years'
        except ValueError as e:
            self.assertRegex(str(e), r'Time period must be in the list of valid time periods, \.*')

    def test_period_ticker_input(self):
        try: 
            self.financial_asset.period = self.mock_ticker
        except TypeError as e:
            self.assertRegex(str(e), r'Time period must be a string in the list of valid time periods, \.*')

    def test_period_bool_input(self):
        try: 
            self.financial_asset.period = True
        except TypeError as e:
            self.assertRegex(str(e),  r'Time period must be a string in the list of valid time periods, \.*')
            
    def test_period_int_input(self):
        try: 
            self.financial_asset.period = 100
        except TypeError as e:
            self.assertRegex(str(e),  r'Time period must be a string in the list of valid time periods, \.*')

    def test_period_negative_int_input(self):
        try: 
            self.financial_asset.period = -1
        except TypeError as e:
            self.assertRegex(str(e),  r'Time period must be a string in the list of valid time periods, \.*')
    
    def test_period_float_input(self):
        try: 
            self.financial_asset.period = 0.15
        except TypeError as e:
            self.assertRegex(str(e),  r'Time period must be a string in the list of valid time periods, \.*')

    def test_period_none_input(self):
        try: 
            self.financial_asset.period = None
        except TypeError as e:
            self.assertRegex(str(e),  r'Time period must be a string in the list of valid time periods, \.*')

    # asset_symbol tests
    def test_asset_symbol_str_input(self):
        self.financial_asset.asset_symbol = 'IBM'
        self.assertEqual('IBM', self.financial_asset.asset_symbol)

    def test_asset_symbol_ticker_input(self):
        try:
            self.financial_asset.asset_symbol = self.mock_ticker
        except TypeError as e:
            self.assertEqual(str(e), 'Asset symbol must be a string object')
    
    def test_asset_symbol_bool_input(self):
        try: 
            self.financial_asset.asset_symbol = True
        except TypeError as e:
            self.assertEqual(str(e), 'Asset symbol must be a string object')
            
    def test_asset_symbol_int_input(self):
        try: 
            self.financial_asset.asset_symbol = 100
        except TypeError as e:
            self.assertEqual(str(e), 'Asset symbol must be a string object')

    def test_asset_symbol_negative_int_input(self):
        try: 
            self.financial_asset.asset_symbol = -1
        except TypeError as e:
            self.assertEqual(str(e), 'Asset symbol must be a string object')
    
    def test_asset_symbol_float_input(self):
        try: 
            self.financial_asset.asset_symbol = 0.15
        except TypeError as e:
            self.assertEqual(str(e), 'Asset symbol must be a string object')

    def test_asset_symbol_none_input(self):
        try: 
            self.financial_asset.asset_symbol = None
        except TypeError as e:
            self.assertEqual(str(e), 'Asset symbol must be a string object')

    # asset_data tests
    def test_asset_data_dataframe_input(self):
        self.financial_asset.asset_data = pd.DataFrame([0, 1, 2])
        assert_frame_equal(pd.DataFrame([0, 1, 2]), self.financial_asset.asset_data)
    
    def test_asset_data_str_input(self):
        try:
            self.financial_asset.asset_data = 'IBM'
        except TypeError as e:
            self.assertEqual(str(e), 'Asset data must be a pandas.DataFrame object')
    
    def test_asset_data_ticker_input(self):
        try:
            self.financial_asset.asset_data = self.mock_ticker
        except TypeError as e:
            self.assertEqual(str(e), 'Asset data must be a pandas.DataFrame object')
    
    def test_asset_data_bool_input(self):
        try: 
            self.financial_asset.asset_data = True
        except TypeError as e:
            self.assertEqual(str(e), 'Asset data must be a pandas.DataFrame object')
            
    def test_asset_data_int_input(self):
        try: 
            self.financial_asset.asset_data = 100
        except TypeError as e:
            self.assertEqual(str(e), 'Asset data must be a pandas.DataFrame object')

    def test_asset_data_negative_int_input(self):
        try: 
            self.financial_asset.asset_data = -1
        except TypeError as e:
            self.assertEqual(str(e), 'Asset data must be a pandas.DataFrame object')
    
    def test_asset_data_float_input(self):
        try: 
            self.financial_asset.asset_data = 0.15
        except TypeError as e:
            self.assertEqual(str(e), 'Asset data must be a pandas.DataFrame object')

    def test_asset_data_none_input(self):
        try: 
            self.financial_asset.asset_data = None
        except TypeError as e:
            self.assertEqual(str(e), 'Asset data must be a pandas.DataFrame object')

    # his_vol tests
    def test_his_vol_float_input(self):
        self.financial_asset.his_vol = 0.15
        self.assertEqual(self.financial_asset.his_vol, 0.15)

    def test_his_vol_int_input(self):
        self.financial_asset.his_vol = 0
        self.assertEqual(self.financial_asset.his_vol, 0)

    def test_his_vol_str_input(self):
        try: 
            self.financial_asset.his_vol = '0.15'
        except TypeError as e:
            self.assertEqual(str(e), 'Historic volatility must be a positive numeric type')
    
    def test_his_vol_bool_input(self):
        try: 
            self.financial_asset.his_vol = True
        except TypeError as e:
            self.assertEqual(str(e), 'Historic volatility must be a positive numeric type')
            
    def test_his_vol_negative_int_input(self):
        try: 
            self.financial_asset.his_vol = -1
        except ValueError as e:
            self.assertEqual(str(e), 'Historic volatility must be positive')

    def test_his_vol_none_input(self):
        try: 
            self.financial_asset.his_vol = None
        except TypeError as e:
            self.assertEqual(str(e), 'Historic volatility must be a positive numeric type')

    # beta tests
    def test_beta_float_input(self):
        self.financial_asset.beta = 0.15
        self.assertEqual(self.financial_asset.beta, 0.15)

    def test_beta_int_input(self):
        self.financial_asset.beta = 0
        self.assertEqual(self.financial_asset.beta, 0)

    def test_beta_str_input(self):
        try: 
            self.financial_asset.beta = '0.15'
        except TypeError as e:
            self.assertEqual(str(e), 'Beta must be a positive numeric type')

    def test_beta_bool_input(self):
        try: 
            self.financial_asset.beta = False
        except TypeError as e:
            self.assertEqual(str(e), 'Beta must be a positive numeric type')
            
    def test_beta_negative_input(self):
        try: 
            self.financial_asset.beta = -1
        except ValueError as e:
            self.assertEqual(str(e), 'Beta must be positive')

    def test_beta_none_input(self):
        try: 
            self.financial_asset.beta = None
        except TypeError as e:
            self.assertEqual(str(e), 'Beta must be a positive numeric type')

    # expected_returns tests
    def test_expected_returns_float_input(self):
        self.financial_asset.expected_returns = 0.15
        self.assertEqual(self.financial_asset.expected_returns, 0.15)

    def test_expected_returns_int_input(self):
        self.financial_asset.expected_returns = 0
        self.assertEqual(self.financial_asset.expected_returns, 0)
    
    def test_expected_returns_str_input(self):
        try: 
            self.financial_asset.expected_returns = '0.15'
        except TypeError as e:
            self.assertEqual(str(e), 'Expected returns must be a numeric type')

    def test_expected_returns_bool_input(self):
        try: 
            self.financial_asset.expected_returns = True
        except TypeError as e:
            self.assertEqual(str(e), 'Expected returns must be a numeric type')

    def test_expected_returns_negative_int_input(self):
        self.financial_asset.expected_returns = -50
        self.assertEqual(self.financial_asset.expected_returns, -50)

    def test_expected_returns_none_input(self):
        try: 
            self.financial_asset.expected_returns = None
        except TypeError as e:
            self.assertEqual(str(e), 'Expected returns must be a numeric type')

    # Expected returns flag tests

    def test_exp_ret_flag__str_input(self):
        self.financial_asset.exp_ret_flag = 'Capital Asset Pricing Model'
        self.assertEqual('Capital Asset Pricing Model', self.financial_asset.exp_ret_flag)
    
    def test_exp_ret_flag_ticker_input(self):
        try:
            self.financial_asset.exp_ret_flag = self.mock_ticker
        except TypeError as e:
            self.assertEqual(str(e), 'Expected returns flag must be a string type')

    def test_exp_ret_flag_float_input(self):
        try:
            self.financial_asset.exp_ret_flag = 0.15
        except TypeError as e:
            self.assertEqual(str(e), 'Expected returns flag must be a string type')

    def test_exp_ret_flag_int_input(self):
        try:
            self.financial_asset.exp_ret_flag = 0
        except TypeError as e:
            self.assertEqual(str(e), 'Expected returns flag must be a string type')

    def test_exp_ret_flag_bool_input(self):
        try: 
            self.financial_asset.exp_ret_flag = True
        except TypeError as e:
            self.assertEqual(str(e), 'Expected returns flag must be a string type')

    def test_exp_ret_flag_negative_int_input(self):
        try:
            self.financial_asset.exp_ret_flag = -0.15
        except TypeError as e:
            self.assertEqual(str(e), 'Expected returns flag must be a string type')

    def test_exp_ret_flag_none_input(self):
        try: 
            self.financial_asset.exp_ret_flag = None
        except TypeError as e:
            self.assertEqual(str(e), 'Expected returns flag must be a string type')


if __name__ == '__main__':
    unittest.main()