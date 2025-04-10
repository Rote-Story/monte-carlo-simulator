

import unittest
from unittest.mock import MagicMock, patch
from requests.exceptions import RequestException, HTTPError
import yfinance as yf
import pandas as pd
from pandas.testing import assert_frame_equal

from monte_carlo_simulator.data_fetcher.market_data_fetcher import MarketDataFetcher


class TestFetchAssetData(unittest.TestCase):

    def setUp(self):
        self.ticker_symbol = "IBM"
        self.mock_ticker_instance = MagicMock(spec=yf.Ticker)

        # CachedLimiterSession not needed for testing
        self.test_market_data_fetcher = MarketDataFetcher(cached_limiter_session=None) 

        # Setup patch for yfinance.Ticker requests
        ticker_patch = patch("yfinance.Ticker", return_value=self.mock_ticker_instance)
        ticker_patch.start()
    
    def test_fetch_asset_data_valid_input(self):
        df = pd.DataFrame({
            "Date": ["2023-01-01", "2023-01-02"], 
            "Adj Close": ["150.0", "152.0"]
            })
        with patch("yfinance.download") as mock_download:
            mock_download.return_value = df
            result = self.test_market_data_fetcher.fetch_asset_data(self.ticker_symbol)
        assert_frame_equal(result, df)

    def test_fetch_asset_data_return_value(self):
        with patch("yfinance.download") as mock_download:
            mock_download.return_value = pd.DataFrame({
                "Date": ["2023-01-01", "2023-01-02"], 
                "Adj Close": ["150.0", "152.0"]
                })

            result = self.test_market_data_fetcher.fetch_asset_data(self.ticker_symbol)
        self.assertEqual(result.iloc[0].iloc[1], "150.0")
    
    def test_fetch_asset_data_return_type(self):
        with patch("yfinance.download") as mock_download:
            mock_download.return_value = pd.DataFrame({
                "Date": ["2023-01-01", "2023-01-02"], 
                "Adj Close": ["150.0", "152.0"]
                })

            result = self.test_market_data_fetcher.fetch_asset_data(self.ticker_symbol)
        self.assertIsInstance(result, pd.DataFrame)

    def test_fetch_asset_data_missing_asset_data(self):
        with patch("yfinance.download") as mock_download:
            mock_download.return_value = pd.DataFrame({})
        
            self.test_market_data_fetcher.fetch_asset_data(self.ticker_symbol)
        result = self.test_market_data_fetcher._error_message
        self.assertEqual(result, f"No data found for this ticker: {self.ticker_symbol}")

    def test_fetch_asset_data_request_exception(self):
        with patch("yfinance.download") as mock_download:
            mock_download.side_effect = RequestException
    
            self.test_market_data_fetcher.fetch_asset_data(self.ticker_symbol)
        result = self.test_market_data_fetcher._error_message
        self.assertRegex(result, r"A request ocurred: \.*")
    
    @patch("yfinance.download")
    def test_fetch_asset_data_ticker_get_info_called_once(self, _):
        self.test_market_data_fetcher.fetch_asset_data(self.ticker_symbol)
        self.mock_ticker_instance.get_info.assert_called_once()
    
    @patch("yfinance.download")
    def test_fetch_asset_data_generic_http_error_message(self, _):
        self.mock_ticker_instance.get_info.side_effect = HTTPError("HTTPError")
        
        self.test_market_data_fetcher.fetch_asset_data(self.ticker_symbol)
        result = self.test_market_data_fetcher._error_message
        self.assertEqual(result, "An HTTP error occurred: HTTPError")

    @patch("yfinance.download")
    def test_fetch_asset_data_request_exception_message(self, _):
        self.mock_ticker_instance.get_info.side_effect = RequestException("RequestException")
        
        self.test_market_data_fetcher.fetch_asset_data(self.ticker_symbol)
        result = self.test_market_data_fetcher._error_message
        self.assertEqual(result, "A request exception ocurred: RequestException")

    @patch("yfinance.download")
    def test_fetch_asset_data_general_exception_message(self, _):
        self.mock_ticker_instance.get_info.side_effect = Exception("Exception")
        
        self.test_market_data_fetcher.fetch_asset_info(self.ticker_symbol)
        result = self.test_market_data_fetcher._error_message
        self.assertEqual(result,  "An error occurred: Exception")

    def tearDown(self):
        patch.stopall()


if __name__ == "__main__":
    unittest.main()