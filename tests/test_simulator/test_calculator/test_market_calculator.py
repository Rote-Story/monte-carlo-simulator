

import unittest
import numpy as np
import pandas as pd

from monte_carlo_simulator.service.calculator.market_calculator import *


class TestMarketCalculator(unittest.TestCase):

    # Read in stored data for testing
    test_market_data = pd.read_csv('.\\tests\\test_simulator\\testing_data\\market_data.csv', header=[0, 1], index_col=[0])
    test_asset_data = pd.read_csv('.\\tests\\test_simulator\\testing_data\\asset_data.csv', header=[0, 1], index_col=[0])
    test_rfr_data = pd.read_csv('.\\tests\\test_simulator\\testing_data\\rfr_data.csv', header=[0, 1], index_col=[0])

    # Change index type from string to datetime 
    test_market_data.index = pd.to_datetime(test_market_data.index)
    test_asset_data.index = pd.to_datetime(test_asset_data.index)
    test_rfr_data.index = pd.to_datetime(test_rfr_data.index)

    # -----------------------------------------------------------------------------
    # calc_market_returns tests
    # -----------------------------------------------------------------------------

    def test_calc_market_returns_valid_input(self):
        result = calc_market_returns(self.test_market_data)

        # Calculate expected result from test data
        expected_result = self.test_market_data['Close'].iloc[:, 0] \
            .resample('YE') \
            .last() 
        expected_result.iloc[0] = self.test_market_data['Close'].iloc[0].iloc[0] 
        expected_result = expected_result.pct_change().mean()

        self.assertAlmostEqual(result, expected_result)

    def test_calc_market_returns_invalid_input_str(self):
        with self.assertRaises(TypeError):
            calc_market_returns('DataFrame')

    def test_calc_market_returns_invalid_input_series(self):
        with self.assertRaises(TypeError):
            calc_market_returns(pd.Series([1, 2, 3]))
    
    def test_calc_market_returns_invalid_input_none(self):
        with self.assertRaises(TypeError):
            calc_market_returns(None)
    
    def test_calc_market_returns_invalid_input_returns_none(self):
        with self.assertRaises(TypeError):
            result = calc_market_returns('DataFrame')
            self.assertIsNone(result)
    
    def test_calc_market_returns_invalid_input_type_error_message(self):
        with self.assertRaises(TypeError) as e:
            calc_market_returns('DataFrame')
            self.assertRegex(str(e), r'"market_data" parameter must be a DataFrame, not \.*')
    
    def test_calc_market_returns_return_type(self):
        result = calc_market_returns(self.test_market_data)
        self.assertIsInstance(result, float)

    # -----------------------------------------------------------------------------
    # calc_daily_market_returns tests
    # -----------------------------------------------------------------------------

    def test_calc_daily_market_returns_valid_input(self):
        result = calc_daily_market_returns(self.test_market_data)

        # Calculate expected result from test data
        expected_result = self.test_market_data['Close'].iloc[:, 0] \
            .pct_change() \
            .mean() 

        self.assertAlmostEqual(result, expected_result)

    def test_calc_daily_market_returns_invalid_input_str(self):
        with self.assertRaises(TypeError):
            calc_daily_market_returns('DataFrame')

    def test_calc_daily_market_returns_invalid_input_series(self):
        with self.assertRaises(TypeError):
            calc_daily_market_returns(pd.Series([1, 2, 3]))
    
    def test_calc_daily_market_returns_invalid_input_none(self):
        with self.assertRaises(TypeError):
            calc_daily_market_returns(None)
    
    def test_calc_daily_market_returns_invalid_input_returns_none(self):
        with self.assertRaises(TypeError):
            result = calc_daily_market_returns('DataFrame')
            self.assertIsNone(result)

    def test_calc_daily_market_returns_invalid_input_type_error_message(self):
        with self.assertRaises(TypeError) as e:
            calc_daily_market_returns('DataFrame')
            self.assertRegex(str(e), r'"market_data" parameter must be a DataFrame, not \.*')
    
    def test_calc_daily_market_returns_return_type(self):
        result = calc_daily_market_returns(self.test_market_data)
        self.assertIsInstance(result, float)

    # -----------------------------------------------------------------------------
    # calc_rfr tests
    # -----------------------------------------------------------------------------

    def test_calc_rfr_valid_input(self):
        result = calc_rfr(self.test_rfr_data)

        # Calculate expected result using test data
        expected_result = self.test_rfr_data['Close'].iloc[:, 0].mean()

        self.assertAlmostEqual(result, expected_result)
    
    def test_calc_rfr_invalid_input_str(self):
        with self.assertRaises(TypeError):
            calc_rfr('DataFrame')

    def test_calc_rfr_invalid_input_series(self):
        with self.assertRaises(TypeError):
            calc_rfr(pd.Series([1, 2, 3]))
    
    def test_calc_rfr_invalid_input_none(self):
        with self.assertRaises(TypeError):
            calc_rfr(None)
    
    def test_calc_rfr_invalid_input_returns_none(self):
        with self.assertRaises(TypeError):
            result = calc_rfr('DataFrame')
            self.assertIsNone(result)

    def test_calc_rfr_invalid_input_type_error_message(self):
        with self.assertRaises(TypeError) as e:
            calc_rfr('DataFrame')
            self.assertRegex(str(e), r'"rfr_data" parameter must be a DataFrame, not \.*')
        
    def test_calc_rfr_return_type(self):
        result = calc_rfr(self.test_rfr_data)
        self.assertIsInstance(result, float)


    # -----------------------------------------------------------------------------
    # calc_daily_rfr tests
    # -----------------------------------------------------------------------------

    def test_calc_daily_rfr_valid_input(self):
        result = calc_daily_rfr(self.test_rfr_data)

        # Calculate expected result using test data
        expected_result = self.test_rfr_data['Close'].iloc[:, 0] \
            .apply(lambda x: (1 + x / 100) ** (1 / 365) - 1) \
            .mean()

        self.assertAlmostEqual(result, expected_result)
    
    def test_calc_daily_rfr_invalid_input_str(self):
        with self.assertRaises(TypeError):
            calc_daily_rfr('DataFrame')

    def test_calc_daily_rfr_invalid_input_series(self):
        with self.assertRaises(TypeError):
            calc_daily_rfr(pd.Series([1, 2, 3]))
    
    def test_calc_daily_rfr_invalid_input_none(self):
        with self.assertRaises(TypeError):
            calc_daily_rfr(None)
    
    def test_calc_daily_rfr_invalid_input_returns_none(self):
        with self.assertRaises(TypeError):
            result = calc_daily_rfr('DataFrame')
            self.assertIsNone(result)

    def test_calc_daily_rfr_invalid_input_type_error_message(self):
        with self.assertRaises(TypeError) as e:
            calc_rfr('DataFrame')
            self.assertRegex(str(e), r'"rfr_data" parameter must be a DataFrame, not \.*')
     
    def test_calc_daily_rfr_return_type(self):
        result = calc_daily_rfr(self.test_asset_data)
        self.assertIsInstance(result, float)


    # -----------------------------------------------------------------------------
    # historic_volatility tests
    # -----------------------------------------------------------------------------
    
    def test_historic_volatility_valid_input(self):
        result = calc_volatility(self.test_asset_data, 60)

        # Calculate expected result using test data
        expected_result = (self.test_asset_data['Close'].iloc[:, 0].pct_change() + 1) \
            .apply(lambda x: np.log(x)) \
            .rolling(window=60) \
            .std().iloc[-1] * np.sqrt(60)

        self.assertAlmostEqual(result, expected_result)
    
    def test_historic_volatility_float_window_input(self):
        result = calc_volatility(self.test_asset_data, 30.5)

        # Calculate expected result using test data (window should be converted to 30)
        expected_result = (self.test_asset_data['Close'].iloc[:, 0].pct_change() + 1) \
            .apply(lambda x: np.log(x)) \
            .rolling(window=30) \
            .std().iloc[-1] * np.sqrt(30)

        self.assertAlmostEqual(result, expected_result)
    
    def test_historic_volatility_invalid_data_input_str(self):
        with self.assertRaises(TypeError):
            calc_volatility('DataFrame', 2)

    def test_historic_volatility_invalid_data_input_series(self):
        with self.assertRaises(TypeError):
            calc_volatility(pd.Series([1, 2, 3]), 40)
    
    def test_historic_volatility_invalid_data_input_none(self):
        with self.assertRaises(TypeError) as e:
            calc_volatility(None, 0)
    
    def test_historic_volatility_invalid_data_input_returns_none(self):
        with self.assertRaises(TypeError):
            result = calc_volatility('DataFrame')
            self.assertIsNone(result)

    def test_historic_volatility_invalid_data_input_type_error_message(self):
        with self.assertRaises(TypeError) as e:
            calc_volatility('DataFrame')
            self.assertRegex(str(e), r'"asset_data" parameter must be a DataFrame, not \.*')

    def test_historic_volatility_invalid_window_input_str(self):
        with self.assertRaises(TypeError):
            calc_volatility(self.test_asset_data, '30')
    
    def test_historic_volatility_invalid_window_input_none(self):
        with self.assertRaises(TypeError):
            calc_volatility(self.test_asset_data, None)

    def test_historic_volatility_invalid_window_input_returns_none(self):
        with self.assertRaises(TypeError):
            result = calc_volatility(self.test_asset_data, None)
            self.assertIsNone(result)

    def test_historic_volatility_invalid_window_input_type_error_message(self):
        with self.assertRaises(TypeError) as e:
            calc_volatility(self.test_asset_data, '30')
            self.assertRegex(str(e), r'"window" parameter must be an integer, not \.*') 
    
    def test_historic_volatility_invalid_window_input_type_error_message(self):
        with self.assertRaises(ValueError) as e:
            calc_volatility(self.test_asset_data, -30)
            self.assertRegex(str(e), r'"window" parameter must be a positive integer, not \.*')

    def test_historic_volatility_return_type(self):
        result = calc_daily_market_returns(self.test_asset_data)
        self.assertIsInstance(result, np.float64)


if __name__ == '__main__':
    unittest.main()
