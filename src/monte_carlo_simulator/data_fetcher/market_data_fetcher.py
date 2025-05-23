
import pandas as pd
import yfinance as yf
from requests.exceptions import RequestException, HTTPError

from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter


class MarketDataFetcher:
    """
    Fetches market data: stocks, bonds, indexes, etcetera.
    Uses CachedLimiterSession to reduce number of requests and
    save previously fetched data.
    """

    def __init__(self, cached_limiter_session):
        self._session = cached_limiter_session
        self._error_message: str = None
    
    def fetch_ticker_object(self, ticker_symbol: str) -> yf.Ticker | None:
        """
        Validates the ticker_symbol, checks that it is accessible through yfinance.
        
        Parameters: 
            ticker_symbol - a valid ticker symbol like 'IBM' or 'AAPL'
            output_queue - a queue to coordinate operations between functions
        
        Returns: yf.Ticker corresponding to ticker_symbol if ticker_symbol 
            valid | error_message if ticker_symbol invalid
        """
        # Main error checking block, ticker validation, connection testing
        try:
            ticker = yf.Ticker(ticker_symbol, session=self._session)

            # Check if input value is a valid ticker symbol
            if not ticker.get_info():
                raise Exception('Missing ticker info.')
            
            return ticker # Return ticker symbol
        
        except HTTPError as http_err:
            self._error_message = f'An HTTP error ocurred: {http_err}'
            
        except RequestException as req_err:
            self._error_message = f'A request exception ocurred: {req_err}'
            
        except Exception as e:
            # Send generalized exception message  
            self._error_message = f'An error ocurred: {e}'
        
    def fetch_historic_div(self, ticker_object: yf.Ticker) -> pd.Series | None:
        """
        Retrieves historic dividend payments info.
        Function assumes that yf.Ticker object has already been validated.

        Parameters: ticker_object - a yf.Ticker object 

        Returns: a pandas.Series containing historical dividend payments
        """
        try: # Check if this security has a dividend rate
            ticker_object.get_info()['dividendRate']
    
        except KeyError:
            self._error_message = f'Ticker object missing key value: Dividend Rate'
            return None # Exit function to prevent entering next try-except block

        try: # Retrieve dividends payment history if it exists
            dividends = ticker_object.get_dividends()
            if dividends.empty:
                raise ValueError

            return dividends # Return divident payment history

        except ValueError:
            self._error_message = 'No dividend payment history found for this ticker'
            
        except RequestException as req_err:
            self._error_message = f'A request ocurred: {req_err}'

        except Exception as e:
            # Send generalized exception message  
            self._error_message = f'An error ocurred: {e}'   

    def fetch_asset_data(self, ticker_symbol: str, period: str ='5y') -> pd.DataFrame | None:
        """
        Fetches asset data corresponding to the ticker_symbol string.

        Parameters: 
            ticker_symbol - a valid asset ticker symbol string
            period - a string representing the desired historical data period

        Returns: a pandas.DataFrame object containing historical asset data
        """
        try:
            # Fetches historical data for the stock
            asset_data = yf.download(
                ticker_symbol,
                session=self._session,
                period=period
                )

            if asset_data.empty:
                raise ValueError
            
            return asset_data

        except ValueError:
            self._error_message = f'No data found for this ticker: {ticker_symbol}'
            
        except HTTPError as http_error:
            self._error_message = f'An HTTP error occurred: {http_error}'

        except RequestException as req_err:
            self._error_message = f'A request exception ocurred: {req_err}'

        except Exception as e:
        # Send generalized exception message  
            self._error_message = f'An error occurred: {e}'


    def fetch_market_data(self, market_symbol: str, period: str = 'max') -> pd.DataFrame | None:
        """
        Fetches returns of the 'broader market,' typically approximated 
        by market index securities like the S&P 500 (^GSPC).

        Parameters: 
            market_symbol - a valid market index symbol string
            period - a string representing the desired historical data period

        Returns: A DataFrame containing data for the chosen market index
        """

        try:
            # Get historic market returns
            market_data = yf.download(
                market_symbol,
                session=self._session,
                period=period
            )
            if market_data.empty:
                raise ValueError
            
            # Successful market_data fetch
            return market_data
            
        except ValueError:
            self._error_message = f'No data found for this ticker: {market_symbol}'
        
        except HTTPError as http_error:
            self._error_message = f'An HTTP error ocurred: {http_error}'

        except RequestException as req_err:
            self._error_message = f'A request exception ocurred: {req_err}'
        
        except Exception as e:
        # Send generalized exception message  
            self._error_message = f'An error ocurred: {e}'        


    def fetch_rfr_data(self, rf_sec_symbol: str, period: str='max') -> pd.DataFrame | None:
        """
        Fetches the historical returns for the treasury securities as a
        standin for the 'risk-free' rate.
        Assumes that calling function will handle exceptions and retrieve 
        error_message to display to users.

        Valid Treasury ticker symbols:
            (^IRX: 13-week, ^FVX: 5-year, ^TNX: 10-year, ^TYX: 30-year)
            
        Parameters: 
            rf_sec_symbol - a string with a risk-free security symbol (e.g., 'IRX')
            period - a string containing the time period to fetch rfr_data for
        
        Returns: A pandas.DataFrame containing risk-free rate data for the selected period
        """
        try:
            # Getting rates for security standing in for 'risk-free'
            risk_free_rate = yf.download(
                rf_sec_symbol,
                session=self._session,
                period=period
            )
            if risk_free_rate.empty:
                raise ValueError  
            
            # Successful risk_free_rate fetch
            return risk_free_rate

        except ValueError:
            self._error_message = f'No data found for this ticker: {rf_sec_symbol}'

        except HTTPError as http_error:
            self._error_message = f'An HTTP error ocurred: {http_error}'

        except RequestException as req_err:
            self._error_message = f'A request exception ocurred: {req_err}'

        except Exception as e:
            # Send generalized exception message  
            self._error_message = f'An error ocurred: {e}'

    
    @property
    def error_message(self) -> str:
        return self._error_message


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    """
    Class combining functionality of CacheMixn, LimiterMixin, and 
    Session, to reduce the burden on yahoo finance's servers and 
    lower the chances of being IP blocked.
    Singleton session function: maintains only one session instance.
    """
    _session = None
    
    def __init__(self, limiter, bucket_class, backend):
        if CachedLimiterSession._session is not None:
            raise Exception('This is a Singleton class. Use get_session() to retrieve an instance instead.')
        else:
            super().__init__(limiter=limiter, bucket_class=bucket_class, backend=backend) 

    @staticmethod
    def get_session():
        """
        Instantiates a new session only if one does not already exist.
        """
        if CachedLimiterSession._session is None:
            CachedLimiterSession._session = CachedLimiterSession(
            limiter=Limiter(RequestRate(2, Duration.SECOND * 5)),  # max 2 requests per 5 seconds
            bucket_class=MemoryQueueBucket,
            backend=SQLiteCache('yfinance.cache'),
            )
        return CachedLimiterSession._session
