
import unittest
from unittest.mock import MagicMock
import tkinter as tk

from monte_carlo_simulator.gui.frames.input_frame import InputFrame
from monte_carlo_simulator.gui.frames.sim_frame import SimFrame
from monte_carlo_simulator.service.simulator_subj import Simulator

class TestinputFrame(unittest.TestCase):

    def setUp(self):
        # Create mock simulator dependency
        self.mock_simulator = MagicMock(spec=Simulator)

        # Initialize test main window
        self.root = tk.Tk()
        self.app = SimFrame(master=self.root, simulator=self.mock_simulator)
        self.root.withdraw() # Prevent main window from showing

        # Initalize test input frame frame 
        self.input_frame = InputFrame(master=self.app)


    def tearDown(self):
        # Dispose of gui elements after tests
        self.input_frame.destroy()
        self.app.destroy()
        self.root.destroy()

    # Test create_simulation_input
    def test_create_simulation_input_asset_entry_default_value(self):
        self.assertEqual(self.input_frame.asset_entry.get(), 'IBM')

    def test_create_simulation_input_horizon_entry_default_value(self):
        self.assertEqual(self.input_frame.horizon_spinbox.get(), '12')

    def test_create_simulation_input_time_period_default_value(self):
        self.assertEqual(self.input_frame.time_period_combobox.get(), 'Last 1 year')

    def test_create_simulation_input_standev_default_value(self):
        self.assertEqual(self.input_frame.standev_spinbox.get(), '365')

    def test_create_simulation_input_standev_default_value(self):
        self.assertEqual(self.input_frame.n_sim_spinbox.get(), '1000')

    def test_create_simulation_input_asset_entry_grid_position(self):  
        self.assertEqual(self.input_frame.asset_entry.grid_info()['row'], 1)
        self.assertEqual(self.input_frame.asset_entry.grid_info()['column'], 1)

    def test_create_simulation_input_horizon_entry_grid_position(self):
        self.assertEqual(self.input_frame.horizon_spinbox.grid_info()['row'], 2)
        self.assertEqual(self.input_frame.horizon_spinbox.grid_info()['column'], 1)

    def test_create_simulation_input_time_combobox_grid_position(self):
        self.assertEqual(self.input_frame.time_period_combobox.grid_info()['row'], 3)
        self.assertEqual(self.input_frame.time_period_combobox.grid_info()['column'], 1)

    def test_create_simulation_input_standev_spinbox_grid_position(self):
        self.assertEqual(self.input_frame.standev_spinbox.grid_info()['row'], 4)
        self.assertEqual(self.input_frame.standev_spinbox.grid_info()['column'], 1)

    def test_create_simulation_input_n_sim_spinbox_grid_position(self):
        self.assertEqual(self.input_frame.n_sim_spinbox.grid_info()['row'], 5)
        self.assertEqual(self.input_frame.n_sim_spinbox.grid_info()['column'], 1)


    # Test create_rfr_input
    def test_create_rfr_input_rfr_combobox_default_value(self):
        self.assertEqual(self.input_frame.rfr_combobox.get(), '13-week U.S. Treasuries')

    def test_create_rfr_input_rfr_combobox_grid_position(self):
        self.assertEqual(self.input_frame.rfr_combobox.grid_info()['row'], 6)
        self.assertEqual(self.input_frame.rfr_combobox.grid_info()['column'], 1)

    # Test create_market_input
    def test_create_market_input_market_combobox_default_value(self):
        self.assertEqual(self.input_frame.market_combobox.get(), 'S&P 500')

    def test_create_market_input_market_combobox_grid_position(self):
        self.assertEqual(self.input_frame.market_combobox.grid_info()['row'], 7)
        self.assertEqual(self.input_frame.market_combobox.grid_info()['column'], 1)

    # Test create_entry_labels
    def test_create_entry_labels_asset_entry_label_text(self):
        self.assertEqual(self.input_frame.asset_entry_label.cget('text'), 'Enter asset ticker symbol:')

    def test_create_entry_labels_horizon_entry_label_text(self):
        self.assertEqual(self.input_frame.horizon_entry_label.cget('text'), 'Enter your investment time horizon (in days):')

    def test_create_entry_labels_time_period_label_text(self):
        self.assertEqual(self.input_frame.time_period_label.cget('text'), 'Enter the timeframe to use in calculations:')

    def test_create_entry_labels_standev_label_text(self):
        self.assertEqual(self.input_frame.standev_label.cget('text'), 'Enter current volatility timeframe (in days):')

    def test_create_entry_labels_n_sim_label_text(self):
        self.assertEqual(self.input_frame.n_sim_label.cget('text'), 'Enter the number of simulations you would like to run:')

    def test_create_entry_labels_rfr_security_label_text(self):
        self.assertEqual(self.input_frame.rfr_security_label.cget('text'), 'Select the security to use for risk-free rate calculations:')
    
    def test_create_entry_labels_market_index_label_text(self):
        self.assertEqual(self.input_frame.market_index_label.cget('text'), 'Select the index to use in calculations:')

    def test_create_entry_labels_asset_entry_label_grid_position(self):
        self.assertEqual(self.input_frame.asset_entry_label.grid_info()['row'], 1)
        self.assertEqual(self.input_frame.asset_entry_label.grid_info()['column'], 0)

    def test_create_entry_labels_horizon_entry_label_grid_position(self):
        self.assertEqual(self.input_frame.horizon_entry_label.grid_info()['row'], 2)
        self.assertEqual(self.input_frame.horizon_entry_label.grid_info()['column'], 0)

    def test_create_entry_labels_time_period_label_grid_position(self):
        self.assertEqual(self.input_frame.time_period_label.grid_info()['row'], 3)
        self.assertEqual(self.input_frame.time_period_label.grid_info()['column'], 0)

    def test_create_entry_labels_standev_label_grid_position(self):
        self.assertEqual(self.input_frame.standev_label.grid_info()['row'], 4)
        self.assertEqual(self.input_frame.standev_label.grid_info()['column'], 0)

    def test_create_entry_labels_n_sim_label_grid_position(self):  
        self.assertEqual(self.input_frame.n_sim_label.grid_info()['row'], 5)
        self.assertEqual(self.input_frame.n_sim_label.grid_info()['column'], 0)

    def test_create_entry_labels_rfr_security_label_grid_position(self):
        self.assertEqual(self.input_frame.rfr_security_label.grid_info()['row'], 6)
        self.assertEqual(self.input_frame.rfr_security_label.grid_info()['column'], 0)

    def test_create_entry_labels_market_index_label_grid_position(self):
        self.assertEqual(self.input_frame.market_index_label.grid_info()['row'], 7)
        self.assertEqual(self.input_frame.market_index_label.grid_info()['column'], 0)


if __name__ == '__main__':
    unittest.main()