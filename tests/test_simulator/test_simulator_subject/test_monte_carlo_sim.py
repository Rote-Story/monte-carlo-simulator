

import unittest
from unittest.mock import Mock
import pandas as pd
import numpy as np

from monte_carlo_simulator.const import ANNUAL_TRADING_DAYS
from monte_carlo_simulator.data_fetcher.market_data_fetcher import MarketDataFetcher
from monte_carlo_simulator.gui.inter.observer_inter import Observer
from monte_carlo_simulator.model.market_index import MarketIndex
from monte_carlo_simulator.model.risk_free_security import RiskFreeSecurity
from monte_carlo_simulator.model.stock import Stock
from monte_carlo_simulator.service.simulator_subj import Simulator


class TestMonteCarloSimulator(unittest.TestCase):

    # Setup function input variables corresponding to test data
    initial_price = 182.96
    beta = 0.6741
    market_returns = 0.17
    risk_free_rate = 0.4
    his_vol = 0.1842
    capm_returns = 0.09

    def setUp(self):
        # Create mock dependencies for Simulator
        self.mock_data_fetcher = Mock(spec=MarketDataFetcher)
        self.mock_stock = Mock(spec=Stock)
        self.mock_market_index = Mock(spec=MarketIndex)
        self.mock_risk_free_sec = Mock(spec=RiskFreeSecurity)

        # Create mock observers to test subject/observer methods
        self.mock_observer = Mock(spec=Observer)
        
        # Create a new "blank" simulator_subject for each test
        self.simulator = Simulator(
            market_data_fetcher=self.mock_data_fetcher, 
            financial_asset=self.mock_stock,
            market_index=self.mock_market_index, 
            risk_free_sec=self.mock_risk_free_sec
            )

    def test_monte_carlo_sim_return_type(self):
        result = self.simulator.monte_carlo_sim(
            initial_price=self.initial_price,
            expected_returns=self.capm_returns,
            his_vol=self.his_vol,
            time_horizon=12,
            n_simulations=100
        )

        self.assertIsInstance(result, np.ndarray)

    def test_monte_carlo_sim_array_shape(self):
        result = self.simulator.monte_carlo_sim(
            initial_price=self.initial_price,
            expected_returns=self.capm_returns,
            his_vol=self.his_vol,
            time_horizon=12,
            n_simulations=100
        )

        self.assertEqual(result.shape, (ANNUAL_TRADING_DAYS, 100))

    def test_monte_carlo_sim_array_size(self):
        result = self.simulator.monte_carlo_sim(
            initial_price=self.initial_price,
            expected_returns=self.capm_returns,
            his_vol=self.his_vol,
            time_horizon=12,
            n_simulations=100
        )

        self.assertEqual(result.size, (ANNUAL_TRADING_DAYS * 100))


    def test_monte_carlo_sim_array_is_not_none(self):
        result = self.simulator.monte_carlo_sim(
            initial_price=self.initial_price,
            expected_returns=self.capm_returns,
            his_vol=self.his_vol,
            time_horizon=12,
            n_simulations=100
        )

        self.assertIsNotNone(result)

    def test_monte_carlo_sim_array_elements_not_none(self):
        result = self.simulator.monte_carlo_sim(
            initial_price=self.initial_price,
            expected_returns=self.capm_returns,
            his_vol=self.his_vol,
            time_horizon=12,
            n_simulations=100
        )
        none_check = 1
        for outer_elem in result:
            for inner_elem in outer_elem:
                if inner_elem == None:
                    none_check = None

        self.assertIsNotNone(none_check)

    def test_monte_carlo_sim_initial_price_type_error(self):
        with self.assertRaises(TypeError) as e:
            self.simulator.monte_carlo_sim(
                initial_price=None,
                expected_returns=self.capm_returns,
                his_vol=self.his_vol,
                time_horizon=12,
                n_simulations=100
            )
            self.assertRegex(str(e), r'"initial_price" must be a number, not \.*')

    def test_monte_carlo_sim_expected_returns_type_error(self):
        with self.assertRaises(TypeError) as e:
            self.simulator.monte_carlo_sim(
                initial_price=self.initial_price,
                expected_returns="0.15",
                his_vol=self.his_vol,
                time_horizon=12,
                n_simulations=100
            )
            self.assertRegex(str(e), r'"expected_returns" must be a number, not \.*')

    def test_monte_carlo_sim_his_vol_type_error(self):
        with self.assertRaises(TypeError) as e:
            self.simulator.monte_carlo_sim(
                initial_price=self.initial_price,
                expected_returns=self.capm_returns,
                his_vol="0.50",
                time_horizon=12,
                n_simulations=100
            )
            self.assertRegex(str(e), r'"his_vol" must be a number, not \.*')

    def test_monte_carlo_sim_his_vol_zero_input(self):
            result = self.simulator.monte_carlo_sim(
                initial_price=self.initial_price,
                expected_returns=self.capm_returns,
                his_vol=0,
                time_horizon=12,
                n_simulations=100
            )
            self.assertIsNotNone(result)

    def test_monte_carlo_sim_his_vol_value_error_negative_input(self):
        with self.assertRaises(ValueError) as e:
            self.simulator.monte_carlo_sim(
                initial_price=self.initial_price,
                expected_returns=self.capm_returns,
                his_vol=-1,
                time_horizon=12,
                n_simulations=100
            )
            self.assertRegex(str(e), r'"his_vol" must be positive, not \.*')

    def test_monte_carlo_sim_time_horizon_type_error(self):
        with self.assertRaises(TypeError) as e:
            self.simulator.monte_carlo_sim(
                initial_price=self.initial_price,
                expected_returns=self.capm_returns,
                his_vol=self.his_vol,
                time_horizon="90",
                n_simulations=100
            )
            self.assertRegex(str(e), r'"time_horizon" must be a positive number, not \.*')

    def test_monte_carlo_sim_time_horizon_value_error_zero_input(self):
        with self.assertRaises(ValueError) as e:
            self.simulator.monte_carlo_sim(
                initial_price=self.initial_price,
                expected_returns=self.capm_returns,
                his_vol=self.his_vol,
                time_horizon=0,
                n_simulations=100
            )
            self.assertRegex(str(e), r'"time_horizon" must be greater than zero, not \.*')

    def test_monte_carlo_sim_time_horizon_negative_value(self):
        with self.assertRaises(ValueError) as e:
            self.simulator.monte_carlo_sim(
                initial_price=self.initial_price,
                expected_returns=self.capm_returns,
                his_vol=self.his_vol,
                time_horizon=-90,
                n_simulations=100
            )
            self.assertRegex(str(e), r'"time_horizon" must be greater than zero, not \.*')

    def test_monte_carlo_sim_n_simulations_type_error(self):
        with self.assertRaises(TypeError) as e:
            self.simulator.monte_carlo_sim(
                initial_price=self.initial_price,
                expected_returns=self.capm_returns,
                his_vol=self.his_vol,
                time_horizon=12,
                n_simulations=None
            )
            self.assertRegex(str(e), r'"n_simulations" must be a positive number, not \.*')

    def test_monte_carlo_sim_n_simulations_value_error_zero_input(self):
        with self.assertRaises(ValueError) as e:
            self.simulator.monte_carlo_sim(
                initial_price=self.initial_price,
                expected_returns=self.capm_returns,
                his_vol=self.his_vol,
                time_horizon=12,
                n_simulations=0
            )
            self.assertRegex(str(e), r'"n_simulations" must be a number greater than zero, not \.*')

    def test_monte_carlo_sim_n_simulations_value_error_negative_input(self):
        with self.assertRaises(ValueError) as e:
            self.simulator.monte_carlo_sim(
                initial_price=self.initial_price,
                expected_returns=self.capm_returns,
                his_vol=self.his_vol,
                time_horizon=12,
                n_simulations=-1
            )
            self.assertRegex(str(e), r'"n_simulations" must be a number greater than zero, not \.*')

    def test_monte_carlo_sim_size(self):
        result = self.simulator.monte_carlo_sim(
            initial_price=self.initial_price,
            expected_returns=self.capm_returns,
            his_vol=self.his_vol,
            time_horizon=12,
            n_simulations=100
        )
        # Returned array should have a size equal to the number of simulationd multiplied by the time horizon 
        # converted to trading days: There are 252 trading days in each year. 
        self.assertEqual(result.size, 100*ANNUAL_TRADING_DAYS)

if __name__ == '__main__':
    unittest.main()