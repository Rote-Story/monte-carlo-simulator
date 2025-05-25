
from typing import List
from matplotlib.figure import Figure
from numbers import Number
import numpy as np

from monte_carlo_simulator.model import *
from monte_carlo_simulator.data_fetcher import MarketDataFetcher
from monte_carlo_simulator.service.interface.subject_inter import Subject
from monte_carlo_simulator.const import ANNUAL_TRADING_DAYS, MONTHS_PER_YEAR

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
        self._train_test_figure: Figure = None
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
    def train_test_figure(self) -> Figure:
        return self._train_test_figure

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
