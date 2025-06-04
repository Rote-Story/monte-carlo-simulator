
import unittest
from unittest.mock import MagicMock, PropertyMock
import tkinter as tk

from monte_carlo_simulator.gui.frames.assumptions_frame_obs import AssumptionsFrame
from monte_carlo_simulator.gui.frames.sim_frame import SimFrame
from monte_carlo_simulator.model.financial_asset import FinancialAsset
from monte_carlo_simulator.model.market_index import MarketIndex
from monte_carlo_simulator.model.risk_free_security import RiskFreeSecurity
from monte_carlo_simulator.service.simulator_subj import Simulator

class TestAssumptionsFrame(unittest.TestCase):

    def setUp(self):
        # # Create mock simulator dependency
        self.mock_simulator = MagicMock(spec=Simulator)

        # Create mock simulator subject data model return values
        # Create mock financial asset and return values
        self.mock_financial_asset = MagicMock(spec=FinancialAsset)
        type(self.mock_simulator).financial_asset = PropertyMock(return_value=self.mock_financial_asset)
        type(self.mock_financial_asset).asset_symbol = PropertyMock(return_value='AAPL')
        type(self.mock_financial_asset).his_vol = PropertyMock(return_value=0.04)
        type(self.mock_financial_asset).expected_returns = PropertyMock(return_value=0.09)
        type(self.mock_financial_asset).beta = PropertyMock(return_value=0.61)
        type(self.mock_financial_asset).div_growth_rate = PropertyMock(return_value=0.01)
        
        # Create mock market index and return values
        self.mock_market_index = MagicMock(spec=MarketIndex)
        type(self.mock_simulator).market_index = PropertyMock(return_value=self.mock_market_index)
        type(self.mock_market_index).market_returns = PropertyMock(return_value=0.17)

        # Create mock risk-free security and return values
        self.mock_risk_free_sec = MagicMock(spec=RiskFreeSecurity)
        type(self.mock_simulator).risk_free_sec = PropertyMock(return_value=self.mock_risk_free_sec)
        type(self.mock_risk_free_sec).rfr_symbol = PropertyMock(return_value='^IRX')
        type(self.mock_risk_free_sec).risk_free_rate = PropertyMock(return_value=0.03)

        # Initialize test main window
        self.root = tk.Tk()
        self.app = SimFrame(master=self.root, simulator=self.mock_simulator)
        self.root.withdraw() # Prevent main window from showing

        # Initalize test assumptions frame 
        self.assumptions_frame = AssumptionsFrame(master=self.app)

        # Setup assumptions labels for testing
        self.assumptions_frame.create_assumptions()

    def tearDown(self):
        self.assumptions_frame.destroy()
        self.app.destroy()
        self.root.destroy()

    def test_create_assumptions_beta_label_grid_position(self):
        self.assertEqual(self.assumptions_frame.beta_label.grid_info()['row'], 0)
        self.assertEqual(self.assumptions_frame.beta_label.grid_info()['column'], 0)

    def test_create_assumptions_volatility_label_grid_position(self):
        self.assertEqual(self.assumptions_frame.volatility_label.grid_info()['row'], 1)
        self.assertEqual(self.assumptions_frame.volatility_label.grid_info()['column'], 0)

    def test_create_assumptions_rfr_label_position(self):
        self.assertEqual(self.assumptions_frame.rfr_label.grid_info()['row'], 0)
        self.assertEqual(self.assumptions_frame.rfr_label.grid_info()['column'], 1)

    def test_create_assumptions_market_returns_grid_position(self):
        self.assertEqual(self.assumptions_frame.market_returns_label.grid_info()['row'], 1)
        self.assertEqual(self.assumptions_frame.market_returns_label.grid_info()['column'], 1)

    def test_create_assumptions_expected_returns_grid_position(self):
        self.assertEqual(self.assumptions_frame.expected_returns_label.grid_info()['row'], 2)
        self.assertEqual(self.assumptions_frame.expected_returns_label.grid_info()['column'], 0)

    def test_create_assumptions_div_growth_label_grid_position(self):
        self.assertEqual(self.assumptions_frame.div_growth_label.grid_info()['row'], 2)
        self.assertEqual(self.assumptions_frame.div_growth_label.grid_info()['column'], 1)

    def test_update_volatility_label_text(self):
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Verify labels match subject return values
        self.assertEqual(
            self.assumptions_frame.volatility_label.cget('text'), 
            'AAPL\'s volatility:  0.0400'
            )

    def test_update_expected_returns_label_text(self):
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Verify labels match subject return values
        self.assertEqual(
            self.assumptions_frame.expected_returns_label.cget('text'), 
            'AAPL\'s expected returns:  9.0000%'
            )
    
    def test_update_div_growth_label_text(self):
        # Set return values to enter 'Dividend Discount Model' case in update() method
        type(self.mock_financial_asset).exp_ret_flag = PropertyMock(return_value='Dividend Discount Model')

        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Verify labels match subject return values
        self.assertEqual(
            self.assumptions_frame.div_growth_label.cget('text'), 
            'AAPL\'s historic dividend growth rate:  1.0000%'
            )
        
    def test_update_market_returns_label_text(self):
        # Set return values to enter 'Capital Asset Pricing Model' case in update() method
        type(self.mock_financial_asset).exp_ret_flag = PropertyMock(return_value='Capital Asset Pricing Model')
        
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Verify labels match subject return values
        self.assertEqual(
            self.assumptions_frame.market_returns_label.cget('text'), 
            'Market returns:  17.0000%'
            )

    def test_update_rfr_label_text(self):
        # Set return values to enter 'Capital Asset Pricing Model' case in update() method
        type(self.mock_financial_asset).exp_ret_flag = PropertyMock(return_value='Capital Asset Pricing Model')
        
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Verify labels match subject return values
        self.assertEqual(
            self.assumptions_frame.rfr_label.cget('text'), 
            '^IRX historic returns:  3.0000%'
            )

    def test_update_beta_label_text(self):
        # Set return values to enter CAPM case in update() method
        type(self.mock_financial_asset).exp_ret_flag = PropertyMock(return_value='Capital Asset Pricing Model')
        
        # Set dividend growth rate return value
        type(self.mock_financial_asset).beta = PropertyMock(return_value=0.67)

        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Verify labels match subject return values
        self.assertEqual(
            self.assumptions_frame.beta_label.cget('text'), 
            'AAPL\'s beta:  0.6700'
            )
        
    def test_update_simple_avg_irrelevant_output_empty(self):
        # Set return values to enter 'Simple Average Returns' case in update() method
        type(self.mock_financial_asset).exp_ret_flag = PropertyMock(return_value='Simple Average Returns')
        
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Verify labels match subject return values
        self.assertEqual(self.assumptions_frame.beta_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.div_growth_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.market_returns_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.rfr_label.cget('text'), '')

    def test_update_simple_avg_irrelevant_output_cleared_capm(self):
        # Set return values to enter 'Capital Asset Pricing Model' case in update() method
        type(self.mock_financial_asset).exp_ret_flag = PropertyMock(return_value='Capital Asset Pricing Model')
        
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Set return values to enter 'Simple Average Returns' case in update() method
        type(self.mock_financial_asset).exp_ret_flag = PropertyMock(return_value='Simple Average Returns')
        
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Verify labels match subject return values
        self.assertEqual(self.assumptions_frame.beta_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.div_growth_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.market_returns_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.rfr_label.cget('text'), '')

    def test_update_simple_avg_irrelevant_output_cleared_ddm(self):
        # Set return values to enter 'Dividend Discount Model' case in update() method
        type(self.mock_financial_asset).exp_ret_flag = PropertyMock(return_value='Dividend Discount Model')
        
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Set return values to enter 'Simple Average Returns' case in update() method
        type(self.mock_financial_asset).exp_ret_flag = PropertyMock(return_value='Simple Average Returns')
        
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Verify labels match subject return values
        self.assertEqual(self.assumptions_frame.beta_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.div_growth_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.market_returns_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.rfr_label.cget('text'), '')

    def test_update_exponential_weighted_avg_irrelevant_output_empty(self):
        # Set return values to enter 'Exponential Weighted Average Returns' case in update() method
        type(self.mock_financial_asset).exp_ret_flag = PropertyMock(return_value='Exponential Weighted Average Returns')
        
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Verify labels match subject return values
        self.assertEqual(self.assumptions_frame.beta_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.div_growth_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.market_returns_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.rfr_label.cget('text'), '')

    def test_update_exponential_weighted_avg_irrelevant_output_cleared_capm(self):
        # Set return values to enter 'Capital Asset Pricing Model' case in update() method
        type(self.mock_financial_asset).exp_ret_flag = PropertyMock(return_value='Capital Asset Pricing Model')
        
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Set return values to enter 'Exponential Weighted Average Returns' case in update() method
        type(self.mock_financial_asset).exp_ret_flag = PropertyMock(return_value='Exponential Weighted Average Returns')
        
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Verify labels match subject return values
        self.assertEqual(self.assumptions_frame.beta_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.div_growth_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.market_returns_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.rfr_label.cget('text'), '')
    
    def test_update_exponential_weighted_avg_irrelevant_output_cleared_capm(self):
        # Set return values to enter 'Dividend Discount Model' case in update() method
        type(self.mock_financial_asset).exp_ret_flag = PropertyMock(return_value='Dividend Discount Model')
        
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Set return values to enter 'Exponential Weighted Average Returns' case in update() method
        type(self.mock_financial_asset).exp_ret_flag = PropertyMock(return_value='Exponential Weighted Average Returns')
        
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Verify labels match subject return values
        self.assertEqual(self.assumptions_frame.beta_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.div_growth_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.market_returns_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.rfr_label.cget('text'), '')

    def test_update_missing_expected_returns(self):
        # Set return values to enter 'Dividend Discount Model' case in update() method
        type(self.mock_financial_asset).expected_returns = PropertyMock(return_value=None)
        
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Verify that no labels have been set
        self.assertEqual(self.assumptions_frame.volatility_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.expected_returns_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.beta_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.div_growth_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.market_returns_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.rfr_label.cget('text'), '')

    def test_update_missing_his_vol(self):
        # Set return values to enter 'Dividend Discount Model' case in update() method
        type(self.mock_financial_asset).his_vol = PropertyMock(return_value=None)
        
        # Call update() to set labels
        self.assumptions_frame.update(self.mock_simulator)
        
        # Verify that no labels have been set
        self.assertEqual(self.assumptions_frame.volatility_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.expected_returns_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.beta_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.div_growth_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.market_returns_label.cget('text'), '')
        self.assertEqual(self.assumptions_frame.rfr_label.cget('text'), '')


if __name__ == '__main__':
    unittest.main()