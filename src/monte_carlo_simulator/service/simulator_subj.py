
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
