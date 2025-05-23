
from typing import List
from matplotlib.figure import Figure

from monte_carlo_simulator.model import *
from monte_carlo_simulator.data_fetcher import MarketDataFetcher
from monte_carlo_simulator.service.interface.subject_inter import Subject


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
