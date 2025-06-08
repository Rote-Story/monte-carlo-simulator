
from tkinter import ttk
from typing import Callable

class ButtonFrame(ttk.Frame):
    """Primary button frame."""

    def __init__(self, master):
        super().__init__(master)
        self._backtest_button: ttk.Button = None
        self._sim_button: ttk.Button = None

    def setup_buttons(self, backtest_button: ttk.Button, sim_button: ttk.Button) -> None:
        """
        Sets up the buttons, on-click behavior, and positions them on the 
        ButtonFrame grid.
        Parameters:
            asset_button - the primary asset button widget; displays asset data 
                when clicked or the 'return' key is pressed
            sim_button - tkinter button widget, runs Monte Carlo simulation when 
                clicked
            asset_button - tkinter button widget, displays historical asset data 
                when clicked
        """
        self._backtest_button = backtest_button
        self._sim_button = sim_button

        # Binding stock data button to enter
        self._backtest_button.bind('<Return>', self._backtest_button.on_backtest_click)

        # Binding run simulation button to enter
        self._sim_button.bind('<Return>', self._sim_button.on_sim_click)

        # Positioning button on the main window grid
        self._backtest_button.grid(
            row=0, column=0, padx=5, pady=5, sticky='ew')
        
        # Positioning button on the main window grid
        self._sim_button.grid(
            row=0, column=1, padx=5, pady=5, sticky='ew')

    # Getter methods
    @property
    def backtest_button(self):
        return self._backtest_button
    
    @property
    def sim_button(self):
        return self._sim_button
    

class BacktestButton(ttk.Button):
    """Button to fetch historical asset prices based on input information"""

    def __init__(self, master: ttk.Frame, backtest_func: Callable):
        super().__init__(
            master,
            text='Test Model Against Historic Performance',
            command=self.on_backtest_click,
            style='TButton'
            )
        self._backtest_func = backtest_func

    def on_backtest_click(self, event=None) -> None:
        """Displays information based on ticker symbol input"""
        self._backtest_func()


class SimButton(ttk.Button):
    """Button widget to fetch data and run monte carlo simulations"""

    def __init__(self,  master: ttk.Frame, run_sim_func: Callable):
        super().__init__(
            master,
            text='Run Simulation of Future Performance',
            command=self.on_sim_click
            )
        self._run_sim_func = run_sim_func

    def on_sim_click(self, event=None) -> None:
        """Runs Monte Carlo simulation"""
        self._run_sim_func()
