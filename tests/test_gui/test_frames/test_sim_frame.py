
import tkinter as tk
import unittest
from unittest.mock import MagicMock, PropertyMock


from monte_carlo_simulator.gui.frames.sim_frame import SimFrame
from monte_carlo_simulator.gui.frames.input_frame import InputFrame
from monte_carlo_simulator.service.simulator_subj import Simulator

class TestSimFrame(unittest.TestCase):

    def setUp(self):
        # Create mock simulator dependency
        self.mock_simulator = MagicMock(spec=Simulator)
        self.mock_simulator.run_backtest = MagicMock(name='run_backtest')
        self.mock_simulator.run_forecast = MagicMock(name='run_forecast')

        # Initialize MainWindow for testing
        self.root = tk.Tk()
        self.app = SimFrame(master=self.root, simulator=self.mock_simulator)
        self.root.withdraw() # Prevent window from showing

        # Initialize basic frames to test grid positioning and hide widget method
        self.button_frame = tk.Frame(master=self.app)
        self.error_frame = tk.Frame(master=self.app)
        self.radio_button_frame = tk.Frame(master=self.app)
        self.assumptions_frame = tk.Frame(master=self.app)
        self.sim_vis_frame = tk.Frame(master=self.app)
        self.backtest_vis_frame = tk.Frame(master=self.app)
        self.input_frame = InputFrame(master=self.app)

        # Set input frame mock properties
        self.input_frame.asset_entry.get = MagicMock(name='get')
        self.input_frame.horizon_spinbox.get = MagicMock(name='get')
        self.input_frame.time_period_combobox.get = MagicMock(name='get')
        self.input_frame.standev_spinbox.get = MagicMock(name='get')
        self.input_frame.n_sim_spinbox.get = MagicMock(name='get')
        self.input_frame.market_combobox.get = MagicMock(name='get')
        self.input_frame.rfr_combobox.get = MagicMock(name='get')

        # Set input frame mock bind methods
        self.input_frame.asset_entry.bind = MagicMock(name='bind')
        self.input_frame.horizon_spinbox.bind = MagicMock(name='bind')
        self.input_frame.time_period_combobox.bind = MagicMock(name='bind')
        self.input_frame.standev_spinbox.bind = MagicMock(name='bind')
        self.input_frame.n_sim_spinbox.bind = MagicMock(name='bind')
        self.input_frame.market_combobox.bind = MagicMock(name='bind')
        self.input_frame.rfr_combobox.bind = MagicMock(name='bind')

        # Set radio frame mock property
        self.radio_button_frame.calc_var = PropertyMock(name='calc_var')

        # Set button frame mock properties
        self.button_frame.sim_button = PropertyMock(name='sim_button')
        self.button_frame.sim_button.on_sim_click = MagicMock(name='on_sim_click')

        # Setup frames on the window for testing
        self.app.setup_frames(
            button_frame = self.button_frame,
            error_frame = self.error_frame,
            radio_button_frame = self.radio_button_frame,
            assumptions_frame = self.assumptions_frame,
            sim_vis_frame = self.sim_vis_frame,
            backtest_vis_frame = self.backtest_vis_frame,
            input_frame = self.input_frame
        )
    
    def tearDown(self):
        self.button_frame.destroy()
        self.error_frame.destroy()
        self.radio_button_frame.destroy()
        self.assumptions_frame.destroy()
        self.sim_vis_frame.destroy()
        self.backtest_vis_frame.destroy()
        self.input_frame.destroy()
        self.app.destroy()
        self.root.destroy()

    def test_setup_frames_asset_vis_frame_grid_position(self):
        self.assertEqual(self.backtest_vis_frame.grid_info()['row'], 0)
        self.assertEqual(self.backtest_vis_frame.grid_info()['column'], 0)

    def test_setup_frames_sim_vis_frame_grid_position(self):
        self.assertEqual(self.sim_vis_frame.grid_info()['row'], 0)
        self.assertEqual(self.sim_vis_frame.grid_info()['column'], 1)

    def test_setup_frames_assumptions_frame_grid_position(self):
        self.assertEqual(self.assumptions_frame.grid_info()['row'], 1)
        self.assertEqual(self.assumptions_frame.grid_info()['column'], 1)

    def test_setup_frames_input_frame_grid_position(self):
        self.assertEqual(self.input_frame.grid_info()['row'], 1)
        self.assertEqual(self.input_frame.grid_info()['column'], 0)

    def test_setup_frames_button_frame_grid_position(self):
        self.assertEqual(self.button_frame.grid_info()['row'], 3)
        self.assertEqual(self.button_frame.grid_info()['column'], 0)

    def test_setup_frames_error_frame_grid_position(self):
        self.assertEqual(self.error_frame.grid_info()['row'], 4)
        self.assertEqual(self.error_frame.grid_info()['column'], 0)

    def test_setup_frames_radio_button_frame_grid_position(self):
        self.assertEqual(self.radio_button_frame.grid_info()['row'], 2)
        self.assertEqual(self.radio_button_frame.grid_info()['column'], 1)

    def test_setup_frames_input_frame_rowspan(self):
        self.assertEqual(self.input_frame.grid_info()['rowspan'], 2)

    def test_setup_frames_button_frame_columnspan(self):
        self.assertEqual(self.button_frame.grid_info()['columnspan'], 2)

    def test_setup_frames_error_frame_columnspan(self):
        self.assertEqual(self.error_frame.grid_info()['columnspan'], 2)


    def test_run_forecast_input_assert_called_once_with(self):
        # Specify get() method return values
        self.input_frame.asset_entry.get.return_value = 'IBM'
        self.input_frame.market_combobox.get.return_value = 'S&P 500'
        self.input_frame.rfr_combobox.get.return_value = '13-week U.S. Treasuries'
        self.input_frame.time_period_combobox.get.return_value = 'Last 5 years'
        self.input_frame.horizon_spinbox.get.return_value = 12
        self.input_frame.n_sim_spinbox.get.return_value = 100
        self.input_frame.standev_spinbox.get.return_value = 30
        self.radio_button_frame.calc_var.get.return_value = 'Capital Asset Pricing Model'

        self.app.run_forecast() # Call method for testing

        self.mock_simulator.run_simulation.assert_called_once_with(
            asset_symbol = 'IBM',
            market_symbol =  '^GSPC', 
            rfr_symbol = '^IRX', 
            period = '5y', 
            n_simulations=100,
            time_horizon = 12,
            exp_ret_flag = 'Capital Asset Pricing Model',
            window = 30
        )

    def test_run_forecast_input_pre_selected_values(self):
        # Specify get() method return values
        self.input_frame.asset_entry.get.return_value = 'IBM'
        self.input_frame.market_combobox.get.return_value = 'S&P 500'
        self.input_frame.rfr_combobox.get.return_value = '13-week U.S. Treasuries'
        self.input_frame.time_period_combobox.get.return_value = 'Last 5 years'
        self.input_frame.horizon_spinbox.get.return_value = 12
        self.input_frame.n_sim_spinbox.get.return_value = 100
        self.input_frame.standev_spinbox.get.return_value = 30
        self.radio_button_frame.calc_var.get.return_value = 'Capital Asset Pricing Model'

        self.app.run_forecast() # Call method for testing

        self.mock_simulator.run_simulation.assert_called_once_with(
            asset_symbol = 'IBM',
            market_symbol =  '^GSPC', 
            rfr_symbol = '^IRX', 
            period = '5y', 
            n_simulations=100,
            time_horizon = 12,
            exp_ret_flag = 'Capital Asset Pricing Model',
            window = 30
        )

    def test_run_forecast_input_user_chosen_values(self):
        # Specify get() method return values
        self.input_frame.asset_entry.get.return_value = 'IBM'
        self.input_frame.market_combobox.get.return_value = '^ABCD' # Field can contain user-entered values or chosen from drop-down menu
        self.input_frame.rfr_combobox.get.return_value = '^BOND' # Field can contain user-entered values or chosen from drop-down menu
        self.input_frame.time_period_combobox.get.return_value = 'Last 5 years'
        self.input_frame.horizon_spinbox.get.return_value = 12
        self.input_frame.n_sim_spinbox.get.return_value = 100
        self.input_frame.standev_spinbox.get.return_value = 30
        self.radio_button_frame.calc_var.get.return_value = 'Capital Asset Pricing Model'

        self.app.run_forecast() # Call method for testing

        self.mock_simulator.run_simulation.assert_called_once_with(
            asset_symbol = 'IBM',
            market_symbol =  '^ABCD',
            rfr_symbol = '^BOND',
            period = '5y',
            n_simulations=100,
            time_horizon = 12,
            exp_ret_flag = 'Capital Asset Pricing Model',
            window = 30
        )

    def test_run_backtest_sim_input_assert_called_once_with(self):
        # Specify get() method return values
        self.input_frame.asset_entry.get.return_value = 'IBM'
        self.input_frame.market_combobox.get.return_value = 'S&P 500'
        self.input_frame.rfr_combobox.get.return_value = '13-week U.S. Treasuries'
        self.input_frame.time_period_combobox.get.return_value = 'Last 5 years'
        self.input_frame.horizon_spinbox.get.return_value = 12
        self.input_frame.n_sim_spinbox.get.return_value = 100
        self.input_frame.standev_spinbox.get.return_value = 30
        self.radio_button_frame.calc_var.get.return_value = 'Capital Asset Pricing Model'

        self.app.run_backtest_sim() # Call method for testing

        self.mock_simulator.run_backtest_split.assert_called_once_with(
            asset_symbol = 'IBM',
            market_symbol =  '^GSPC', 
            rfr_symbol = '^IRX', 
            period = '5y', 
            n_simulations=100,
            time_horizon = 12,
            exp_ret_flag = 'Capital Asset Pricing Model',
            window = 30
        )

    def test_run_backtest_sim_input_pre_selected_values(self):
        # Specify get() method return values
        self.input_frame.asset_entry.get.return_value = 'IBM'
        self.input_frame.market_combobox.get.return_value = 'S&P 500'
        self.input_frame.rfr_combobox.get.return_value = '13-week U.S. Treasuries'
        self.input_frame.time_period_combobox.get.return_value = 'Last 5 years'
        self.input_frame.horizon_spinbox.get.return_value = 12
        self.input_frame.n_sim_spinbox.get.return_value = 100
        self.input_frame.standev_spinbox.get.return_value = 30
        self.radio_button_frame.calc_var.get.return_value = 'Capital Asset Pricing Model'

        self.app.run_backtest_sim() # Call method for testing

        self.mock_simulator.run_backtest_split.assert_called_once_with(
            asset_symbol = 'IBM',
            market_symbol =  '^GSPC', 
            rfr_symbol = '^IRX', 
            period = '5y', 
            n_simulations=100,
            time_horizon = 12,
            exp_ret_flag = 'Capital Asset Pricing Model',
            window = 30
        )

    def test_run_backtest_sim_input_user_chosen_values(self):
        # Specify get() method return values
        self.input_frame.asset_entry.get.return_value = 'IBM'
        self.input_frame.market_combobox.get.return_value = '^ABCD' # Field can contain user-entered values or chosen from drop-down menu
        self.input_frame.rfr_combobox.get.return_value = '^BOND' # Field can contain user-entered values or chosen from drop-down menu
        self.input_frame.time_period_combobox.get.return_value = 'Last 5 years'
        self.input_frame.horizon_spinbox.get.return_value = 12
        self.input_frame.n_sim_spinbox.get.return_value = 100
        self.input_frame.standev_spinbox.get.return_value = 30
        self.radio_button_frame.calc_var.get.return_value = 'Capital Asset Pricing Model'

        self.app.run_backtest_sim() # Call method for testing

        self.mock_simulator.run_backtest_split.assert_called_once_with(
            asset_symbol = 'IBM',
            market_symbol =  '^ABCD',
            rfr_symbol = '^BOND',
            period = '5y',
            n_simulations=100,
            time_horizon = 12,
            exp_ret_flag = 'Capital Asset Pricing Model',
            window = 30
        )

    # Test hide_input
    def test_hide_input_capm_rfr_label(self):
        # Explicitly call hide input method to test functionality
        self.app.hide_input(selected_value='Capital Asset Pricing Model')

        # Check grid position of risk-free rate and market index inputs
        self.assertEqual(self.input_frame.rfr_security_label.grid_info()['row'], 6)
        self.assertEqual(self.input_frame.rfr_security_label.grid_info()['column'], 0)

    def test_hide_input_capm_rfr_combobox(self):
        # Explicitly call hide input method to test functionality
        self.app.hide_input(selected_value='Capital Asset Pricing Model')

        # Check grid position of risk-free rate and market index inputs
        self.assertEqual(self.input_frame.rfr_combobox.grid_info()['row'], 6)
        self.assertEqual(self.input_frame.rfr_combobox.grid_info()['column'], 1)

    def test_hide_input_capm_market_index_label(self):
        # Explicitly call hide input method to test functionality
        self.app.hide_input(selected_value='Capital Asset Pricing Model')

        # Check grid position of risk-free rate and market index inputs
        self.assertEqual(self.input_frame.market_index_label.grid_info()['row'], 7)
        self.assertEqual(self.input_frame.market_index_label.grid_info()['column'], 0)

    def test_hide_input_capm_market_combobox(self):
        # Explicitly call hide input method to test functionality
        self.app.hide_input(selected_value='Capital Asset Pricing Model')

        # Check grid position of risk-free rate and market index inputs
        self.assertEqual(self.input_frame.market_combobox.grid_info()['row'], 7)
        self.assertEqual(self.input_frame.market_combobox.grid_info()['column'], 1)

    def test_hide_input_ddm_rfr_label(self):
        # Explicitly call hide input method to test functionality
        self.app.hide_input(selected_value='Dividend Discount Model')

        # Check grid position of risk-free rate and market index inputs
        # grid_info should return an empty dictionary when widgets are hidden
        self.assertEqual(self.input_frame.rfr_security_label.grid_info(), {})
        self.assertEqual(self.input_frame.rfr_security_label.grid_info(), {})

    def test_hide_input_ddm_rfr_combobox(self):
        # Explicitly call hide input method to test functionality
        self.app.hide_input(selected_value='Dividend Discount Model')

        # Check grid position of risk-free rate and market index inputs
        # grid_info should return an empty dictionary when widgets are hidden
        self.assertEqual(self.input_frame.rfr_combobox.grid_info(), {})
        self.assertEqual(self.input_frame.rfr_combobox.grid_info(), {})

    def test_hide_input_ddm_market_index_label(self):
        # Explicitly call hide input method to test functionality
        self.app.hide_input(selected_value='Dividend Discount Model')

        # Check grid position of risk-free rate and market index inputs
        # grid_info should return an empty dictionary when widgets are hidden
        self.assertEqual(self.input_frame.market_index_label.grid_info(), {})
        self.assertEqual(self.input_frame.market_index_label.grid_info(), {})

    def test_hide_input_ddm_market_combobox(self):
        # Explicitly call hide input method to test functionality
        self.app.hide_input(selected_value='Dividend Discount Model')

        # Check grid position of risk-free rate and market index inputs
        # grid_info should return an empty dictionary when widgets are hidden
        self.assertEqual(self.input_frame.market_combobox.grid_info(), {})
        self.assertEqual(self.input_frame.market_combobox.grid_info(), {})

    def test_process_market_input_valid_key(self):
        # Set market combobox return value as an existing market index key
        self.input_frame.market_combobox.get.return_value = 'S&P 500'

        # Explicitly call function, save result
        result = self.app._process_market_input()

        # result should equal value corresponding to key
        self.assertEqual(result, '^GSPC')

    def test_process_market_input_user_generated_value(self):
        # Set market combobox return value as an existing market index key
        self.input_frame.market_combobox.get.return_value = '12345'

        # Explicitly call function, save result
        result = self.app._process_market_input()

        # result should equal user generated value
        self.assertEqual(result, '12345')


    def test_process_rfr_input_valid_key(self):
        # Set market combobox return value as an existing market index key
        self.input_frame.rfr_combobox.get.return_value = '13-week U.S. Treasuries'

        # Explicitly call function, save result
        result = self.app._process_rfr_input()

        # result should equal value corresponding to key
        self.assertEqual(result, '^IRX')

    def test_process_rfr_input_user_generated_value(self):
        # Set market combobox return value as an existing market index key
        self.input_frame.rfr_combobox.get.return_value = 'Twinkies'

        # Explicitly call function, save result
        result = self.app._process_rfr_input()

        # result should equal user generated value
        self.assertEqual(result, 'Twinkies')


if __name__ == '__main__':
    unittest.main()