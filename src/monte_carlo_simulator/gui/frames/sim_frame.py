
import tkinter as tk
from tkinter import ttk
from monte_carlo_simulator.const import RFR_SECURITIES, TIME_PERIODS, MARKET_INDEXES


from monte_carlo_simulator.gui.frames.button_frame import ButtonFrame
from monte_carlo_simulator.gui.frames.error_frame_obs import ErrorFrame
from monte_carlo_simulator.gui.frames.radio_button_frame import RadioButtonFrame
from monte_carlo_simulator.gui.frames.assumptions_frame_obs import AssumptionsFrame
from monte_carlo_simulator.gui.frames.vis_frames_obs import SimVisFrame, BacktestVisFrame
from monte_carlo_simulator.gui.frames.input_frame import InputFrame
from monte_carlo_simulator.service.interface.subject_inter import Subject


class SimFrame(ttk.Frame):
    """
    Main simulation GUI window. Contains user I/O frames arranged
    in a grid format.
    """

    def __init__(self, master: tk.Tk, simulator: Subject):

        super().__init__(master=master, height=1000, width=1525)
        self.simulator = simulator

        self._button_frame: ButtonFrame = None 
        self._error_frame: ErrorFrame = None 
        self._radio_button_frame: RadioButtonFrame = None 
        self._assumptions_frame: AssumptionsFrame = None 
        self._sim_vis_frame: SimVisFrame = None 
        self._backtest_vis_frame: BacktestVisFrame = None 
        self._input_frame: InputFrame = None 

    def setup_frames(self,
                button_frame: ButtonFrame,
                error_frame: ErrorFrame,
                radio_button_frame: RadioButtonFrame,
                assumptions_frame: AssumptionsFrame,
                sim_vis_frame: SimVisFrame,
                backtest_vis_frame: BacktestVisFrame,
                input_frame: InputFrame
                ):
        """Sets up frames on the main window and positions them on the grid"""

        # Creating input and output frames on the main window
        self._button_frame = button_frame
        self._error_frame = error_frame
        self._radio_button_frame = radio_button_frame
        self._assumptions_frame = assumptions_frame
        self._sim_vis_frame = sim_vis_frame
        self._backtest_vis_frame = backtest_vis_frame
        self._input_frame = input_frame
        
        # Positioning frames and error output label on the window grid
        self._backtest_vis_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ns')
        self._sim_vis_frame.grid(row=0, column=1, padx=5, pady=5)
        self._assumptions_frame.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self._input_frame.grid(row=1, column=0, padx=5, pady=5, sticky='new', rowspan=2)
        self._button_frame.grid(row=3, column=0, padx=5, pady=5, columnspan=2, sticky='s')
        self._error_frame.grid(row=4, column=0, padx=5, pady=5, columnspan=2)
        self._radio_button_frame.grid(row=2, column=1, padx=5, pady=20, sticky='new')

        # Configuring frame grid columns
        self._backtest_vis_frame.grid_columnconfigure(0, weight=1)
        self._sim_vis_frame.grid_columnconfigure(0, weight=1)
        self._input_frame.grid_columnconfigure(0, weight=1)
        self._assumptions_frame.grid_columnconfigure(0, weight=1)
        self._button_frame.grid_columnconfigure(0, weight=1)
        self._error_frame.grid_columnconfigure(0, weight=1)
        self._radio_button_frame.grid_columnconfigure(0, weight=1)

        # Configure frame grid rows
        self._backtest_vis_frame.grid_rowconfigure(0, weight=1)
        self._sim_vis_frame.grid_rowconfigure(0, weight=1)
        self._input_frame.grid_rowconfigure(0, weight=1)
        self._assumptions_frame.grid_rowconfigure(0, weight=1)
        self._button_frame.grid_rowconfigure(0, weight=1)
        self._error_frame.grid_rowconfigure(0, weight=1)
        self._radio_button_frame.grid_rowconfigure(0, weight=1)

        # Bind enter to simulation button for each input widget
        self._input_frame.asset_entry.bind('<Return>', self._button_frame.sim_button.on_sim_click)
        self._input_frame.horizon_spinbox.bind('<Return>', self._button_frame.sim_button.on_sim_click)
        self._input_frame.market_combobox.bind('<Return>', self._button_frame.sim_button.on_sim_click)
        self._input_frame.time_period_combobox.bind('<Return>', self._button_frame.sim_button.on_sim_click)
        self._input_frame.standev_spinbox.bind('<Return>', self._button_frame.sim_button.on_sim_click)
        self._input_frame.n_sim_spinbox.bind('<Return>', self._button_frame.sim_button.on_sim_click)
        self._input_frame.rfr_combobox.bind('<Return>', self._button_frame.sim_button.on_sim_click)

    def hide_input(self, selected_value: str) -> None:
        """
        Dynamically hides or shows input frame widgets depending on the radio button 
        frame's selected calculation method.
        """
        # Check to make sure input frame has been created before hiding widgets
        if self._input_frame != None:

            # Match input hiding to appropriate valuation models
            match selected_value:

                case 'Capital Asset Pricing Model':
                    # Show risk-free rate and market index input options to user
                    self._input_frame.rfr_security_label.grid(row=6, column=0, padx=5, pady=5, sticky='e')
                    self._input_frame.rfr_combobox.grid(row=6, column=1, padx=5, pady=5, sticky='ew')
                    self._input_frame.market_index_label.grid(row=7, column=0, padx=5, pady=5, sticky='e')
                    self._input_frame.market_combobox.grid(row=7, column=1, padx=5, pady=5, sticky='ew')
                    
                # Default case: Hides input fields irrelevant to the chosen valuation model
                case _:
                    # Hide risk-free rate and market index inputs, since they are 
                    # not used in this valuation method's calculations
                    self._input_frame.rfr_security_label.grid_forget()
                    self._input_frame.rfr_combobox.grid_forget()
                    self._input_frame.market_index_label.grid_forget()
                    self._input_frame.market_combobox.grid_forget()

    def run_forecast(self):
        """
        Runs a simulation using all available data to project future price paths over 
        the chosen investment time horizon.
        """

        rfr_symbol = self._process_rfr_input()
        market_symbol = self._process_market_input()

        self.simulator.run_simulation(
            asset_symbol = self.input_frame.asset_entry.get(),
            period = TIME_PERIODS[self.input_frame.time_period_combobox.get()],
            exp_ret_flag = self.radio_button_frame.calc_var.get(),
            time_horizon = int(self.input_frame.horizon_spinbox.get()), # Cast str to int
            n_simulations = int(self.input_frame.n_sim_spinbox.get()), # Cast str to int
            standev_window = self._input_frame.standev_spinbox.get(),
            market_symbol = market_symbol,
            rfr_symbol = rfr_symbol
        )

    def run_backtest_sim(self):
        """
        Runs a simulation displaying how the model would have performed over the chosen 
        time horizon, comparing simulated price paths to actual asset returns over the 
        period.
        """

        rfr_symbol = self._process_rfr_input()
        market_symbol = self._process_market_input()

        self.simulator.run_backtest(
            asset_symbol = self.input_frame.asset_entry.get(),
            period = TIME_PERIODS[self.input_frame.time_period_combobox.get()],
            exp_ret_flag = self.radio_button_frame.calc_var.get(),
            time_horizon = int(self.input_frame.horizon_spinbox.get()), # Cast str to int
            n_simulations = int(self.input_frame.n_sim_spinbox.get()), # Cast str to int
            standev_window = self._input_frame.standev_spinbox.get(),
            market_symbol = market_symbol,
            rfr_symbol = rfr_symbol
        )

    def _process_market_input(self) -> str:
        """
        Identifies whether market index input is in the pre-selected list. If the 
        value was pre-selected, then the function converts pre-selected list values 
        into their corresponding market symbols, otherwise, returns the symbol.
        
        Returns: A tuple containing the market symbol and risk-free rate symbol, with the 
            market symbol returned as the first value, e.g. (market_symbol, rfr_symbol)
        """
        # Check if user input one of the pre-selected market indexes
        if self.input_frame.market_combobox.get() in MARKET_INDEXES.keys():
            # If the user selected a market index from the list, get the corresponding ticker
            market_symbol = MARKET_INDEXES[self.input_frame.market_combobox.get()]
        
        # If the user entered their own index ticker symbol, then use the input directly
        else:
            market_symbol = self.input_frame.market_combobox.get()
        
        return market_symbol

    def _process_rfr_input(self) -> str:
        """
        Identifies whether risk-free rate input is in the pre-selected list. If the 
        value was pre-selected, then the function converts pre-selected list values 
        into their corresponding risk-free rate symbols, otherwise, returns the symbol.
        
        Returns: The risk-free rate symbol
        """
        # Check if the user input one of the pre-selected risk-free securities
        if self.input_frame.rfr_combobox.get() in RFR_SECURITIES.keys():
            # If the user selected a risk-free security from the list, then get the corresponding ticker
            rfr_symbol = RFR_SECURITIES[self.input_frame.rfr_combobox.get()]
        
        # If the user entered their own risk-free security ticker symbol, then use their input directly
        else:
            rfr_symbol = self.input_frame.rfr_combobox.get()

        return rfr_symbol

    @property
    def button_frame(self):
        return self._button_frame
    
    @property
    def error_frame(self):
        return self._error_frame
    
    @property
    def radio_button_frame(self):
        return self._radio_button_frame
    
    @property
    def assumptions_frame(self):
        return self._assumptions_frame
    
    @property
    def sim_vis_frame(self):
        return self._sim_vis_frame
    
    @property
    def asset_vis_frame(self):
        return self._backtest_vis_frame
    
    @property
    def input_frame(self):
        return self._input_frame


    @button_frame.setter
    def button_frame(self, button_frame) -> None:
        self._button_frame = button_frame
        
    @error_frame.setter
    def error_frame(self, error_frame) -> None:
        self._error_frame = error_frame
        
    @radio_button_frame.setter
    def radio_button_frame(self, radio_button_frame) -> None:
        self._radio_button_frame = radio_button_frame
        
    @assumptions_frame.setter
    def assumptions_frame(self, assumptions_frame) -> None:
        self._assumptions_frame = assumptions_frame
        
    @sim_vis_frame.setter
    def sim_vis_frame(self, sim_vis_frame) -> None:
        self._sim_vis_frame = sim_vis_frame
        
    @asset_vis_frame.setter
    def asset_vis_frame(self, asset_vis_frame) -> None:
        self._backtest_vis_frame = asset_vis_frame
        
    @input_frame.setter
    def input_frame(self, input_frame) -> None:
        self._input_frame = input_frame
        