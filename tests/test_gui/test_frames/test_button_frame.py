
import tkinter as tk
import unittest
from unittest.mock import MagicMock

from monte_carlo_simulator.gui.frames.button_frame import ButtonFrame, SimButton, BacktestButton
from monte_carlo_simulator.gui.frames.sim_frame import SimFrame
from monte_carlo_simulator.service.simulator_subj import Simulator

class TestButtonFrame(unittest.TestCase):

    def setUp(self):
        # Create mock simulator dependency
        self.mock_simulator = MagicMock(spec=Simulator)

        # Initialize test main window, replace test methods with mocks
        self.root = tk.Tk()
        self.app = SimFrame(master=self.root, simulator=self.mock_simulator)
        self.root.withdraw() # Prevent window from being shown
        self.app.run_forecast = MagicMock(name='run_forecast')
        self.app.run_backtest_sim = MagicMock(name='run_backtest_sim')

        # Initalize test assumptions frame 
        self.button_frame = ButtonFrame(master=self.app)

        # Create mock sim button, mock asset button
        self.sim_button = SimButton(
            master=self.button_frame, 
            run_sim_func=self.app.run_forecast)
        
        self.backtest_button = BacktestButton(
            master=self.button_frame, 
            backtest_func=self.app.run_backtest_sim)
    
        # Setup assumptions labels for testing
        self.button_frame.setup_buttons(
            sim_button=self.sim_button, 
            backtest_button=self.backtest_button
            )

    def tearDown(self):
        self.sim_button.destroy()
        self.backtest_button.destroy()
        self.button_frame.destroy()
        self.app.destroy()
        self.root.destroy()

    def test_setup_buttons_backtest_button_grid_position(self):
        self.assertEqual(self.button_frame.backtest_button.grid_info()['row'], 0)
        self.assertEqual(self.button_frame.backtest_button.grid_info()['column'], 0)

    def test_setup_buttons_sim_button_grid_position(self):
        self.assertEqual(self.button_frame.sim_button.grid_info()['row'], 0)
        self.assertEqual(self.button_frame.sim_button.grid_info()['column'], 1)

    def test_setup_buttons_backtest_button_text(self):
        self.assertEqual(self.button_frame.backtest_button.cget('text'), 'Test Model Against Historic Performance')

    def test_setup_buttons_sim_button_text(self):
        self.assertEqual(self.button_frame.sim_button.cget('text'), 'Run Simulation of Future Performance')

    def test_on_click_backtest_button_click_behavior(self):
        self.button_frame.backtest_button.invoke() 
        self.app.run_backtest_sim.assert_called_once()

    def test_on_click_sim_button_click_behavior(self):
        self.button_frame.sim_button.invoke()
        self.app.run_forecast.assert_called_once()


if __name__ == '__main__':
    unittest.main()