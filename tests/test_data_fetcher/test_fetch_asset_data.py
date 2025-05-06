

import unittest
from unittest.mock import patch
from requests.exceptions import RequestException, HTTPError
import pandas as pd
from pandas.testing import assert_frame_equal

from monte_carlo_simulator.data_fetcher.market_data_fetcher import CachedLimiterSession, MarketDataFetcher


class TestFetchAssetData(unittest.TestCase):
    
    # Test variables
    ticker_symbol = 'IBM'
    asset_data = pd.DataFrame({
        'Date': ['2023-01-01', '2023-01-02'], 
        'Adj Close': ['150.0', '152.0']
        })

    
    def setUp(self):
        session = CachedLimiterSession.get_session()
        self.market_data_fetcher = MarketDataFetcher(cached_limiter_session=session) 
        patcher = patch('monte_carlo_simulator.data_fetcher.market_data_fetcher.yf.download', return_value=self.asset_data)
        self.mock_download = patcher.start()

    def tearDown(self):
        patch.stopall()
    
    def test_fetch_asset_data_valid_input(self):
        result = self.market_data_fetcher.fetch_asset_data(self.ticker_symbol)
        assert_frame_equal(result, self.asset_data)

    def test_fetch_asset_data_return_value(self):
        result = self.market_data_fetcher.fetch_asset_data(self.ticker_symbol)
        self.assertEqual(result.iloc[0].iloc[1], '150.0')
    
    def test_fetch_asset_data_return_type(self):
        result = self.market_data_fetcher.fetch_asset_data(self.ticker_symbol)
        self.assertIsInstance(result, pd.DataFrame)

    def test_fetch_asset_data_missing_asset_data(self):
        self.mock_download.return_value = pd.DataFrame({})
        self.market_data_fetcher.fetch_asset_data(self.ticker_symbol)

        result = self.market_data_fetcher._error_message
        self.assertEqual(result, f'No data found for this ticker: {self.ticker_symbol}')
    
    def test_fetch_asset_data_generic_http_error_message(self):
        self.mock_download.side_effect = HTTPError('HTTPError')
        
        self.market_data_fetcher.fetch_asset_data(self.ticker_symbol)
        result = self.market_data_fetcher._error_message
        self.assertEqual(result, 'An HTTP error occurred: HTTPError')

    def test_fetch_asset_data_request_exception_message(self):
        self.mock_download.side_effect = RequestException('RequestException')
        
        self.market_data_fetcher.fetch_asset_data(self.ticker_symbol)
        result = self.market_data_fetcher._error_message
        self.assertEqual(result, 'A request exception ocurred: RequestException')

    def test_fetch_asset_data_general_exception_message(self):
        self.mock_download.side_effect = Exception('Exception')
        
        self.market_data_fetcher.fetch_ticker_object(self.ticker_symbol)
        result = self.market_data_fetcher._error_message
        self.assertRegex(result, r'An error ocurred:\.*')


if __name__ == '__main__':
    unittest.main()