

import unittest
from unittest.mock import patch, Mock
import yfinance as yf
import requests

from monte_carlo_simulator.data_fetcher.market_data_fetcher import MarketDataFetcher


class TestValidateTicker(unittest.TestCase):

    def setUp(self):
        self.mock_ticker_instance = Mock() # Mock yfinance.Ticker object
        session = None # Session not needed for testing
        self.test_market_data_fetcher = MarketDataFetcher(session) 
        self.ticker_symbol = "AAPL"
        
        self.patcher = patch("yfinance.Ticker", return_value=self.mock_ticker_instance)
        self.patcher.start()

    def test_validate_ticker_valid_input(self):
        self.mock_ticker_instance.get_info.return_value = {
            "symbol": "AAPL",
            "shortName" : "Apple Inc.",
            "previousClose": "206.11"
        }

        validation_check = self.test_market_data_fetcher.validate_ticker(
            self.ticker_symbol)
        self.assertTrue(validation_check) # True value indicates successful call
    
    def test_validate_ticker_function_called_once(self):
        self.mock_ticker_instance.get_info.return_value = { 
            "symbol": "AAPL",
            "shortName" : "Apple Inc.",
            "previousClose": "206.11"
        }

        self.test_market_data_fetcher.validate_ticker(self.ticker_symbol)
        self.mock_ticker_instance.get_info.assert_called_once()
        
    def test_validate_ticker_missing_ticker_error_message(self):
        self.mock_ticker_instance.get_info.side_effect = yf.exceptions.YFTickerMissingError
        
        result = self.test_market_data_fetcher.validate_ticker(self.ticker_symbol)
        self.assertRegex(result, r"An error occurred: .*")

    def test_validate_ticker_generic_http_error_message(self):
        self.mock_ticker_instance.get_info.side_effect = requests.exceptions.HTTPError("HTTPError")
        
        result = self.test_market_data_fetcher.validate_ticker(self.ticker_symbol)
        self.assertEqual(result, "An HTTP error occurred: HTTPError")

    def test_validate_ticker_request_exception_message(self):
        self.mock_ticker_instance.get_info.side_effect = requests.exceptions.RequestException("RequestException")
        
        result = self.test_market_data_fetcher.validate_ticker(self.ticker_symbol)
        self.assertEqual(result, "A request exception ocurred: RequestException")

    def test_validate_ticker_general_exception_message(self):
        self.mock_ticker_instance.get_info.side_effect = Exception("Exception")
        
        result = self.test_market_data_fetcher.validate_ticker(self.ticker_symbol)
        self.assertEqual(result,  "An error occurred: Exception")

    def tearDown(self):
        patch.stopall() # Clean up post-test patches
    

if __name__ == "__main__":
    unittest.main()