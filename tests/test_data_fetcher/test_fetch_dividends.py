
import unittest
from unittest.mock import MagicMock, patch
from requests.exceptions import RequestException
import pandas as pd
from pandas.testing import assert_series_equal
import yfinance as yf

from monte_carlo_simulator.data_fetcher.market_data_fetcher import CachedLimiterSession, MarketDataFetcher


class TestFetchDividends(unittest.TestCase):

    # Create test variables
    his_div = pd.Series({
            '2023-01-01': '0.50',
            '2023-04-01': '0.55',
            '2023-07-01': '0.60'
        })

    def setUp(self):
        session = CachedLimiterSession.get_session()
        self.market_data_fetcher = MarketDataFetcher(session)
        self.mock_ticker_instance = MagicMock(spec=yf.Ticker) # Mock ticker object
        self.mock_ticker_instance.get_info.return_value = {'dividendRate':0.01}
        self.mock_ticker_instance.get_dividends.return_value = self.his_div

    def test_fetch_dividends_valid_input(self):
        result = self.market_data_fetcher.fetch_historic_div(self.mock_ticker_instance)
        assert_series_equal(result, self.his_div)

    def test_fetch_dividends_return_value(self):
        result = self.market_data_fetcher.fetch_historic_div(self.mock_ticker_instance)
        self.assertEqual(result.iloc[2], '0.60')
    
    def test_fetch_dividends_return_type(self):
        result = self.market_data_fetcher.fetch_historic_div(self.mock_ticker_instance)
        self.assertIsInstance(result, pd.Series)

    def test_fetch_dividends_ticker_get_dividend_called_once(self):
        self.market_data_fetcher.fetch_historic_div(self.mock_ticker_instance)
        self.mock_ticker_instance.get_dividends.assert_called_once()

    def test_fetch_dividends_dividend_rate_key_error(self):
        self.mock_ticker_instance.get_info.return_value = {}

        # Call fetch_asset_info to test error handling 
        self.market_data_fetcher.fetch_historic_div(self.mock_ticker_instance)
        
        # Check MarketDataFetcher error message 
        result = self.market_data_fetcher._error_message
        
        self.assertEqual(result, 'Ticker object missing key value: Dividend Rate')

    def test_fetch_dividends_missing_dividends(self):
        self.mock_ticker_instance.get_dividends.return_value = pd.Series({})
        
        # Call fetch_asset_info to test error handling 
        self.market_data_fetcher.fetch_historic_div(self.mock_ticker_instance)
        
        # Check MarketDataFetcher error message 
        result = self.market_data_fetcher._error_message
        self.assertEqual(result, 'No dividend payment history found for this ticker')

    def test_fetch_dividends_request_exception(self):
        self.mock_ticker_instance.get_dividends.side_effect = RequestException
        
        # Call fetch_asset_info to test error handling 
        self.market_data_fetcher.fetch_historic_div(self.mock_ticker_instance)
        
        # Check MarketDataFetcher error message 
        result = self.market_data_fetcher._error_message
        self.assertRegex(result, r'A request ocurred: \.*')

    def test_fetch_dividends_generic_exception(self):
        self.mock_ticker_instance.get_dividends.side_effect = Exception
        
        # Call fetch_asset_info to test error handling 
        self.market_data_fetcher.fetch_historic_div(self.mock_ticker_instance)
        
        # Check MarketDataFetcher error message 
        result = self.market_data_fetcher._error_message
        self.assertRegex(result, r'An error ocurred: \.*')


if __name__ == '__main__':
    unittest.main()