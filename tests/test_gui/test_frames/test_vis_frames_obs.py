
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import unittest
from unittest.mock import MagicMock, PropertyMock, patch
import tkinter as tk

from monte_carlo_simulator.gui.frames.vis_frames_obs import BacktestVisFrame, SimVisFrame
from monte_carlo_simulator.gui.frames.sim_frame import SimFrame
from monte_carlo_simulator.model.financial_asset import FinancialAsset
from monte_carlo_simulator.service.simulator_subj import Simulator

class TestSimVisFrame(unittest.TestCase):

    def setUp(self):
        # Create mock simulator dependency
        self.mock_simulator = MagicMock(spec=Simulator)

        # Initialize test main window, replace test methods with mocks
        self.root = tk.Tk()
        self.app = SimFrame(master=self.root, simulator=self.mock_simulator)
        self.root.withdraw() # Prevent window from being shown

        # Initialize radio button frame
        self.sim_vis_frame = SimVisFrame(self.app)

        # Create figure, and figure canvas objects with mock methods
        self.figure = plt.Figure()
        self.fig_canvas = FigureCanvasTkAgg
        self.fig_canvas.draw = MagicMock(name='draw')
        self.fig_canvas.get_tk_widget = MagicMock(name='get_tk_widget')

        patch('monte_carlo_simulator.gui.frames.vis_frames_obs.FigureCanvasTkAgg',
            return_value=self.fig_canvas
            )

    def tearDown(self):
        self.sim_vis_frame.destroy()
        self.app.destroy()
        self.root.destroy()
        patch.stopall()

    def test_update_sim_figure_canvas_draw_called_once(self):
        self.mock_simulator.configure_mock(sim_figure=self.figure)
        self.sim_vis_frame.update(self.mock_simulator)
        self.fig_canvas.draw.assert_called_once()

    def test_update_sim_figure_canvas_get_tk_widget_called_once(self):
        self.mock_simulator.configure_mock(sim_figure=self.figure)
        self.sim_vis_frame.update(self.mock_simulator)
        self.fig_canvas.get_tk_widget.assert_called_once()

    def test_update_subject_sim_data_int(self):
        self.mock_simulator.configure_mock(sim_figure=10)
        self.sim_vis_frame.update(self.mock_simulator) # Call method to test behavior
        
        # FigureCanvasTkAgg object methods should only be called if update is called
        # with a Figure object
        self.fig_canvas.draw.assert_not_called()
        self.fig_canvas.get_tk_widget.assert_not_called()

    def test_update_subject_sim_data_none(self):
        self.mock_simulator.configure_mock(sim_figure=None)
        self.sim_vis_frame.update(self.mock_simulator) # Call method to test behavior
        
        # FigureCanvasTkAgg object methods should only be called if update is called
        # with a Figure object
        self.fig_canvas.draw.assert_not_called()
        self.fig_canvas.get_tk_widget.assert_not_called()

    def test_update_subject_sim_data_bool(self):
        self.mock_simulator.configure_mock(sim_figure=True)
        self.sim_vis_frame.update(self.mock_simulator) # Call method to test behavior
        
        # FigureCanvasTkAgg object methods should only be called if update is called
        # with a Figure object
        self.fig_canvas.draw.assert_not_called()
        self.fig_canvas.get_tk_widget.assert_not_called()

    def test_update_subject_sim_data_float(self):
        self.mock_simulator.configure_mock(sim_figure=0.03)
        self.sim_vis_frame.update(self.mock_simulator) # Call method to test behavior
        
        # FigureCanvasTkAgg object methods should only be called if update is called
        # with a Figure object
        self.fig_canvas.draw.assert_not_called()
        self.fig_canvas.get_tk_widget.assert_not_called()

    def test_update_subject_sim_data_str(self):
        self.mock_simulator.configure_mock(sim_figure='string')
        self.sim_vis_frame.update(self.mock_simulator) # Call method to test behavior
        
        # FigureCanvasTkAgg object methods should only be called if update is called
        # with a Figure object
        self.fig_canvas.draw.assert_not_called()
        self.fig_canvas.get_tk_widget.assert_not_called()

    def test_update_subject_sim_data_list(self):
        self.mock_simulator.configure_mock(sim_figure=[10, 12])
        self.sim_vis_frame.update(self.mock_simulator) # Call method to test behavior
        
        # FigureCanvasTkAgg object methods should only be called if update is called
        # with a Figure object
        self.fig_canvas.draw.assert_not_called()
        self.fig_canvas.get_tk_widget.assert_not_called()

    def test_update_subject_sim_data_dict(self):
        self.mock_simulator.configure_mock(sim_figure={'Array': np.linspace(0, 10, 10)})
        self.sim_vis_frame.update(self.mock_simulator) # Call method to test behavior
        
        # FigureCanvasTkAgg object methods should only be called if update is called
        # with a Figure object
        self.fig_canvas.draw.assert_not_called()
        self.fig_canvas.get_tk_widget.assert_not_called()


