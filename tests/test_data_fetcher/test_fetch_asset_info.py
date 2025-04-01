
import unittest
from unittest.mock import Mock, patch
import requests
import yfinance as yf

from monte_carlo_simulator.data_fetcher.market_data_fetcher import MarketDataFetcher


class TestFetchAssetInfo(unittest.TestCase):

    def setUp(self):
        self.mock_ticker_instance = Mock(spec=yf.Ticker) # Mock ticker object
        self.ticker_symbol = "AAPL"
        session = None # Session not needed for testing
        self.test_market_data_fetcher = MarketDataFetcher(session)
        patches = patch("yfinance.Ticker", return_value=self.mock_ticker_instance)
        patches.start()

    def test_fetch_asset_info_valid_input(self):
        self.mock_ticker_instance.get_info.return_value = {
            "symbol": "AAPL",
            "shortName" : "Apple Inc.",
            "previousClose": "206.11"
        }
        
        result = self.test_market_data_fetcher.fetch_asset_info(self.ticker_symbol)
        self.assertEqual(result, self.mock_ticker_instance)

    def test_fetch_asset_info_return_symbol(self):
        self.mock_ticker_instance.get_info.return_value = {
            "symbol": "AAPL",
            "shortName" : "Apple Inc.",
            "previousClose": "206.11"
        }
        
        result = self.test_market_data_fetcher.fetch_asset_info(self.ticker_symbol)
        self.assertEqual(result.get_info()["symbol"], "AAPL")
    
    def test_fetch_asset_info_return_type(self):
        self.mock_ticker_instance.get_info.return_value = {
            "symbol": "AAPL",
            "shortName" : "Apple Inc.",
            "previousClose": "206.11"
        }
        
        result = self.test_market_data_fetcher.fetch_asset_info(self.ticker_symbol)
        self.assertIsInstance(result.get_info(), dict)

    def test_fetch_asset_info_ticker_get_info_called_once(self):
        self.test_market_data_fetcher.fetch_asset_info(self.ticker_symbol)
        self.mock_ticker_instance.get_info.assert_called_once()
        
    def test_fetch_asset_info_missing_ticker_error_message(self):
        self.mock_ticker_instance.get_info.side_effect = yf.exceptions.YFTickerMissingError
        
        result = self.test_market_data_fetcher.fetch_asset_info(self.ticker_symbol)
        self.assertRegex(result, r"An error occurred: .*")

    def test_fetch_asset_info_generic_http_error_message(self):
        self.mock_ticker_instance.get_info.side_effect = requests.exceptions.HTTPError("HTTPError")
        
        result = self.test_market_data_fetcher.fetch_asset_info(self.ticker_symbol)
        self.assertEqual(result, "An HTTP error occurred: HTTPError")

    def test_fetch_asset_info_request_exception_message(self):
        self.mock_ticker_instance.get_info.side_effect = requests.exceptions.RequestException("RequestException")
        
        result = self.test_market_data_fetcher.fetch_asset_info(self.ticker_symbol)
        self.assertEqual(result, "A request exception ocurred: RequestException")

    def test_fetch_asset_info_general_exception_message(self):
        self.mock_ticker_instance.get_info.side_effect = Exception("Exception")
        
        result = self.test_market_data_fetcher.fetch_asset_info(self.ticker_symbol)
        self.assertEqual(result,  "An error occurred: Exception")

    def tearDown(self):
        patch.stopall()


if __name__ == "__main__":
    unittest.main()