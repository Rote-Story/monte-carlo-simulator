

from tkinter import ttk

from monte_carlo_simulator.const import RFR_SECURITIES, TIME_PERIODS, MARKET_INDEXES

class InputFrame(ttk.Labelframe):
    """Main frame for user input."""

    def __init__(self, master):
        super().__init__(master, text='Simulation Information Input')
        self.master = master
        self.create_simulation_input()
        self.create_rfr_input()
        self.create_market_input()
        self.create_entry_labels()

    def create_simulation_input(self):
        """Displays asset input widgets"""

        # Asset entry widget
        self.asset_entry = ttk.Entry(
            self,
            width=26,
            style='TEntry'
            )
        # Set default value
        self.asset_entry.insert(0, 'IBM')

        # Time horizon entry widget
        self.horizon_spinbox = ttk.Spinbox(
            self,
            from_=1,  # Minimum value
            to=365,  # Maximum value, 1 year
            increment=1,  # Increment steps
            width=26,
            style='TSpinbox'
            )
        # Set default value
        self.horizon_spinbox.insert(0, 12)

        # Time period input combobox, read only, drop down selection window
        # Historical data to use in asset calculations
        self.time_period_combobox = ttk.Combobox(
            self,
            values=list(TIME_PERIODS.keys()), # Set values to valid yfinance time period dictionary keys
            state='readonly',
            width=26,
            style='TCombobox'
            )
        # Set default value to the last 1 year
        self.time_period_combobox.set('Last 2 years')

        # Rolling standard deviation window input
        self.standev_spinbox = ttk.Spinbox(
            self,
            from_=1,  # Minimum value
            to=365,  # Maximum value, 1 year
            increment=1,  # Increment steps
            width=26,
            style='TSpinbox'
            )
        # Set initial value to 30 days
        self.standev_spinbox.insert(0, 30)
        
        # The number of simulations to be run spinbox
        self.n_sim_spinbox = ttk.Spinbox(
            self,
            from_=100,  # Minimum value
            to=100000,  # Maximum value
            increment=100,  # Increment steps
            width=26,
            style='TSpinbox'
            )
        # Set initial value to 30 days
        self.n_sim_spinbox.insert(0, 1000)

        # Position widgets on input_frame grid
        self.asset_entry.grid(
            row=1, column=1, padx=5, pady=5, sticky='ew')
        self.horizon_spinbox.grid(
            row=2, column=1, padx=5, pady=5, sticky='ew')
        self.time_period_combobox.grid(
            row=3, column=1, padx=5, pady=5, sticky='ew')
        self.standev_spinbox.grid(
            row=4, column=1, padx=5, pady=5, sticky='ew')
        self.n_sim_spinbox.grid(
            row=5, column=1, padx=5, pady=5, sticky='ew')

    def create_rfr_input(self):
        # Risk-free rate security input combobox, read only
        self.rfr_combobox = ttk.Combobox(
            self,
            # Set values to possible time frame keys for 
            # data_fetcher.ThreadManager.periods dictionary
            values=list(RFR_SECURITIES.keys()),
            state='active',
            width=26,
            style='TCombobox'
            )
        # Set default value to the last 1 year
        self.rfr_combobox.set('13-week U.S. Treasuries')

        self.rfr_combobox.grid(
            row=6, column=1, padx=5, pady=5, sticky='ew')
        
    def create_market_input(self):
        # Risk-free rate security input combobox, read only
        self.market_combobox = ttk.Combobox(
            self,
            # Set values to possible time frame keys for 
            # data_fetcher.ThreadManager.periods dictionary
            values=list(MARKET_INDEXES.keys()),
            state='active',
            width=26,
            style='TCombobox'
            )
        # Set default value to the last 1 year
        self.market_combobox.set('S&P 500')

        self.market_combobox.grid(
            row=7, column=1, padx=5, pady=5, sticky='ew')
        
    def create_entry_labels(self):
        """Displays entry labels for each input box"""

        # Asset entry widget label
        self.asset_entry_label = ttk.Label(
            self,
            text='Enter asset ticker symbol:',
            style='TLabel'
            )

        # Time horizon entry widget label; how far into the future to predict
        self.horizon_entry_label = ttk.Label(
            self,
            text='Enter your investment time horizon (in days):',
            style='TLabel'
            )

        # Time period label
        self.time_period_label = ttk.Label(
            self,
            text='Enter the timeframe to use in calculations:',
            style='TLabel'
            )

        # Rolling standard deviation window label
        self.standev_label = ttk.Label(
            self,
            text='Enter current volatility timeframe (in days):',
            style='TLabel'
            )

        # Number of simulations window label
        self.n_sim_label = ttk.Label(
            self,
            text='Enter the number of simulations you would like to run:',
            style='TLabel'
            )

        self.rfr_security_label = ttk.Label(
            self,
            text='Select the security to use for risk-free rate calculations:',
            style='TLabel'
            )

        self.market_index_label = ttk.Label(
            self,
            text='Select the index to use in calculations:',
            style='TLabel'
            )

        # Position labels on the input_frame grid
        self.asset_entry_label.grid(
            row=1, column=0, padx=5, pady=5, sticky='e')
        self.horizon_entry_label.grid(
            row=2, column=0, padx=5, pady=5, sticky='e')
        self.time_period_label.grid(
            row=3, column=0, padx=5, pady=5, sticky='e')
        self.standev_label.grid(
            row=4, column=0, padx=5, pady=5, sticky='e')
        self.n_sim_label.grid(
            row=5, column=0, padx=5, pady=5, sticky='e')
        self.rfr_security_label.grid(
            row=6, column=0, padx=5, pady=5, sticky='e')
        self.market_index_label.grid(
            row=7, column=0, padx=5, pady=5, sticky='e')