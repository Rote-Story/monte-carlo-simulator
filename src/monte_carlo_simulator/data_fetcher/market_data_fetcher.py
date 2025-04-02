
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
        self.session = cached_limiter_session

    
    def validate_ticker(self, ticker_symbol: str):
        """
        Validates that the ticker_symbol is valid and is accessible through yfinance.
        params: ticker_symbol - a valid ticker symbol like "IBM" or "TNX"
            output_queue - a queue to coordinate operations between functions
        return: True if ticker symbol valid, error_message string otherwise
        """
        # Main error checking block, ticker validation, connection testing
        try:
            yf
            ticker = yf.Ticker(ticker_symbol, session=self.session)
            # Check if input value is a valid ticker symbol
            if not ticker.get_info():
                raise yf.exceptions.YFTickerMissingError
        
        except yf.exceptions.YFTickerMissingError as ticker_missing_error:
            error_message = f"An error occurred: {ticker_missing_error}"
            return error_message
        
        except HTTPError as http_err:
            error_message = f"An HTTP error occurred: {http_err}"
            return error_message

        except RequestException as req_err:
            error_message = f"A request exception ocurred: {req_err}"
            return error_message

        except Exception as error:
            # Send generalized exception message  
            error_message = f"An error occurred: {error}"
            return error_message

        else:
            return True

    def fetch_asset_info(self, ticker_symbol: str):
        """
        Retrieves info from stock ticker, primary error or invalid
        symbol check
        params: ticker_symbol - a valid ticker symbol of type str
        return: yf.Ticker corresponding to ticker_symbol if ticker_symbol 
            valid | error_message if ticker_symbol invalid
        """
        # Check to ensure ticker symbol is valid
        result = self.validate_ticker(ticker_symbol)

        if result == True: # Valid ticker_symbol
            return yf.Ticker(ticker_symbol, session=self.session)
        else: # Ticker_symbol invalid, return error message
            return result
        
    def fetch_dividends(self, ticker_object: yf.Ticker):
        """
        Retrieves historic dividend payments info.
        Function assumes that yf.Ticker object has already been validated.
        params: ticker_object a yf.Ticker object 
        return: a pandas.Series containing historical dividend payments
        """
        try: # Check if this security has a dividend rate
            ticker_object.get_info()["dividendRate"]
            
        except KeyError:
            error_message = f"Ticker object missing key value: Dividend Rate"
            return error_message
        
        try: # Retrieve dividends payment history if it exists
            dividends = ticker_object.get_dividends()
            if dividends.empty:
                raise ValueError

        except ValueError:
            error_message = "No dividend payment history found for this ticker"
            return error_message
        
        except RequestException as req_err:
            error_message = f"A request ocurred: {req_err}"
            return error_message

        else: 
            return dividends

class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    """
    Class combining functionality of CacheMixn, LimiterMixin, and 
    Session, to reduce the burden on yahoo finance's servers 
    and lower the chances of being IP blocked.
    """

session = CachedLimiterSession(
    limiter=Limiter(RequestRate(2, Duration.SECOND * 5)),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
    )
