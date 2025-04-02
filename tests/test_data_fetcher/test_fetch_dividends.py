
import unittest
from unittest.mock import Mock, patch
from requests.exceptions import RequestException
import yfinance as yf
import pandas as pd
from pandas.testing import assert_series_equal

from monte_carlo_simulator.data_fetcher.market_data_fetcher import MarketDataFetcher


class TestFetchDividends(unittest.TestCase):

    def setUp(self):
        self.mock_ticker_instance = Mock(spec=yf.Ticker) # Mock ticker object
        session = None # Session not needed for testing
        self.test_market_data_fetcher = MarketDataFetcher(session)
        patches = patch("yfinance.Ticker", return_value=self.mock_ticker_instance)
        patches.start()

    def test_fetch_dividends_valid_input(self):
        self.mock_ticker_instance.get_dividends.return_value = pd.Series({
            "2023-01-01": "0.50",
            "2023-04-01": "0.55",
            "2023-07-01": "0.60"
        })

        result = self.test_market_data_fetcher.fetch_dividends(self.mock_ticker_instance)
        assert_series_equal(result, self.mock_ticker_instance.get_dividends())

    def test_fetch_dividends_return_value(self):
        self.mock_ticker_instance.get_dividends.return_value = pd.Series({
            "2023-01-01": "0.50",
            "2023-04-01": "0.55",
            "2023-07-01": "0.60"
        })
        
        result = self.test_market_data_fetcher.fetch_dividends(self.mock_ticker_instance)
        self.assertEqual(result.iloc[2], "0.60")
    
    def test_fetch_dividends_return_type(self):
        self.mock_ticker_instance.get_dividends.return_value = pd.Series({
            "2023-01-01": "0.50",
            "2023-04-01": "0.55",
            "2023-07-01": "0.60"
        })
        
        result = self.test_market_data_fetcher.fetch_dividends(self.mock_ticker_instance)
        self.assertIsInstance(result, pd.Series)

    def test_fetch_dividends_ticker_get_dividend_called_once(self):
        self.test_market_data_fetcher.fetch_dividends(self.mock_ticker_instance)
        self.mock_ticker_instance.get_dividends.assert_called_once()

    def test_fetch_dividends_dividend_rate_key_error(self):
        self.mock_ticker_instance.get_info.return_value = {}
        
        result = self.test_market_data_fetcher.fetch_dividends(self.mock_ticker_instance)
        self.assertEqual(result, "Ticker object missing key value: Dividend Rate")

    def test_fetch_dividends_missing_dividends(self):
        self.mock_ticker_instance.get_dividends.return_value = pd.Series({})
        
        result = self.test_market_data_fetcher.fetch_dividends(self.mock_ticker_instance)
        self.assertEqual(result, "No dividend payment history found for this ticker")

    def test_fetch_dividends_request_exception(self):
        self.mock_ticker_instance.get_dividends.side_effect = RequestException
        
        result = self.test_market_data_fetcher.fetch_dividends(self.mock_ticker_instance)
        self.assertRegex(result, r"A request ocurred: .*")

    def test_fetch_dividends_ticker_get_info_called_once(self):
        # Verifying that function is validating ticker symbol with get_info()
        self.test_market_data_fetcher.fetch_dividends(self.mock_ticker_instance)
        self.mock_ticker_instance.get_info.assert_called_once()

    def tearDown(self):
        patch.stopall()


if __name__ == "__main__":
    unittest.main()