class TestAssetVisFrame(unittest.TestCase):

    def setUp(self):
        # Create mock simulator dependency, financial asset, and asset data return value
        self.mock_simulator = MagicMock(spec=Simulator)
        self.mock_financial_asset = MagicMock(spec=FinancialAsset)
        type(self.mock_simulator).financial_asset = PropertyMock(return_value=self.mock_financial_asset)

        # Initialize test main window, replace test methods with mocks
        self.root = tk.Tk()
        self.app = SimFrame(master=self.root, simulator=self.mock_simulator)
        self.root.withdraw() # Prevent window from being shown

        # Initialize radio button frame
        self.backtest_vis_frame = BacktestVisFrame(self.app)

         # Create figure, and figure canvas objects with mock methods
        self.figure = plt.Figure()
        self.fig_canvas = FigureCanvasTkAgg
        self.fig_canvas.draw = MagicMock(name='draw')
        self.fig_canvas.get_tk_widget = MagicMock(name='get_tk_widget')

        patch('monte_carlo_simulator.gui.frames.vis_frames_obs.FigureCanvasTkAgg',
            return_value=self.fig_canvas
            )

    def tearDown(self):
        self.backtest_vis_frame.destroy()
        self.app.destroy()
        self.root.destroy()
        patch.stopall()

    def test_update_backtest_figure_canvas_draw_called_once(self):
        self.mock_simulator.configure_mock(backtest_figure=self.figure)
        self.backtest_vis_frame.update(self.mock_simulator)
        self.fig_canvas.draw.assert_called_once()

    def test_update_backtest_figure_canvas_get_tk_widget_called_once(self):
        self.mock_simulator.configure_mock(backtest_figure=self.figure)
        self.backtest_vis_frame.update(self.mock_simulator)
        self.fig_canvas.get_tk_widget.assert_called_once()

    def test_update_subject_asset_data_int(self):
        self.mock_simulator.configure_mock(backtest_figure=10)
        self.backtest_vis_frame.update(self.mock_simulator) # Call method to test behavior
           
        # FigureCanvasTkAgg object methods should only be called if update is called
        # with a Figure object
        self.fig_canvas.draw.assert_not_called()
        self.fig_canvas.get_tk_widget.assert_not_called()            

    def test_update_subject_asset_data_none(self):
        self.mock_simulator.configure_mock(backtest_figure=None)
        self.backtest_vis_frame.update(self.mock_simulator) # Call method to test behavior
        
        # FigureCanvasTkAgg object methods should only be called if update is called
        # with a Figure object
        self.fig_canvas.draw.assert_not_called()
        self.fig_canvas.get_tk_widget.assert_not_called()

    def test_update_subject_asset_data_bool(self):
        self.mock_simulator.configure_mock(backtest_figure=True)
        self.backtest_vis_frame.update(self.mock_simulator) # Call method to test behavior
        
        # FigureCanvasTkAgg object methods should only be called if update is called
        # with a Figure object
        self.fig_canvas.draw.assert_not_called()
        self.fig_canvas.get_tk_widget.assert_not_called()

    def test_update_subject_asset_data_float(self):
        self.mock_simulator.configure_mock(backtest_figure=0.03)
        self.backtest_vis_frame.update(self.mock_simulator) # Call method to test behavior
        
        # FigureCanvasTkAgg object methods should only be called if update is called
        # with a Figure object
        self.fig_canvas.draw.assert_not_called()
        self.fig_canvas.get_tk_widget.assert_not_called()

    def test_update_subject_asset_data_str(self):
        self.mock_simulator.configure_mock(backtest_figure='string')
        self.backtest_vis_frame.update(self.mock_simulator) # Call method to test behavior
        
        # FigureCanvasTkAgg object methods should only be called if update is called
        # with a Figure object
        self.fig_canvas.draw.assert_not_called()
        self.fig_canvas.get_tk_widget.assert_not_called()

    def test_update_subject_asset_data_list(self):
        self.mock_simulator.configure_mock(backtest_figure=[10, 12])
        self.backtest_vis_frame.update(self.mock_simulator) # Call method to test behavior
        
        # FigureCanvasTkAgg object methods should only be called if update is called
        # with a Figure object
        self.fig_canvas.draw.assert_not_called()
        self.fig_canvas.get_tk_widget.assert_not_called()

    def test_update_subject_asset_data_dict(self):
        self.mock_simulator.configure_mock(backtest_figure={'Array': np.linspace(0, 10, 10)})
        self.backtest_vis_frame.update(self.mock_simulator) # Call method to test behavior
        
        # FigureCanvasTkAgg object methods should only be called if update is called
        # with a Figure object
        self.fig_canvas.draw.assert_not_called()
        self.fig_canvas.get_tk_widget.assert_not_called()


if __name__ == '__main__':
    unittest.main()