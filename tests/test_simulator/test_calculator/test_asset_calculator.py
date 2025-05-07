
import unittest
from unittest.mock import DEFAULT, patch, Mock
import yfinance as yf
import pandas as pd
import numpy as np

from monte_carlo_simulator.model import MarketIndex, Stock, RiskFreeSecurity
from monte_carlo_simulator.data_fetcher import MarketDataFetcher
from monte_carlo_simulator.service.calculator.asset_calculator import *


class TestGetExpectedRetrns(unittest.TestCase):

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

class TestAssetReturnsCalculator(unittest.TestCase):

    # Dividend growth rate is the average percent change of historical growth rates
    # The growth rate = ((55-50)/50 + (60-55)/55)/2 
    div_growth_rate = 0.09545454545454546
    asset_data = pd.read_csv('.\\tests\\test_simulator\\testing_data\\asset_data.csv', header=[0, 1], index_col=[0])
    asset_data.index = pd.to_datetime(asset_data.index, utc=True)

    dividends = pd.Series(
        data=[0.50, 0.55, 0.60], 
        index=[pd.Timestamp('2018-07-01 00:00:00-05:00'),  
               pd.Timestamp('2022-08-06 00:00:00-05:00'),  
               pd.Timestamp('2023-07-01 00:00:00-05:00')]
        ) 

    def test_capm_returns(self):
        # Create testing variables to control result
        test_rfr = 0.04 # 4% risk-free rate
        test_beta = 1.239 
        test_market_returns = 0.07 # 7% market returns 

        # risk_free_rate + beta(market_returns - risk_free_rate) = capm
        test_capm = test_rfr + test_beta * (test_market_returns - test_rfr)
        result = capm_returns(test_beta, test_market_returns, test_rfr)
        
        self.assertAlmostEqual(
            test_capm, 
            result 
            )
    
    def test_ddm_returns(self):
        # Create test data variables
        test_current_price = 233.85
        test_expected_div = 0.6572727272727272

        # expected returns = expected dividend per share/current price + dividend growth rate
        test_expected_returns = test_expected_div/test_current_price + self.div_growth_rate
        result = ddm_returns(
                test_current_price, 
                self.dividends,
                self.div_growth_rate
                )
        
        self.assertAlmostEqual(
            test_expected_returns,
            result
        )
    
    def test_calc_div_growth_rate(self):
        result = calc_div_growth_rate(self.dividends)
        
        self.assertAlmostEqual(
            self.div_growth_rate,
            result
            )

    def test_average_returns(self):
        test_avg_returns = self.asset_data['Close'].iloc[-30:].pct_change().mean()
        result = average_returns(self.asset_data, returns_window=30)
        
        self.assertAlmostEqual(
            test_avg_returns.iloc[0],
            result
            )
    
    def test_weighted_average_returns(self):
        result = exponential_weighted_average(self.asset_data, 30)
        expected_result = self.asset_data['Close'].pct_change() \
            .ewm(span=30, adjust=False) \
            .mean().iloc[-1].iloc[-1]

        self.assertAlmostEqual(expected_result, result)


class TestBetaCalculator(unittest.TestCase):

    # Read in stored data for testing
    market_data = pd.read_csv('.\\tests\\test_simulator\\testing_data\\market_data.csv', header=[0, 1], index_col=[0])
    asset_data = pd.read_csv('.\\tests\\test_simulator\\testing_data\\asset_data.csv', header=[0, 1], index_col=[0])

    # Change index type from string to datetime 
    market_data.index = pd.to_datetime(market_data.index)
    asset_data.index = pd.to_datetime(asset_data.index)

    start_date = '2020-04-08' # Earliest entry date in the test data

    # Create mock yf.Tickers, set .history return values
    mock_asset_ticker = Mock(spec=yf.Ticker)
    mock_asset_ticker.history.return_value = asset_data 

    mock_market_ticker = Mock(spec=yf.Ticker)
    mock_market_ticker.history.return_value = market_data


    def test_calc_beta_valid_input(self):
        result = calc_beta(self.asset_data, self.market_data)

        # Find expected returns from the dataset
        expected_returns = self.market_data.loc[str(self.start_date):]['Close'].iloc[:, 0] \
            .resample('ME') \
            .last() \
            .pct_change()
        
        # Find expected returns variance
        expected_variance = expected_returns.var() 
        
        #Find expected returns covariance 
        expected_cov = expected_returns.cov(
            self.asset_data.loc[str(self.start_date):]['Close'].iloc[:, 0] \
                .resample('ME') \
                .last() \
                .pct_change()
        ) 
        # Calculate expected beta
        expected_result = expected_cov / expected_variance

        self.assertAlmostEqual(result, expected_result)
        
    def test_calc_beta_type_output(self):
        result = calc_beta(self.asset_data, self.market_data)
        self.assertIsInstance(result, float)

    def test_calc_beta_asset_ticker_history_called_with_correct_args(self):
        calc_beta(self.asset_data, self.market_data)
    
    def test_calc_beta_test_invalid_market_ticker_input(self):
        with self.assertRaises(TypeError):
            calc_beta(self.mock_asset_ticker, 'IBM')

    def test__beta_test_invalid_asset_ticker_input(self):
        with self.assertRaises(TypeError):
            calc_beta(None, self.mock_market_ticker)

    def test__beta_test_invalid_market_and_asset_ticker_input(self):
        with self.assertRaises(TypeError):
            calc_beta('IBM', '^GSPC')

    def test_calc_beta_test_type_error_returns_none(self):
        with self.assertRaises(TypeError):
            result = calc_beta('ticker', 'IBM')
            self.assertIsNone(result)

    def test_calc_beta_invalid_asset_input_type_error_message(self):
        with self.assertRaises(TypeError) as e:
            calc_beta('data', self.mock_market_ticker)
            self.assertRegex(str(e), r'"asset_ticker" must be of type yfinance.Ticker, not  \.*') 
    
    def test_calc_beta_invalid_asset_market_type_error_message(self):
        with self.assertRaises(TypeError) as e:
            calc_beta(self.mock_asset_ticker, 'data')
            self.assertRegex(str(e), r'"market_ticker" must be of type yfinance.Ticker, not  \.*') 


if __name__ == '__main__':
    unittest.main()