

import unittest
from unittest.mock import Mock, patch
from requests.exceptions import RequestException, HTTPError
import yfinance as yf
import pandas as pd
from pandas.testing import assert_frame_equal

from monte_carlo_simulator.data_fetcher.market_data_fetcher import CachedLimiterSession, MarketDataFetcher


class TestFetchRFRData(unittest.TestCase):
    
    # Create test variables
    rfr_symbol = '^TNX'
    rfr_data = pd.DataFrame({
            'Date': ['2023-01-01', '2023-01-02'], 
            'Adj Close': ['5272.0', '5244.0']
            })
    
    def setUp(self):
        session = CachedLimiterSession.get_session()
        self.market_data_fetcher = MarketDataFetcher(session)
        self.mock_ticker_instance = Mock(spec=yf.Ticker) # Mock ticker object
        patcher = patch('monte_carlo_simulator.data_fetcher.market_data_fetcher.yf.download', return_value=self.rfr_data)
        self.mock_download = patcher.start()

    
    def tearDown(self):
        patch.stopall()

    def test_fetch_rfr_data_valid_input(self):
        result = self.market_data_fetcher.fetch_rfr_data(self.rfr_symbol)
        assert_frame_equal(result, self.rfr_data)

    def test_fetch_rfr_data_return_value(self):
        result = self.market_data_fetcher.fetch_rfr_data(self.rfr_symbol)
        self.assertEqual(result.iloc[0].iloc[1], '5272.0')
    
    def test_fetch_rfr_data_return_type(self):
        result = self.market_data_fetcher.fetch_rfr_data(self.rfr_symbol)
        self.assertIsInstance(result, pd.DataFrame)

    def test_fetch_rfr_data_missing_market_data(self):
        # Set download return value
        self.mock_download.return_value = pd.DataFrame({})
        
        self.market_data_fetcher.fetch_rfr_data(self.rfr_symbol)
        result = self.market_data_fetcher._error_message
        self.assertEqual(result, f'No data found for this ticker: {self.rfr_symbol}')

    def test_fetch_rfr_data_request_exception(self):
        # Set download return value
        self.mock_download.side_effect = RequestException
    
        self.market_data_fetcher.fetch_rfr_data(self.rfr_symbol)
        result = self.market_data_fetcher._error_message
        self.assertRegex(result, r'A request exception ocurred: \.*')
    
    def test_fetch_rfr_data_generic_http_error_message(self):
        self.mock_download.side_effect = HTTPError('HTTPError')
        
        self.market_data_fetcher.fetch_rfr_data(self.rfr_symbol)
        result = self.market_data_fetcher._error_message
        self.assertEqual(result, 'An HTTP error ocurred: HTTPError')

    def test_fetch_rfr_data_general_exception_message(self):
        self.mock_download.side_effect = Exception('Exception')
        
        self.market_data_fetcher.fetch_rfr_data(self.rfr_symbol)
        result = self.market_data_fetcher._error_message
        self.assertEqual(result,  'An error ocurred: Exception')


if __name__ == '__main__':
    unittest.main()