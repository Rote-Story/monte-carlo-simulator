
import unittest
from unittest.mock import DEFAULT, patch, Mock
import yfinance as yf
import pandas as pd
import numpy as np

from monte_carlo_simulator.model import MarketIndex, Stock, RiskFreeSecurity
from monte_carlo_simulator.data_fetcher import MarketDataFetcher
from monte_carlo_simulator.service.calculator.asset_calculator import calc_exp_returns


class TestCalcExpectedRetrns(unittest.TestCase):

    # Create data to use with  testing
    mock_ticker = Mock(spec=yf.Ticker) # Ticker symbol object
    asset_symbol = 'IBM'
    market_symbol = '^GSPC'
    error_message = 'Exception!' # Fake error message text

    # Expected returns testing data
    expected_returns = 0.09
    div_growth_rate = 0.01
    beta = 0.67
    market_returns = 0.17
    risk_free_rate = 0.04
    end_index = -252
    
    # Read in stored data for testing
    asset_data = pd.read_csv('.\\tests\\test_simulator\\testing_data\\asset_data.csv', header=[0, 1], index_col=[0])
    market_data = pd.read_csv('.\\tests\\test_simulator\\testing_data\\market_data.csv', header=[0, 1], index_col=[0])
    rfr_data = pd.read_csv('.\\tests\\test_simulator\\testing_data\\rfr_data.csv', header=[0, 1], index_col=[0])
    his_div = pd.read_csv('.\\tests\\test_simulator\\testing_data\\his_div_data.csv', header=[0, 1], index_col=[0])
    

    # Change index type from string to datetime 
    asset_data.index = pd.to_datetime(asset_data.index, utc=True)
    market_data.index = pd.to_datetime(market_data.index, utc=True)
    rfr_data.index = pd.to_datetime(rfr_data.index, utc=True)
    his_div.index = pd.to_datetime(his_div.index, utc=True)

    # Convert historic dividend data to a pandas.Series object to match yfinance output format
    his_div = pd.Series(np.reshape(np.array(his_div), (250)), index=his_div.index)

    def setUp(self):
            
        # Create mock dependencies for Simulator
        self.mock_data_fetcher = Mock(spec=MarketDataFetcher)
        self.mock_financial_asset = Mock(spec=Stock)
        self.mock_market_index = Mock(spec=MarketIndex)
        self.mock_risk_free_sec = Mock(spec=RiskFreeSecurity)
        
        # Configure default mock return values 
        self.mock_data_fetcher.configure_mock(error_message=None)
        self.mock_financial_asset.configure_mock(
            asset_ticker=self.mock_ticker, 
            asset_symbol=self.asset_symbol,
            asset_data=self.asset_data,
            his_div=self.his_div
            )
        self.mock_risk_free_sec.configure_mock(risk_free_rate=self.risk_free_rate, rfr_data=self.rfr_data)
        self.mock_market_index.configure_mock(market_data=self.market_data, market_returns=self.market_returns)

        # Create patcher for mock function calls
        patcher = patch.multiple('monte_carlo_simulator.service.calculator.asset_calculator', 
                    calc_div_growth_rate=DEFAULT,
                    ddm_returns=DEFAULT,
                    calc_beta=DEFAULT, 
                    capm_returns=DEFAULT,
                    calc_rfr=DEFAULT,
                    calc_market_returns=DEFAULT,
                    average_returns=DEFAULT,
                    exponential_weighted_average=DEFAULT,
                    price_col_checker=DEFAULT
                    )
        self.calc_patcher = patcher.start()

        # Set patched method return values
        self.calc_patcher['calc_div_growth_rate'].return_value = self.div_growth_rate
        self.calc_patcher['ddm_returns'].return_value = self.expected_returns
        self.calc_patcher['calc_beta'].return_value = self.beta
        self.calc_patcher['capm_returns'].return_value = self.expected_returns
        self.calc_patcher['calc_rfr'].return_value = self.risk_free_rate
        self.calc_patcher['calc_market_returns'].return_value = self.market_returns
        self.calc_patcher['average_returns'].return_value = self.expected_returns
        self.calc_patcher['exponential_weighted_average'].return_value = self.expected_returns
        self.calc_patcher['price_col_checker'].return_value = 'Close'


    def tearDown(self):
        patch.stopall()

    def test_get_exp_returns_ddm_returns_output(self):
        # Set expected returns flag
        self.mock_financial_asset.configure_mock(exp_ret_flag='Dividend Discount Model')

        # Set method return values  
        self.mock_data_fetcher.fetch_historic_div.return_value = self.his_div


        # Call method for testing
        exp_returns = calc_exp_returns(
            financial_asset=self.mock_financial_asset,
            market_index=self.mock_market_index,
            risk_free_sec=self.mock_risk_free_sec,
            )
        
        self.assertEqual(exp_returns, self.expected_returns)
        self.calc_patcher['ddm_returns'].assert_called_once()
        self.calc_patcher['calc_div_growth_rate'].assert_called_once()
        self.calc_patcher['price_col_checker'].assert_called_once()

    def test_get_exp_returns_ddm_returns_end_index_calls(self):
        # Set expected returns flag
        self.mock_financial_asset.configure_mock(exp_ret_flag='Dividend Discount Model')
        
        # Call method for testing
        calc_exp_returns(
            financial_asset=self.mock_financial_asset,
            market_index=self.mock_market_index,
            risk_free_sec=self.mock_risk_free_sec,
            end_index=self.end_index
            )
            
        # Verify correct error message issued
        self.calc_patcher['calc_div_growth_rate'].assert_called_once()

    
    def test_get_exp_returns_capm_returns_output(self):
        # Set expected returns flag
        self.mock_financial_asset.configure_mock(exp_ret_flag='Capital Asset Pricing Model')

        # Call method for testing
        exp_returns = calc_exp_returns(
            financial_asset=self.mock_financial_asset,
            market_index=self.mock_market_index,
            risk_free_sec=self.mock_risk_free_sec,
            )
        
        self.assertEqual(exp_returns, self.expected_returns)
        self.calc_patcher['calc_beta'].assert_called_once()
        self.calc_patcher['calc_market_returns'].assert_called_once()
        self.calc_patcher['calc_rfr'].assert_called_once()
        self.calc_patcher['capm_returns'].assert_called_once_with(
            beta=self.beta, 
            market_returns=self.mock_market_index.market_returns,
            risk_free_rate=self.mock_risk_free_sec.risk_free_rate
            )

    def test_get_exp_returns_capm_returns_end_index_calls(self):
        # Set expected returns flag
        self.mock_financial_asset.configure_mock(exp_ret_flag='Capital Asset Pricing Model')

        # Call method for testing
        calc_exp_returns(
            financial_asset=self.mock_financial_asset,
            market_index=self.mock_market_index,
            risk_free_sec=self.mock_risk_free_sec,
            end_index=self.end_index
            )
        
        self.calc_patcher['calc_beta'].assert_called_once()
        self.calc_patcher['calc_market_returns'].assert_called_once()
        self.calc_patcher['calc_rfr'].assert_called_once()
        self.calc_patcher['capm_returns'].assert_called_once_with(
            beta=self.beta, 
            market_returns=self.mock_market_index.market_returns,
            risk_free_rate=self.mock_risk_free_sec.risk_free_rate
            )

    def test_get_exp_returns_simple_average_returns_output(self):
        # Set expected returns flag
        self.mock_financial_asset.configure_mock(exp_ret_flag='Simple Average Returns')

        # Call method for testing
        exp_returns = calc_exp_returns(
            financial_asset=self.mock_financial_asset,
            market_index=self.mock_market_index,
            risk_free_sec=self.mock_risk_free_sec
            )
        
        self.assertEqual(self.expected_returns, exp_returns)
        self.calc_patcher['average_returns'].assert_called_once()

    def test_get_exp_returns_simple_average_returns_end_index_output(self):
        # Set expected returns flag
        self.mock_financial_asset.configure_mock(exp_ret_flag='Simple Average Returns')

        # Call method for testing
        exp_returns = calc_exp_returns(
            financial_asset=self.mock_financial_asset,
            market_index=self.mock_market_index,
            risk_free_sec=self.mock_risk_free_sec,
            end_index=self.end_index
            )
        
        self.assertEqual(self.expected_returns, exp_returns)
        self.calc_patcher['average_returns'].assert_called_once()

    def test_get_exp_returns_weighted_average_output(self):
        # Set expected returns flag
        self.mock_financial_asset.configure_mock(exp_ret_flag='Exponential Weighted Average Returns')

        # Call method for testing
        exp_returns = calc_exp_returns(
            financial_asset=self.mock_financial_asset,
            market_index=self.mock_market_index,
            risk_free_sec=self.mock_risk_free_sec,
            returns_window=150
            )
        
        self.assertEqual(self.expected_returns, exp_returns)
        self.calc_patcher['exponential_weighted_average'].assert_called_once()

    def test_get_exp_returns_weighted_average_returns_end_index_output(self):
        # Set expected returns flag
        self.mock_financial_asset.configure_mock(exp_ret_flag='Exponential Weighted Average Returns')

        # Call method for testing
        exp_returns = calc_exp_returns(
            financial_asset=self.mock_financial_asset,
            market_index=self.mock_market_index,
            risk_free_sec=self.mock_risk_free_sec,
            end_index=self.end_index
            )
        
        self.assertEqual(self.expected_returns, exp_returns)
        self.calc_patcher['exponential_weighted_average'].assert_called_once()


if __name__ == '__main__':
    unittest.main()
