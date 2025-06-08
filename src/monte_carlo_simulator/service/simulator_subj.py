
from typing import List
from matplotlib.figure import Figure
from numbers import Number
import numpy as np

from monte_carlo_simulator.model import *
from monte_carlo_simulator.data_fetcher import MarketDataFetcher
from monte_carlo_simulator.service.interface.subject_inter import Subject
from monte_carlo_simulator.const import ANNUAL_TRADING_DAYS, MONTHS_PER_YEAR
from monte_carlo_simulator.service.util.price_col_checker import price_col_checker
from monte_carlo_simulator.service.calculator import *
from monte_carlo_simulator.service.util.data_visualizer import monte_carlo_sim_vis, backtest_vis

class Simulator(Subject):
    """
    Subject implementation that facilitates gathering and storing data to
    run Monte Carlo simulations, as well as notifying the GUI of results.
    Maintains a list of observers which are notified whenever the state of 
    the Simulator object changes, allowing them to update displayed information.

    __init__ Parameters:
        market_data_fetcher - a MarketDataFetcher object used to fetch financial data using yfinance module
        financial_asset - a data storage class modeling a generalized financial asset
        market_index - a data storage class modeling a market index 
        risk_free_sec - a data storgae class modeling a 'risk-free' security
    """
    def __init__(self, 
                 market_data_fetcher: MarketDataFetcher, 
                 financial_asset: FinancialAsset, 
                 market_index: MarketIndex,
                 risk_free_sec: RiskFreeSecurity
                 ):
        self.data_fetcher = market_data_fetcher
        self._observers: List = []
        self._financial_asset: FinancialAsset = financial_asset
        self._market_index: MarketIndex = market_index
        self._risk_free_sec: RiskFreeSecurity = risk_free_sec
        self._backtest_figure: Figure = None
        self._sim_figure: Figure = None
        self._error_message: str = None

    def attach(self, observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer) -> None:
        try:
            self._observers.remove(observer)
        except ValueError:
            self.error_message = f'{observer} not in list of observers.'
            self.notify()

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def populate_data(
            self, 
            asset_symbol: str, 
            market_symbol:str, 
            rfr_symbol:str, 
            period:str,
            exp_ret_flag: str
            ) -> None:
        """
        Populates asset data, market data, and risk-free rate data. If matching data 
        already exists for the symbols and time periods, then no data is gathered.
        
        Parameters: 
            asset_symbol - a ticker symbol for an asset, like a 'IBM'
            market_symbol - a valid ticker symbol for a market index, like the 
                S&P 500 ('^GSPC')
            rfr_symbol - a valid ticker symbol for a 'risk-free' asset, like U.S. 
                treasuries (e.g, '^TNX')
            period - a valid time period like '5y' (5 years), or 6mo (6 months)
            exp_ret_flag - a string holding the returns calculation method used to
                predict future asset returns (e.g., 'Dividend Discount Model')

        Returns: None; fills out class data fields instead of returning values
        """
        # Check that asset symbol is correct type 
        if type(asset_symbol) != str:
            raise TypeError(f'"asset_symbol" must be of type str, not {type(asset_symbol)}')

        # Check if time period and asset symbol match existing data
        elif self.financial_asset.period != period or self.financial_asset.asset_symbol != asset_symbol:

            # Poupulate asset_data fields
            self.financial_asset.asset_symbol = asset_symbol
            self.financial_asset.asset_data = self.data_fetcher.fetch_asset_data(asset_symbol, period)
 
        # Store exp_ret_flag to use when calling calculate expected returns function
        self.financial_asset.exp_ret_flag = exp_ret_flag

        # Fetch additional data needed for the chosen asset valuation model
        match exp_ret_flag:

            case 'Capital Asset Pricing Model':
                # Make sure that risk-free and market index symbols are included
                if type(market_symbol) != str:
                    raise TypeError(f'"market_symbol" must be of type str, not {type(market_symbol)}')

                elif type(rfr_symbol) != str:
                    raise TypeError(f'"rfr_symbol" must be of type str, not {type(rfr_symbol)}')

                # Gather preliminary market data if existing data does not match user request
                if self.market_index.market_symbol != market_symbol:

                    # Populate market index data fields
                    self.market_index.market_symbol = market_symbol
                    self.market_index.market_data = self.data_fetcher.fetch_market_data(market_symbol, period)

                
                # Gather preliminary risk-free rate data if existing data does not match user request
                if self.risk_free_sec.rfr_symbol != rfr_symbol:
                    
                    # Populate risk-free rate data fields
                    self.risk_free_sec.rfr_symbol = rfr_symbol
                    self.risk_free_sec.rfr_data = self.data_fetcher.fetch_rfr_data(rfr_symbol, period)

            case 'Dividend Discount Model':
                # Fetch asset ticker object (needed to get historic dividend data)
                self.financial_asset.asset_ticker = self.data_fetcher.fetch_ticker_object(asset_symbol)

                # Historic dividends needed to calculate expected returns using the Dividend Discount Model
                self.financial_asset.his_div = self.data_fetcher.fetch_historic_div(self.financial_asset.asset_ticker)
        
        # Store any error messages generated by data fetcher function calls
        self._error_message = self.data_fetcher.error_message

    def run_simulation(
            self, 
            asset_symbol: str, 
            period: str,
            exp_ret_flag: str,
            time_horizon: int = 12,
            n_simulations: int = 1000,
            standev_window: int = 30,
            market_symbol: str = None, 
            rfr_symbol: str = None
            ) -> None:
        """
        Facilitates running Monte Carlo simulation: Manages gathering data and
        calculations necessary to run the calculation, handles errors, and notifies
        observers of the results or any problems that occur. 
        
        Parameters: 
            asset_symbol - a ticker symbol for a financial asset (e.g., 'AAPL')
            period - the period of historical asset, market, and risk-free rate, data
                that the user would like to use in the calculations and simulation
            exp_ret_flag - a string holding the returns calculation method used to
                predict future asset returns (e.g., 'Dividend Discount Model')
            time_horizon - the future period to be forecasted by the Monte Carlo 
                simulation (in months)
            n_simulations - the number of simulations the user would like to run
            standev_window - the number of days used to calculate the rolling standard 
                deviation of asset prices 
            market_symbol - a ticker symbol for a market index (e.g., '^GSPC')
            rfr_symbol - a ticker symbol for a 'risk-free' asset (e.g, '^IRX')

        Returns: None; this method calls self.notify() to notify observers
            of simulation results. Observers then display results or any error 
            messages encountered during this function 
        """
        # Run as protected code to handle exceptions
        try: 
            # Populating primary data fields for future calculations and simulation
            self.populate_data(asset_symbol, market_symbol, rfr_symbol, period, exp_ret_flag)
            

            # Calculate expected returns
            self.financial_asset.expected_returns = calc_exp_returns(
                financial_asset=self.financial_asset,
                market_index=self.market_index,
                risk_free_sec=self.risk_free_sec
                )
            # Handle possible KeyErrors for market_data with only a 'Close' column
            close_column = price_col_checker(self.financial_asset.asset_data)

            # Set initial price for Monte Carlo simulations to most recent value
            initial_price = self.financial_asset.asset_data[close_column].iloc[-1, -1]
            
            # Calculate historic volatility of the chosen asset
            self.financial_asset.his_vol = calc_volatility(
                self.financial_asset.asset_data, standev_window)

            # Run Monte Carlo simulation to predict future prices
            sim_data = self.monte_carlo_sim(
                initial_price=initial_price, 
                expected_returns=self.financial_asset.expected_returns,
                his_vol=self.financial_asset.his_vol,
                time_horizon=time_horizon,
                n_simulations=n_simulations
                )

            # Get simulation visualization figure
            self._sim_figure = monte_carlo_sim_vis(sim_data, time_horizon)

            self.notify()  # Notify observers of updated data
        
        # Notify observers if an exception occurred
        except Exception as e: 
            # If no exception message has been set, use generalized message
            if self.error_message == None:
                self.error_message = f'An exception occurred: {e}'

            self.notify()

    def run_backtest(
            self, 
            asset_symbol: str, 
            period: str,
            exp_ret_flag: str,
            time_horizon: int = 12,
            n_simulations: int = 1000,
            standev_window: int = 30,
            market_symbol: str = None, 
            rfr_symbol: str = None
            ) -> None:
        """
        Splits data into "training" and testing data, with testing data length equal to
        the number of data points in the selected time horizon and training data equal
        to the number of data points in the selected time period minus the time horizon.
        
        Uses the training data to calculate volatility and expected returns and then
        uses those inputs to run a simulation with the first value in the testing 
        data period.

        Uses the testing data to chart price paths predicted by the Monte Carlo 
        simulator using the training inputs against the actual prices observed over 
        the testing period.

        Parameters:
            asset_symbol - a ticker symbol for a financial asset (e.g., 'AAPL')
            period - the period of historical asset, market, and risk-free rate, data
                that the user would like to use in the calculations and simulation
            exp_ret_flag - a string holding the returns calculation method used to
                predict future asset returns (e.g., 'Dividend Discount Model')
            time_horizon - the future period to be forecasted by the Monte Carlo 
                simulation (in months)
            n_simulations - the number of simulations the user would like to run
            standev_window - the number of days used to calculate the rolling standard 
                deviation of asset prices 
            market_symbol - a ticker symbol for a market index (e.g., '^GSPC')
            rfr_symbol - a ticker symbol for a 'risk-free' asset (e.g, '^IRX')

        Returns: None; this method calls self.notify() to notify observers
            of simulation results. Observers then display results or any error 
            messages encountered by this function 
        """
        # Run as protected code to handle exceptions
        try: 
            # Populating primary data fields for future calculations and simulation
            self.populate_data(asset_symbol, market_symbol, rfr_symbol, period, exp_ret_flag)

            # Get correct clost column label
            close_col = price_col_checker(self.financial_asset.asset_data)

            # Set the starting index for the testing data equal to the investment horizon 
            # The investment time horizon is divided by the time measure 
            # (months, days, years) divided by the number of trading days in a year
            test_start_index = round(time_horizon / (MONTHS_PER_YEAR/ANNUAL_TRADING_DAYS)) 

            # If chosen period is shorter than time horizon, abort function, output error message
            if test_start_index > self.financial_asset.asset_data.index.size:
                raise Exception('Chosen time period must be greater than investment horizon for training data comparison.')

            # Split the asset data into training data and testing data
            asset_train = self.financial_asset.asset_data[close_col].iloc[:-test_start_index]
            asset_test = self.financial_asset.asset_data[close_col].iloc[-test_start_index:]

            # Use the training data to calculate simulation inputs for the model
            self.financial_asset.his_vol= calc_volatility(asset_train, standev_window)
            self.financial_asset.expected_returns = calc_exp_returns(
                financial_asset=self.financial_asset,
                market_index=self.market_index,
                risk_free_sec=self.risk_free_sec,
                end_index= -test_start_index # The ending index of the training data
                )
            
            # Run the simulation using the training calculation outputs
            train_sim = self.monte_carlo_sim(
                initial_price=asset_test.iloc[0, 0],
                expected_returns=self.financial_asset.expected_returns,
                his_vol=self.financial_asset.his_vol,
                time_horizon=time_horizon,
                n_simulations=n_simulations
            )

            # Visualize training data against testing data
            self._backtest_figure = backtest_vis(train_sim, asset_test)
            
            self.notify()

        # Notify observers if an exception occurred
        except Exception as e: 
            # If no exception message has been set, use generalized message
            if self.error_message == None:
                self.error_message = f'An exception occurred: {e}'

            self.notify()

    def monte_carlo_sim(self,
            initial_price: float,
            expected_returns: float,
            his_vol: float,
            time_horizon: int,
            n_simulations: int = 1000
            ) -> np.ndarray:
        """
        Returns future stock price predictions using the Geometric Brownian Motion
        model:

        Price(t) = Price(0) * e^(Return - 0.5*Volatility**2)*t+Volatility * Brownian Motion
            Where:
                Price(t) is the price at time t
                Price(0) is the starting price
                e is Euler's number
                Return is the expected return of the market
                Volatility is calculated as the standard deviation of returns
                Brownian Motion is simulated using a log-normally distributed random 
                variable

        Parameters:
            his_asset_data - a pandas.DataFrame containing historic asset data
            expected_returns - a floating point number representing the expected returns of
                the asset
            his_vol - a floating point number representing the asset's volatility
            time_horizon - the future period to be forecasted by the Monte Carlo 
                simulation (in months)
            n_simulations - the number of simulations to be run    

        Returns: An ndarray containing simulated future prices of the asset
        """

        # Verify arguments are of the correct type
        if not isinstance(initial_price, Number):
            self.error_message = f'"initial_price" must be a number, not {type(initial_price)}'
            raise TypeError
        elif not isinstance(expected_returns, Number):
            self.error_message = f'"expected_returns" must be a number, not {type(expected_returns)}'
            raise TypeError
        elif not isinstance(his_vol, Number):
            self.error_message = f'"his_vol" must be a number, not {type(his_vol)}'
            raise TypeError
        elif not isinstance(time_horizon, Number):
            self.error_message = f'"time_horizon" must be a number, not {type(time_horizon)}'
            raise TypeError
        elif not isinstance(n_simulations, Number):
            self.error_message = f'"n_simulations" must be a number, not {type(n_simulations)}'
            raise TypeError

        # Verify that arguments are within the expected range
        if initial_price < 0:
            self.error_message = f'"initial_price" must be positive, not {initial_price}'
            raise ValueError
        if his_vol < 0:
            self.error_message = f'"his_vol" must be positive, not {his_vol}'
            raise ValueError
        if time_horizon <= 0:
            self.error_message = f'"time_horizon" must be greater than zero, not {time_horizon}'
            raise ValueError
        if n_simulations <= 0:
            self.error_message = f'"n_simulations" must be greater than zero, not {n_simulations}'
            raise ValueError

        # Set the number of trading days to match the time_horizon
        num_steps = round(time_horizon / (MONTHS_PER_YEAR/ANNUAL_TRADING_DAYS))

        # The proportion of the time horizon each step represents (dt) 
        # Used to scale results as distance from day zero increases
        step_size = 1/num_steps

        # Calculating the stochastic drift: The change in the average value
        # of a random process
        drift = expected_returns - 0.5 * his_vol**2

        # Get random normal distribution with the right scale and dimensions
        random_normal = np.random.normal(
            scale=np.sqrt(step_size),
            size=(n_simulations, num_steps)
            )

        # Take the cumulative sum of the normal distribution to simulate Brownian Motion
        brownian_motion = np.cumsum(random_normal, axis=1)

        # Populate time step data; does not start at index=0 because that is filled in
        # later with the initial price of the asset
        time_step = np.linspace(step_size, step_size, num_steps)
        time_steps = np.broadcast_to(time_step, (n_simulations, num_steps))

        # Calculate simulation results
        prices = initial_price * np.exp(drift * time_steps + his_vol * brownian_motion)

        # Insert initial price as the first value
        prices[0,:] = initial_price

        # Transpose data for visualizations
        return prices.transpose()

    @property
    def risk_free_sec(self) -> RiskFreeSecurity:
        return self._risk_free_sec

    @property
    def financial_asset(self) -> FinancialAsset:
        return self._financial_asset

    @property
    def market_index(self) -> MarketIndex:
        return self._market_index
    
    @property
    def backtest_figure(self) -> Figure:
        return self._backtest_figure

    @property
    def sim_figure(self) -> Figure:
        return self._sim_figure

    @property
    def error_message(self) -> str:
        return self._error_message

    @risk_free_sec.setter
    def risk_free_sec(self, risk_free_sec: RiskFreeSecurity) -> None:
        self._risk_free_sec = risk_free_sec

    @financial_asset.setter
    def financial_asset(self, financial_asset: FinancialAsset) -> None:
        self._financial_asset = financial_asset

    @market_index.setter
    def market_index(self, market_index: MarketIndex) -> None:
        self._market_index = market_index

    @error_message.setter
    def error_message(self, error_message: str) -> None:
        self._error_message = error_message
