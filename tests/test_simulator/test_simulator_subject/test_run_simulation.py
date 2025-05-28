import unittest
from unittest.mock import DEFAULT, patch, Mock
from matplotlib import pyplot as plt
import numpy as np
import yfinance as yf
import pandas as pd
from pandas.testing import assert_frame_equal

from monte_carlo_simulator.model import MarketIndex, Stock, RiskFreeSecurity
from monte_carlo_simulator.data_fetcher import MarketDataFetcher
from monte_carlo_simulator.gui.frames.error_frame_obs import ErrorFrame
from monte_carlo_simulator.gui.frames.vis_frames_obs import SimVisFrame, TrainTestVisFrame
from monte_carlo_simulator.gui.inter.observer_inter import Observer
from monte_carlo_simulator.service.simulator_subj import Simulator



class TestRunSimulation(unittest.TestCase):

    # Create data to use with stock_data assignment testing
    mock_ticker = Mock(spec=yf.Ticker)
    asset_symbol = 'IBM'
    asset_his_vol = 0.15

    # Market testing data
    market_symbol = '^GSPC'
    market_returns = 0.17
    daily_market_returns = 0.00005

    # Risk-free rate testing data
    rfr_symbol = '^IRX'
    rfr = 0.04
    daily_rfr = 0.00001

    # Expected returns testing data
    expected_returns = 0.09
    
    # Read in stored data for testing
    market_data = pd.read_csv('.\\tests\\test_simulator\\testing_data\\market_data.csv', header=[0, 1], index_col=[0])
    asset_data = pd.read_csv('.\\tests\\test_simulator\\testing_data\\asset_data.csv', header=[0, 1], index_col=[0])
    rfr_data = pd.read_csv('.\\tests\\test_simulator\\testing_data\\rfr_data.csv', header=[0, 1], index_col=[0])
    his_div = pd.read_csv('.\\tests\\test_simulator\\testing_data\\his_div_data.csv', header=[0, 1], index_col=[0])

    # Change index type from string to datetime 
    market_data.index = pd.to_datetime(market_data.index, utc=True)
    asset_data.index = pd.to_datetime(asset_data.index, utc=True)
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

        # Create mock observers to test subject/observer methods
        self.mock_observer = Mock(spec=Observer)
        self.mock_error_observer = Mock(spec=ErrorFrame)
        self.mock_sim_vis_observer = Mock(spec=SimVisFrame)
        
        # Create a new "blank" simulator_subject for each test
        self.simulator_subject = Simulator(
            market_data_fetcher=self.mock_data_fetcher, 
            financial_asset=self.mock_financial_asset,
            market_index=self.mock_market_index, 
            risk_free_sec=self.mock_risk_free_sec
            )
        
        # Create patcher for mock function calls
        patcher = patch.multiple('monte_carlo_simulator.service.simulator_subject', 
                    calc_volatility=DEFAULT,
                    calc_market_returns=DEFAULT,
                    calc_rfr=DEFAULT, 
                    calc_exp_returns=DEFAULT,
                    price_col_checker=DEFAULT,
                    monte_carlo_sim_vis=DEFAULT
                    )
        self.sim_patcher = patcher.start()

        # Set populate_data return values
        self.mock_data_fetcher.fetch_ticker_object.return_value = self.mock_ticker
        self.mock_data_fetcher.fetch_asset_data.return_value = self.asset_data
        self.mock_data_fetcher.configure_mock(error_message=None)
        self.mock_data_fetcher.fetch_market_data.return_value = self.market_data
        self.mock_data_fetcher.fetch_rfr_data.return_value = self.rfr_data
        self.mock_data_fetcher.fetch_historic_div.return_value = self.his_div

        # Set volatility return value
        self.sim_patcher['calc_volatility'].return_value = self.asset_his_vol
        
        # Set get_exp_returns return values
        self.sim_patcher['calc_exp_returns'].return_value = self.expected_returns

        # Set price_col_checker return value
        self.sim_patcher['price_col_checker'].return_value = 'Close'

        # Set visualization return value
        self.sim_patcher['monte_carlo_sim_vis'].return_value = Mock(spec=plt.Figure)

        # Replace monte_carlo_sim method with mock, set return value
        self.sim_data =  np.ndarray((252, 100)) # Save to variable for assertion checks
        self.simulator_subject.monte_carlo_sim = Mock(
             spec=self.simulator_subject.monte_carlo_sim,
             side_effect=self.sim_data
             )

        # Attach mock observers
        self.simulator_subject.attach(self.mock_sim_vis_observer)
        self.simulator_subject.attach(self.mock_observer)

    def tearDown(self):
        patch.stopall()
        
    def test_run_simulation_sim_figure_is_plt_figure(self):
        self.simulator_subject.run_simulation(
            asset_symbol=self.asset_symbol,
            market_symbol=self.market_symbol,
            rfr_symbol=self.rfr_symbol,
            period='5y',
            exp_ret_flag='Simple Average Returns',
            standev_window=30,
            time_horizon=12,
            n_simulations=100
        )
        self.assertIsInstance(self.simulator_subject.sim_figure, plt.Figure)

    def test_run_simulation_error_message_is_none(self):
        self.simulator_subject.run_simulation(
            asset_symbol=self.asset_symbol,
            market_symbol=self.market_symbol,
            rfr_symbol=self.rfr_symbol,
            period='5y',
            exp_ret_flag='Simple Average Returns',
            standev_window=30,
            time_horizon=12,
            n_simulations=100
        )
        self.assertIsNone(self.simulator_subject.error_message)

    def test_run_simulation_error_message_output(self):
        self.mock_data_fetcher.configure_mock(error_message='Exception!')
        self.simulator_subject.run_simulation(
            asset_symbol=self.asset_symbol,
            market_symbol=self.market_symbol,
            rfr_symbol=self.rfr_symbol,
            period='5y',
            exp_ret_flag='Simple Average Returns',
            standev_window=30,
            time_horizon=12,
            n_simulations=100
        )

        self.assertEqual(self.simulator_subject.error_message, 'Exception!')
    
    def test_run_simulation_calc_volatility_called_once(self):
        self.simulator_subject.run_simulation(
            asset_symbol=self.asset_symbol,
            market_symbol=self.market_symbol,
            rfr_symbol=self.rfr_symbol,
            period='5y',
            exp_ret_flag='Simple Average Returns',
            standev_window=30,
            time_horizon=12,
            n_simulations=100
        )
        self.sim_patcher['calc_volatility'].assert_called_once_with(self.asset_data, 30)

    def test_run_simulation_monte_carlo_sim_vis_called_once(self):
        self.simulator_subject.run_simulation(
            asset_symbol=self.asset_symbol,
            market_symbol=self.market_symbol,
            rfr_symbol=self.rfr_symbol,
            period='5y',
            exp_ret_flag='Simple Average Returns',
            standev_window=30,
            time_horizon=12,
            n_simulations=100
        )   
        self.sim_patcher['monte_carlo_sim_vis'].assert_called_once()

    def test_run_simulation_expected_returns_method_called_once(self):
            self.simulator_subject.run_simulation(
                asset_symbol=self.asset_symbol,
                market_symbol=self.market_symbol,
                rfr_symbol=self.rfr_symbol,
                period='5y',
                exp_ret_flag='Simple Average Returns',
                standev_window=30,
                time_horizon=12,
                n_simulations=100
            )             
            self.sim_patcher['calc_exp_returns'].assert_called_once_with(
                financial_asset=self.mock_financial_asset,
                market_index=self.mock_market_index,
                risk_free_sec=self.mock_risk_free_sec
                )
                       
    def test_run_simulation_price_col_checker_called_once(self):
            self.simulator_subject.run_simulation(
                asset_symbol=self.asset_symbol,
                market_symbol=self.market_symbol,
                rfr_symbol=self.rfr_symbol,
                period='5y',
                exp_ret_flag='Simple Average Returns',
                standev_window=30,
                time_horizon=12,
                n_simulations=100
            )           
            self.sim_patcher['price_col_checker'].assert_called_once_with(self.asset_data)

    def test_run_simulation_update_called_once(self):
            self.simulator_subject.run_simulation(
                asset_symbol=self.asset_symbol,
                market_symbol=self.market_symbol,
                rfr_symbol=self.rfr_symbol,
                period='5y',
                exp_ret_flag='Simple Average Returns',
                standev_window=30,
                time_horizon=12,
                n_simulations=100
            )
            self.mock_sim_vis_observer.update.assert_called_with(self.simulator_subject)

    def test_run_simulation_populate_data_called_once(self):
            self.simulator_subject.populate_data = Mock(name='populate_data')

            self.simulator_subject.run_simulation(
                asset_symbol=self.asset_symbol,
                market_symbol=self.market_symbol,
                rfr_symbol=self.rfr_symbol,
                period='5y',
                exp_ret_flag='Simple Average Returns',
                standev_window=30,
                time_horizon=12,
                n_simulations=100
            )
            self.simulator_subject.populate_data.assert_called_once_with(
                self.asset_symbol, 
                self.market_symbol,
                self.rfr_symbol, 
                '5y',
                'Simple Average Returns'
                )

    def test_run_simulation_monte_carlo_sim_called_once(self):
        self.simulator_subject.run_simulation(
            asset_symbol=self.asset_symbol,
            market_symbol=self.market_symbol,
            rfr_symbol=self.rfr_symbol,
            period='5y',
            exp_ret_flag='Simple Average Returns',
            standev_window=30,
            time_horizon=12,
            n_simulations=100
        )   

        self.simulator_subject.monte_carlo_sim.assert_called_once_with(
            initial_price=self.asset_data['Close'].iloc[-1, -1],
            expected_returns=self.expected_returns,
            his_vol=self.asset_his_vol,
            time_horizon=12,
            n_simulations=100
        )

if __name__ == '__main__':
    unittest.main()