import unittest.mock
from yfinance import Ticker
import unittest

from monte_carlo_simulator.data.asset_data import AssetData

class TestAssetData(unittest.TestCase):
    
    test_asset_data = AssetData()
    mock_ticker = unittest.mock.Mock(spec=Ticker)

    # asset_info tests
    def test_asset_info_ticker_type(self):
        self.test_asset_data.asset_info = self.mock_ticker
        self.assertIsInstance(self.test_asset_data.asset_info, Ticker)

    def test_asset_info_ticker_input(self):
        self.test_asset_data.asset_info = self.mock_ticker
        self.assertIs(self.test_asset_data.asset_info, self.mock_ticker)

    def test_asset_info_str_input(self):
        try: 
            self.test_asset_data.asset_info = "0.15"
        except ValueError as e:
            self.assertEqual(str(e), "Stock info must be a yfinance.Ticker object")
    
    def test_asset_info_bool_input(self):
        try: 
            self.test_asset_data.asset_info = True
        except ValueError as e:
            self.assertEqual(str(e), "Stock info must be a yfinance.Ticker object")
            
    def test_asset_info_int_input(self):
        try: 
            self.test_asset_data.asset_info = 100
        except ValueError as e:
            self.assertEqual(str(e), "Stock info must be a yfinance.Ticker object")

    def test_asset_info_negative_int_input(self):
        try: 
            self.test_asset_data.asset_info = -1
        except ValueError as e:
            self.assertEqual(str(e), "Stock info must be a yfinance.Ticker object")
    
    def test_asset_info_float_input(self):
        try: 
            self.test_asset_data.asset_info = 0.15
        except ValueError as e:
            self.assertEqual(str(e), "Stock info must be a yfinance.Ticker object")

    def test_asset_info_none_input(self):
        try: 
            self.test_asset_data.asset_info = None
        except ValueError as e:
            self.assertEqual(str(e), "Stock info must be a yfinance.Ticker object")


    # his_vol tests
    def test_his_vol_float_input(self):
        self.test_asset_data.his_vol = 0.15
        self.assertEqual(self.test_asset_data.his_vol, 0.15)

    def test_his_vol_int_input(self):
        self.test_asset_data.his_vol = 0
        self.assertEqual(self.test_asset_data.his_vol, 0)

    def test_his_vol_str_input(self):
        try: 
            self.test_asset_data.his_vol = "0.15"
        except ValueError as e:
            self.assertEqual(str(e), "Historic volatility must be a positive numeric type")
    
    def test_his_vol_bool_input(self):
        try: 
            self.test_asset_data.his_vol = True
        except ValueError as e:
            self.assertEqual(str(e), "Historic volatility must be a positive numeric type")
            
    def test_his_vol_negative_int_input(self):
        try: 
            self.test_asset_data.his_vol = -1
        except ValueError as e:
            self.assertEqual(str(e), "Historic volatility must be a positive numeric type")

    def test_his_vol_none_input(self):
        try: 
            self.test_asset_data.his_vol = None
        except ValueError as e:
            self.assertEqual(str(e), "Historic volatility must be a positive numeric type")

    # beta tests
    def test_beta_float_input(self):
        self.test_asset_data.beta = 0.15
        self.assertEqual(self.test_asset_data.beta, 0.15)

    def test_beta_int_input(self):
        self.test_asset_data.beta = 0
        self.assertEqual(self.test_asset_data.beta, 0)

    def test_beta_str_input(self):
        try: 
            self.test_asset_data.beta = "0.15"
        except ValueError as e:
            self.assertEqual(str(e), "Beta must be a positive numeric type")

    def test_beta_bool_input(self):
        try: 
            self.test_asset_data.beta = False
        except ValueError as e:
            self.assertEqual(str(e), "Beta must be a positive numeric type")
            
    def test_beta_negative_input(self):
        try: 
            self.test_asset_data.beta = -1
        except ValueError as e:
            self.assertEqual(str(e), "Beta must be a positive numeric type")

    def test_beta_none_input(self):
        try: 
            self.test_asset_data.beta = None
        except ValueError as e:
            self.assertEqual(str(e), "Beta must be a positive numeric type")

    # expected_returns tests
    def test_expected_returns_float_input(self):
        self.test_asset_data.expected_returns = 0.15
        self.assertEqual(self.test_asset_data.expected_returns, 0.15)

    def test_expected_returns_int_input(self):
        self.test_asset_data.expected_returns = 0
        self.assertEqual(self.test_asset_data.expected_returns, 0)
    
    def test_expected_returns_str_input(self):
        try: 
            self.test_asset_data.expected_returns = "0.15"
        except ValueError as e:
            self.assertEqual(str(e), "Expected returns must be a numeric type")

    def test_expected_returns_bool_input(self):
        try: 
            self.test_asset_data.expected_returns = True
        except ValueError as e:
            self.assertEqual(str(e), "Expected returns must be a numeric type")

    def test_expected_returns_negative_int_input(self):
        self.test_asset_data.expected_returns = -50
        self.assertEqual(self.test_asset_data.expected_returns, -50)

    def test_expected_returns_none_input(self):
        try: 
            self.test_asset_data.expected_returns = None
        except ValueError as e:
            self.assertEqual(str(e), "Expected returns must be a numeric type")

if __name__ == "__main__":
    unittest.main()