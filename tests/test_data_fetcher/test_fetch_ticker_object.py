

import unittest
from unittest.mock import patch, Mock
from requests import RequestException
from requests.exceptions import HTTPError
import yfinance as yf


from monte_carlo_simulator.data_fetcher.market_data_fetcher import CachedLimiterSession, MarketDataFetcher


class TestFetchTickerObject(unittest.TestCase):

    # Create test variables
    ticker_symbol = 'AAPL'

    def setUp(self):
        session = CachedLimiterSession.get_session()
        self.market_data_fetcher = MarketDataFetcher(session) 
        self.mock_ticker_instance = Mock(spec=yf.Ticker) # Mock yfinance.Ticker object
        self.mock_ticker_instance.get_info.return_value = {
            'symbol': 'AAPL',
            'shortName' : 'Apple Inc.',
            'previousClose': '206.11'
        }
        self.patcher = patch('yfinance.Ticker', return_value=self.mock_ticker_instance)
        self.patcher.start()

    def tearDown(self):
        patch.stopall() # Clean up post-test patches
        
    def test_fetch_ticker_object_valid_input(self):
        result = self.market_data_fetcher.fetch_ticker_object(
            self.ticker_symbol)
        
        self.assertEqual(result, self.mock_ticker_instance) 
        self.assertIsNone(self.market_data_fetcher._error_message)

    def test_fetch_ticker_object_function_called_once(self):
        self.market_data_fetcher.fetch_ticker_object(self.ticker_symbol)
        self.mock_ticker_instance.get_info.assert_called_once()
        
    def test_fetch_ticker_object_generic_http_error_message(self):
        self.mock_ticker_instance.get_info.side_effect = HTTPError('HTTPError')
        
        # Call fetch_ticker to test error handling
        self.market_data_fetcher.fetch_ticker_object(self.ticker_symbol)

        # Get exception message from MarketDataFetcher class
        result = self.market_data_fetcher._error_message
        self.assertEqual(result, 'An HTTP error ocurred: HTTPError')

    def test_fetch_ticker_object_request_exception_message(self):
        self.mock_ticker_instance.get_info.side_effect = RequestException('RequestException')
        
        # Call fetch_ticker to test error handling
        self.market_data_fetcher.fetch_ticker_object(self.ticker_symbol)

        # Get error message from MarketDataFetcher class
        result = self.market_data_fetcher._error_message
        self.assertEqual(result, 'A request exception ocurred: RequestException')

    def test_fetch_ticker_object_general_exception_message(self):
        self.mock_ticker_instance.get_info.side_effect = Exception('Exception')

        # Call fetch_ticker to test error handling
        self.market_data_fetcher.fetch_ticker_object(self.ticker_symbol)

        # Get error message from MarketDataFetcher class
        result = self.market_data_fetcher._error_message
        self.assertEqual(result,  'An error ocurred: Exception')

    def test_fetch_ticker_object_empty_ticker_info_exception_message(self):
        self.mock_ticker_instance.get_info.return_value = {}

        # Call fetch_ticker to test error handling
        self.market_data_fetcher.fetch_ticker_object(self.ticker_symbol)

        # Get error message from MarketDataFetcher class
        result = self.market_data_fetcher._error_message
        self.assertRegex(result,  r'An error ocurred: \.*')
    

if __name__ == '__main__':
    unittest.main()