
from tkinter import ttk

from monte_carlo_simulator.gui.inter.observer_inter import Observer


class AssumptionsFrame(ttk.Labelframe, Observer):
    """
    Displays assumptions used in monte carlo simulation input data to user:
        Volatility, beta, risk-free rate, market returns, and expected returns 
        of the target asset (stock).
    """

    def __init__(self, master):
        super().__init__(master, text='Simulation Assumptions')
        self.create_assumptions()

    def create_assumptions(self):
        """
        Displays assumptions that the financial model uses for
        predictions 
        """


        # Calculated volatility based on standard deviation of historical
        # returns
        self.volatility_label = ttk.Label(
            self,
            text=''
            )

        # Create label to show beta assumption supplied by yfinance
        self.beta_label = ttk.Label(
            self,
            text=''
            )

        # Create label to show risk free rate from relevant asset
        # (relevant asset is 10-year treasury bonds)
        self.rfr_label = ttk.Label(
            self,
            text=''
            )

        # Create label to show market returns from relevant index
        # (relevant index is S&P 500)
        self.market_returns_label = ttk.Label(
            self,
            text=''
            )

        # Create label to show expected returns
        self.expected_returns_label = ttk.Label(
            self,
            text=''
            )

        # Create label to show historic dividend growth
        self.div_growth_label = ttk.Label(
            self,
            text=''
            )

        # Position contents on the assumptions_frame grid
        self.beta_label.grid(
            row=0, column=0, padx=15, pady=5, sticky='e')
        self.volatility_label.grid(
            row=1, column=0, padx=15, pady=5, sticky='e')
        self.rfr_label.grid(
            row=0, column=1, padx=15, pady=5, sticky='e')
        self.market_returns_label.grid(
            row=1, column=1, padx=15, pady=5, sticky='e')
        self.expected_returns_label.grid(
            row=2, column=0, padx=15, pady=5, sticky='e')
        self.div_growth_label.grid(
            row=2, column=1, padx=15, pady=5, sticky='e')
    
    def update(self, subject):
        """
        Configures assumption frame's output labels; 
        displays key model assumptions to user.
        """
        # Check that expected returns have been calculated
        if subject.financial_asset.his_vol != None and subject.financial_asset.expected_returns != None:

            # Set volatility_label to show calculated stock volatility
            self.volatility_label.config(
                text=f'{subject.financial_asset.asset_symbol}\'s volatility: {subject.financial_asset.his_vol: .4f}')

            # Set expected_returns_label output to show expected returns; converting to annual returns
            self.expected_returns_label.config(
                text=f'{subject.financial_asset.asset_symbol}\'s expected returns: {subject.financial_asset.expected_returns * 100: .4f}%')
        
            # Check which model was chosen to provide model-specific assumptions
            match subject.financial_asset.exp_ret_flag:
            
                case 'Dividend Discount Model':
                    # Display historic dividend prices
                    self.div_growth_label.config(
                        text=f'{subject.financial_asset.asset_symbol}\'s historic dividend growth rate: {subject.financial_asset.div_growth_rate * 100: .4f}%')

                case 'Capital Asset Pricing Model':
                    # Display beta for selected stock
                    self.beta_label.config(
                        text=f'{subject.financial_asset.asset_symbol}\'s beta: {subject.financial_asset.beta: .4f}')

                    # Set returns_label output to show market returns
                    self.market_returns_label.config(
                        text=f'Market returns: {subject.market_index.market_returns * 100: .4f}%')
                    
                    # Set risk free rate label to show 'risk free rate'
                    self.rfr_label.config(
                        text=f'{subject.risk_free_sec.rfr_symbol} historic returns: {subject.risk_free_sec.risk_free_rate * 100: .4f}%')

                    # Clearing any old output text not relevant to this model
                    self.div_growth_label.config(text=f'')

                case 'Simple Average Returns':
                    # No additional metrics are used in calculation of historical average returns
                    # Clearing prior assumptions text that is irrelevant to this model
                    self.beta_label.config(text=f'')
                    self.market_returns_label.config(text=f'')
                    self.rfr_label.config(text=f'')
                    self.div_growth_label.config(text=f'')

                case 'Exponential Weighted Average Returns':
                    # No additional metrics are used in calculation of historical average returns
                    # No additional metrics are used in calculation of historical average returns
                    # Clearing prior assumptions text that is irrelevant to this model
                    self.beta_label.config(text=f'')
                    self.market_returns_label.config(text=f'')
                    self.rfr_label.config(text=f'')
                    self.div_growth_label.config(text=f'')

 

