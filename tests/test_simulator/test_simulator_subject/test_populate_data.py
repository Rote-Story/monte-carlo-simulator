
import unittest
from unittest.mock import Mock
from matplotlib import pyplot as plt
import numpy as np
import yfinance as yf
import pandas as pd
from pandas.testing import assert_frame_equal

from monte_carlo_simulator.data_fetcher.market_data_fetcher import MarketDataFetcher
from monte_carlo_simulator.gui.frames.error_frame_obs import ErrorFrame
from monte_carlo_simulator.gui.inter.observer_inter import Observer
from monte_carlo_simulator.model.market_index import MarketIndex
from monte_carlo_simulator.model.risk_free_security import RiskFreeSecurity
from monte_carlo_simulator.model.stock import Stock
from monte_carlo_simulator.service.simulator_subj import Simulator

class TestPopulateData(unittest.TestCase):


    # Create data to use with stock_data assignment testing
    mock_ticker = Mock(spec=yf.Ticker)
    mock_figure = Mock(spec=plt.Figure)
    asset_symbol = 'IBM'
    his_vol = 0.15

    # Read in stored data for testing, set index to datetime 
    asset_data = pd.read_csv('.\\tests\\test_simulator\\testing_data\\asset_data.csv', header=[0, 1], index_col=[0])
    asset_data.index = pd.to_datetime(asset_data.index, utc=True)
    
    # Risk-free rate testing data
    rfr_symbol = '^IRX'
    risk_free_rate = 0.04
    rfr_data = pd.read_csv('.\\tests\\test_simulator\\testing_data\\rfr_data.csv', header=[0, 1], index_col=[0])
    rfr_data.index = pd.to_datetime(rfr_data.index, utc=True)

   # Market testing data
    market_symbol = '^GSPC'
    market_returns = 0.17
    market_data = pd.read_csv('.\\tests\\test_simulator\\testing_data\\market_data.csv', header=[0, 1], index_col=[0])
    market_data.index = pd.to_datetime(market_data.index, utc=True)

    # Read in istoric dividends 
    his_div = pd.read_csv('.\\tests\\test_simulator\\testing_data\\his_div_data.csv', header=[0, 1], index_col=[0])
    his_div.index = pd.to_datetime(his_div.index, utc=True)
    
    # Convert historic dividend data to a pandas.Series object to match yfinance output format
    his_div = pd.Series(np.reshape(np.array(his_div), (250)), index=his_div.index)

    def setUp(self):
            
        # Create mock dependencies for Simulator
        self.mock_data_fetcher = Mock(spec=MarketDataFetcher)
        self.mock_financial_asset = Mock(spec=Stock)
        self.mock_market_index = Mock(spec=MarketIndex)
        self.mock_risk_free_sec = Mock(spec=RiskFreeSecurity)

        # Create mock observers to test subject/observer methods
        self.mock_observer = Mock(spec=Observer)
        self.mock_error_observer = Mock(spec=ErrorFrame)
        
        # Create a new "blank" simulator_subject for each test
        self.simulator_subject = Simulator(
            market_data_fetcher=self.mock_data_fetcher, 
            financial_asset=self.mock_financial_asset,
            market_index=self.mock_market_index, 
            risk_free_sec=self.mock_risk_free_sec
            )
        
        # Configure data fetcher mock object return values
        self.mock_data_fetcher.configure_mock(error_message=None)
        self.mock_data_fetcher.fetch_rfr_data.return_value = self.rfr_data        
        self.mock_data_fetcher.fetch_market_data.return_value = self.market_data
        self.mock_data_fetcher.fetch_ticker_object.return_value = self.mock_ticker
        self.mock_data_fetcher.fetch_asset_data.return_value = self.asset_data
        self.mock_data_fetcher.fetch_historic_div.return_value = self.his_div

    def test_populate_data_capm_valid_input_error_is_none(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Capital Asset Pricing Model'
            )

        # Successful calls should not produce an error message
        self.assertIsNone(self.simulator_subject.error_message) 

    def test_populate_data_capm_rfr_data_output(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Capital Asset Pricing Model'
            )

        # Subject stock_data.his_data should match data_fetcher return value
        assert_frame_equal(self.simulator_subject.risk_free_sec.rfr_data, self.rfr_data)

    def test_populate_data_capm_rfr_symbol_output(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Capital Asset Pricing Model'
            )

        self.assertEqual(self.simulator_subject.risk_free_sec.rfr_symbol, self.rfr_symbol)

    def test_populate_data_capm_error_message(self):
        # Set error return value
        self.mock_data_fetcher.configure_mock(error_message='An error occurred: Exception')
       
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Capital Asset Pricing Model'
            )

        self.assertEqual(self.simulator_subject.error_message, 'An error occurred: Exception') 

    def test_populate_data_capm_fetch_rfr_data_called_once(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Capital Asset Pricing Model'
            )

        self.mock_data_fetcher.fetch_rfr_data.assert_called_once_with(self.rfr_symbol, '5y')

    def test_populate_data_capm_asset_symbol_type_error(self):
        with self.assertRaises(TypeError) as e:

            # Call method for testing
            self.simulator_subject.populate_data(
                None, 
                self.market_symbol,
                self.rfr_symbol,
                '5y',
                'Capital Asset Pricing Model'
                )
            
            self.assertRegex(str(e), r'"asset_symbol" must be of type str, not \.*')

    def test_populate_data_capm_market_symbol_type_error(self):
        with self.assertRaises(TypeError) as e:

            # Call method for testing
            self.simulator_subject.populate_data(
                self.asset_symbol, 
                None,
                self.rfr_symbol,
                '5y',
                'Capital Asset Pricing Model'
                )
            
            self.assertRegex(str(e), r'"market_symbol" must be of type str, not \.*')

    def test_populate_data_capm_rfr_symbol_type_error(self):
        # Test method using with statement
        with self.assertRaises(TypeError) as e:
            
            # Call method for testing
            self.simulator_subject.populate_data(
                self.asset_symbol, 
                self.market_symbol,
                None,
                '5y',
                'Capital Asset Pricing Model'
                )
            
            self.assertRegex(str(e), r'"rfr_symbol" must be of type str, not \.*')

    def test_populate_data_capm_market_data_output(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Capital Asset Pricing Model'
            )
        
        # Subject stock_data.his_data should match data_fetcher return value
        assert_frame_equal(self.simulator_subject.market_index.market_data, self.market_data)

    def test_populate_data_capm_market_symbol_output(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Capital Asset Pricing Model'
            )
        
        self.assertEqual(self.simulator_subject.market_index.market_symbol, self.market_symbol)

    def test_populate_data_fetch_market_data_called_once(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Capital Asset Pricing Model'
            )

        self.mock_data_fetcher.fetch_market_data.assert_called_once_with(self.market_symbol, '5y')

    def test_populate_data_ddm_valid_input_calls_fetch_historic_div(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Dividend Discount Model'
            )
        
        self.mock_data_fetcher.fetch_historic_div.assert_called_once_with(self.mock_financial_asset.asset_ticker)

    def test_populate_data_valid_input_asset_ticker_output(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Dividend Discount Model'
            )
        
        self.assertIsInstance(self.simulator_subject.financial_asset.asset_ticker, yf.Ticker)
        self.assertIs(self.simulator_subject.financial_asset.asset_ticker, self.mock_ticker)

    def test_populate_data_valid_input_asset_symbol_output(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Dividend Discount Model'
            )
        
        self.assertEqual(self.simulator_subject.financial_asset.asset_symbol, self.asset_symbol)

    def test_populate_data_valid_input_asset_data_output(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Dividend Discount Model'
            )
        
        assert_frame_equal(self.simulator_subject.financial_asset.asset_data, self.asset_data)

    def test_populate_data_same_period_different_symbol(self):
        # Set the period to match the method call argument
        self.mock_financial_asset.configure_mock(period='5y')

        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Dividend Discount Model'
            )

        self.mock_data_fetcher.fetch_ticker_object.assert_called_once()
        self.mock_data_fetcher.fetch_asset_data.assert_called_once()

    def test_populate_data_different_period_same_symbol(self):
        # Set the symbol to match the method call argument
        self.mock_financial_asset.configure_mock(asset_symbol=self.asset_symbol)

        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Dividend Discount Model'
            )

        self.mock_data_fetcher.fetch_ticker_object.assert_called_once()
        self.mock_data_fetcher.fetch_asset_data.assert_called_once()

    def test_populate_data_same_period_same_symbol(self):
        # Set the period to match the method call
        self.mock_financial_asset.configure_mock(period='5y')
        self.mock_financial_asset.configure_mock(asset_symbol=self.asset_symbol)

        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Dividend Discount Model'
            )

        # If the existing symbol and period both match, then the fetcher should not be called 
        self.mock_data_fetcher.fetch_ticker_object.assert_not_called()
        self.mock_data_fetcher.fetch_asset_data.assert_not_called()

    def test_populate_data_fetch_ticker_object_called_once(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Dividend Discount Model'
            )
        
        self.mock_data_fetcher.fetch_ticker_object.assert_called_once_with(self.asset_symbol)

    def test_populate_data_fetch_asset_data_called_once(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Dividend Discount Model'
            )
        
        self.mock_data_fetcher.fetch_asset_data.assert_called_once_with(self.asset_symbol, '5y')

    def test_populate_data_non_capm_fetch_market_data_not_called(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Simple Average Returns'
            )
        
        self.mock_data_fetcher.fetch_market_data.assert_not_called()

    def test_populate_data_non_capm_fetch_rfr_data_not_called(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Simple Average Returns'
            )
        
        self.mock_data_fetcher.fetch_rfr_data.assert_not_called()

    def test_populate_data_non_ddm_fetch_historic_div_not_called(self):
        # Call method for testing
        self.simulator_subject.populate_data(
            self.asset_symbol, 
            self.market_symbol,
            self.rfr_symbol,
            '5y',
            'Simple Average Returns'
            )
        
        self.mock_data_fetcher.fetch_historic_div.assert_not_called()
    

if __name__ == '__main__':
    unittest.main()