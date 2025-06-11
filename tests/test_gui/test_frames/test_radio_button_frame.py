
import tkinter as tk
import unittest
from unittest.mock import MagicMock

from monte_carlo_simulator.gui.frames.radio_button_frame import RadioButtonFrame
from monte_carlo_simulator.gui.frames.sim_frame import SimFrame
from monte_carlo_simulator.service.simulator_subj import Simulator

class TestRadioButtonFrame(unittest.TestCase):

    def setUp(self):
        # Create mock simulator dependency
        self.mock_simulator = MagicMock(spec=Simulator)

        # Initialize test main window, replace test methods with mocks
        self.root = tk.Tk()
        self.app = SimFrame(master=self.root, simulator=self.mock_simulator)
        self.root.withdraw() # Prevent window from being shown

        # Initialize radio button frame
        self.rad_button_frame = RadioButtonFrame(self.app)

    def tearDown(self):
        self.rad_button_frame.destroy()
        self.app.destroy()
        self.root.destroy()

    def test_create_rbutton_labels_capm_label_text(self):
        self.assertEqual(
            self.rad_button_frame.capm_label.cget('text'), 
            'risk-free rate + beta * (expected market returns - risk-free rate)'
            )

    def test_create_rbutton_labels_ddm_label_text(self):
        self.assertEqual(
            self.rad_button_frame.ddm_label.cget('text'), 
            '(expected dividend / current price) + expected dividend growth rate'
            )

    def test_create_rbutton_labels_simple_avg_label_text(self):
        self.assertEqual(
            self.rad_button_frame.simple_avg_label.cget('text'), 
            'Calculates the unweighted average for the selected average window period'
            )

    def test_create_rbutton_labels_weighted_avg_label_text(self):
        self.assertEqual(
            self.rad_button_frame.weighted_avg_label.cget('text'), 
            'Calculates average weighted to value more recent observations higher'
            )
    
    def test_create_rbutton_labels_capm_label_grid_position(self):
        self.assertEqual(self.rad_button_frame.capm_label.grid_info()['row'], 1)
        self.assertEqual(self.rad_button_frame.capm_label.grid_info()['column'], 1)

    def test_create_rbutton_labels_ddm_label_grid_position(self):
        self.assertEqual(self.rad_button_frame.ddm_label.grid_info()['row'], 2)
        self.assertEqual(self.rad_button_frame.ddm_label.grid_info()['column'], 1)

    def test_create_rbutton_labels_simple_avg_label_grid_position(self):
        self.assertEqual(self.rad_button_frame.simple_avg_label.grid_info()['row'], 4)
        self.assertEqual(self.rad_button_frame.simple_avg_label.grid_info()['column'], 1)

    def test_create_rbutton_labels_weighted_avg_label_grid_position(self):
        self.assertEqual(self.rad_button_frame.weighted_avg_label.grid_info()['row'], 5)
        self.assertEqual(self.rad_button_frame.weighted_avg_label.grid_info()['column'], 1)

    # Test create_rad_buttons
    def test_create_rad_buttons_capm_button_text(self):
        self.assertEqual(self.rad_button_frame.capm_button.cget('text'), 'Capital Asset Pricing Model')

    def test_create_rad_buttons_ddm_button_text(self):
        self.assertEqual(self.rad_button_frame.ddm_button.cget('text'), 'Dividend Discount Model')
    
    def test_create_rad_buttons_simple_avg_button_text(self):
        self.assertEqual(self.rad_button_frame.simple_avg_button.cget('text'), 'Simple Average Returns')
    
    def test_create_rad_buttons_weighted_avg_button_text(self):
        self.assertEqual(self.rad_button_frame.weighted_avg_button.cget('text'), 'Exponential Weighted Average Returns')

    def test_create_rbutton_buttons_capm_button_grid_position(self):
        self.assertEqual(self.rad_button_frame.capm_button.grid_info()['row'], 1)
        self.assertEqual(self.rad_button_frame.capm_button.grid_info()['column'], 0)

    def test_create_rbutton_buttons_ddm_button_grid_position(self):
        self.assertEqual(self.rad_button_frame.ddm_button.grid_info()['row'], 2)
        self.assertEqual(self.rad_button_frame.ddm_button.grid_info()['column'], 0)

    def test_create_rbutton_buttons_simple_avg_button_grid_position(self):
        self.assertEqual(self.rad_button_frame.simple_avg_button.grid_info()['row'], 4)
        self.assertEqual(self.rad_button_frame.simple_avg_button.grid_info()['column'], 0)

    def test_create_rbutton_buttons_weighted_avg_button_grid_position(self):
        self.assertEqual(self.rad_button_frame.weighted_avg_button.grid_info()['row'], 5)
        self.assertEqual(self.rad_button_frame.weighted_avg_button.grid_info()['column'], 0)

    # Test update_selection
    def test_capm_button_click_updates_selection(self):
        # Mock app hide input method 
        self.app.hide_input = MagicMock(name='hide_input')
        
        # Select radio button
        self.rad_button_frame.capm_button.invoke()
        
        self.assertEqual(self.rad_button_frame.calc_var.get(), 'Capital Asset Pricing Model')
        self.app.hide_input.assert_called_once_with(self.rad_button_frame.selected_value)

    def test_ddm_button_click_updates_selection(self):
        # Mock app hide input method 
        self.app.hide_input = MagicMock(name='hide_input')
        
        # Select radio button
        self.rad_button_frame.ddm_button.invoke()
        
        self.assertEqual(self.rad_button_frame.calc_var.get(), 'Dividend Discount Model')
        self.app.hide_input.assert_called_once_with(self.rad_button_frame.selected_value)

    def test_simple_avg_button_click_updates_selection(self):
        # Mock app hide input method 
        self.app.hide_input = MagicMock(name='hide_input')
        
        # Select radio button
        self.rad_button_frame.simple_avg_button.invoke()
        
        self.assertEqual(self.rad_button_frame.calc_var.get(), 'Simple Average Returns')
        self.app.hide_input.assert_called_once_with(self.rad_button_frame.selected_value)

    def test_weighted_avg_button_click_updates_selection(self):
        # Mock app hide input method 
        self.app.hide_input = MagicMock(name='hide_input')
        
        # Select radio button
        self.rad_button_frame.weighted_avg_button.invoke()
        
        self.assertEqual(self.rad_button_frame.calc_var.get(), 'Exponential Weighted Average Returns')
        self.app.hide_input.assert_called_once_with(self.rad_button_frame.selected_value)


if __name__ == '__main__':
    unittest.main()