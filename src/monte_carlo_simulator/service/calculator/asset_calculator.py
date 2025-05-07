
import pandas as pd
from pandas import DataFrame

from monte_carlo_simulator.model.financial_asset import FinancialAsset
from monte_carlo_simulator.model.market_index import MarketIndex
from monte_carlo_simulator.model.risk_free_security import RiskFreeSecurity
from monte_carlo_simulator.service.calculator.market_calculator import calc_market_returns, calc_rfr
from monte_carlo_simulator.service.util.price_col_checker import price_col_checker


def calc_exp_returns(
        financial_asset: FinancialAsset,
        market_index: MarketIndex = None,
        risk_free_sec: RiskFreeSecurity = None,
        end_index: int = -1,
        returns_window: int = 150
        ) -> float:
    """
    Calculates expected returns based on user's chosen method.
    Assumes that all market, risk-free rate, and asset data has been fetched
    and stored in the Simulator class.
    Assumes that asset_symbol and market_symbol are valid.
    Assumes that function is being called after market, risk-free rate, and asset data
    have been populated.

    Calculation Methods:
        Dividend Discount Model: only works for assets that pay a dividend
        Capital Asset Pricing Model: Fetches 5 years of asset and market data
            in order to calculate beta
        Simple Average: Takes the average of returns over the specified period
        Weighted Average: Takes the average of returns over the specified period
            weighted so that more recent observations have a greater impact on the 
            final returns calculation 

    Parameters: 
        financial_asset - A FinancialAsset data storage object 
        market_index - A MarketIndex data storage object
        risk_free_sec - A RiskFreeSecurity data storage object
        end_index - An integer representing the ending index value to be included
            in expected returns calculations; used to exclude testing data from calculations.
            Includes all values if no ending index is specified
        returns_window - An integer representing the days used to calculate average or 
            weighted average returns

    Returns: A float with the expected returns calculated by the chosen method
    """
    
    match financial_asset.exp_ret_flag: # User's chosen expected returns calculation method
        
        case 'Dividend Discount Model': # Dividend Discount model works only for assets that pay a dividend
            # Convert ending index into a date so that the closest available dividend payment date can be 
            # selected from historic dividends
            end_date = financial_asset.asset_data.index[end_index]
            
            # Fetch dividend growth rate for calculations
            financial_asset.div_growth_rate = calc_div_growth_rate(
                his_div=financial_asset.his_div.loc[:end_date])
            
            close_col = price_col_checker(financial_asset.asset_data) # Get correct close column label
            
            recent_price = financial_asset.asset_data[close_col].iloc[-1, -1] # Get most recent asset price

            # Calculate expected returns, dividend growth rate
            annual_expected_returns = ddm_returns(
                recent_price=recent_price,
                div_growth_rate=financial_asset.div_growth_rate)
            
        case 'Capital Asset Pricing Model': # beta calculation relies on having market data fetched       
            # Calculate beta, storing it in class attribute
            financial_asset.beta = calc_beta(
                asset_data=financial_asset.asset_data.iloc[:end_index],
                market_data=market_index.market_data.iloc[:end_index]
                )
            
            # Calculate market returns
            market_index.market_returns = calc_market_returns(market_index.market_data.iloc[:end_index])

            # Calculate risk-free rate
            risk_free_sec.risk_free_rate = calc_rfr(risk_free_sec.rfr_data.iloc[:end_index])

            # Calculate expected returns 
            annual_expected_returns = capm_returns(
                beta=financial_asset.beta,  
                market_returns=market_index.market_returns,
                risk_free_rate=risk_free_sec.risk_free_rate
                )

        case 'Simple Average Returns':
            # Calculate expected returns
            annual_expected_returns = average_returns(
                asset_data=financial_asset.asset_data.iloc[:end_index],
                returns_window=returns_window)
            
        case 'Exponential Weighted Average Returns':
            # Calculate expected returns
            annual_expected_returns = exponential_weighted_average(
                asset_data=financial_asset.asset_data.iloc[:end_index],
                returns_window=returns_window)

    return annual_expected_returns

def capm_returns(beta: float, market_returns: float, risk_free_rate: float) -> float:
    """
    Estimates expected return by using that capital asset pricing model (capm).

    Equation: Rf + Beta(Rm - Rf)
        Rf = risk-free rate
        Beta = measure of stock volatility relative to the rest of the market
        Rm = expected market return'

    Parameters: beta - a float representing the asset's beta value
        market_returns - a float representing the returns of a chosen market index
        risk_free_rate - a float representing the return of a 'risk-free' asset

    Returns: The annual expected returns (float)
    """
    
    # Set expected_returns estimate to output of CAPM
    expected_returns = risk_free_rate + beta * \
        (market_returns - risk_free_rate)

    return expected_returns

def calc_div_growth_rate(his_div: pd.Series) -> float:
    # Select 10-year time frame for historical growth rate
    start_date = his_div.index[-1] - pd.DateOffset(years=10)

    # Calculate growth rate
    div_growth_rate = his_div.loc[str(start_date):] \
        .pct_change() \
        .mean()
    
    return div_growth_rate

def ddm_returns(recent_price: float, his_div: pd.Series, div_growth_rate: float) -> float:
    """
    Calculates the Dividend Discount Model returns

    Equation: E(r) = D1/P0 + g
        E(r): Expected return
        D1: Expected dividend per share next year
        P0: Current price per share
        g: Expected growth rate of dividends
    D1 - found by forecasting dividend payments for the next year.
    g - found by estimating growth rate based on historical growth rates.

    Assumptions: This method is only usable for companies with a stable divididend
    history, and is incompatible for firms in non-cyclical industries.

    Parameters:
        asset_ticker - a yfinance.Ticker object to get the most recent price data
        his_div - a pandas.Series containing historic dividend payment amounts and dates
        div_growth_rate - a floating point number representing the dividend growth rate,
            as calculated by the calc_div_growth_rate function

    Returns: The expected returns and the growth rate (float)
    """
    # Calculate expected dividend payments for the next year by applying the
    # growth rate to the most recent annual dividend amount
    expected_dividend = his_div.resample('YE').sum() * (1 + div_growth_rate) 

    ddm_returns = expected_dividend.iloc[-1]/recent_price + div_growth_rate

    return ddm_returns

def average_returns(asset_data: pd.DataFrame, returns_window: int = 150) -> float:
    """
    Calculates the simple average of returns over the given time window.
    
    Parameters: 
        asset_data - a pandas.Dataframe containing historic asset data
        window - an integer representing the number of days to be used for calculating 
            the moving average

    Returns: A float representing the unweighted average returns over the window
    """
    # Handle possible KeyErrors for market_data with only a 'Close' column
    close_column = price_col_checker(asset_data)

    # Calculating the average price change from start of window until most recent price
    his_avg = asset_data[close_column].iloc[-returns_window:] \
        .pct_change() \
        .mean() 
         

    return float(his_avg.iloc[0]) # Return only the element, not the index


def exponential_weighted_average(asset_data: pd.DataFrame,  returns_window: int = 150) -> float:
    """
    Uses historic adjusted stock price data to estimate future returns using
    a weighted average giving more 'weight' to more recent data points.

    Equation: EMA = (Adj(smoothing/(1+days))) + EMAt-1(1 - (smoothing/(1+days)))
        Adj = the adjusted closing price of the stock data for that day
        EMAt-1 = the EMA at t-1 where t is time in days (t-1 = yesterday's EMA) 
        smoothing = a smoothing factor to act as a multiplier for the weights.
        days = how many days since from the least recent observation.
            Example: Using a window of 200 would mean that at 200 days ago 
            days would equal 1 (days=1), and 1 day ago days would equal 200. 
    
    Parameters: 
        asset_data - a pandas.DataFrame containing historical asset data
        window - an integer representing the number of days to be used for calculating 
            the exponential moving average
    
    Returns: A float with the calculated expected returns based on the EMA
    """
    # Handle possible KeyErrors for market_data with only a 'Close' column
    close_column = price_col_checker(asset_data)

    pct_returns = asset_data[close_column].pct_change()

    # Use pandas DataFrame.ewm() (expeonential moving window) to calculate the exponential 
    # weighted average
    ema_returns = pct_returns.ewm(span=returns_window, adjust=False).mean()

    return float(ema_returns.iloc[-1, -1]) # Return only the element, not the index

def calc_beta(asset_data: DataFrame, market_data: DataFrame) -> float:
    """
    Calculates stock beta relative to a benchmark index like the S&P 500.
    Requires at least 5-years of historical asset_data and market_data to
    calculate beta.
    Resamples data to get monthly returns for beta calculations.
    Function assumes that ticker symbols have already been validated.

    Equation: Beta = Covariance(Rs, RI)/Variance(RI)
        RI = Returns of the market index
        Rs = Returns of the stock

    Parameters: 
        asset_data - a pandas.DataFrame object for the target asset
        market_ticker - a pandas.DataFrame object for the target asset
    
    Returns: A float containing the asset's beta value
    """
    # Verify both arguments are DataFrame objects
    if not isinstance(asset_data, DataFrame):
        raise TypeError(f'"asset_data" must be of type pandas.DataFrame, not {type(asset_data)}')
    elif not isinstance(market_data, DataFrame):
        raise TypeError(f'"market_data" must be of type pandas.DataFrame, not {type(market_data)}')

    # Get start of date of asset data to ensure periods match
    start_date = asset_data.index[0]

    # Handle possible KeyErrors for market_data with only a 'Close' column
    close_column = price_col_checker(market_data)

    # Get benchmark returns from monthly market index percent changes in price
    benchmark_returns = market_data.loc[str(start_date):][close_column].iloc[:, 0] \
        .resample('ME') \
        .last() \
        .pct_change() \
        .dropna()
    
    # Calculate variance of benchmark returns
    benchmark_variance = benchmark_returns.var()

    # Calculate covariance between the market and the stock as a percent change
    asset_cov =  benchmark_returns.cov(
        asset_data.loc[str(start_date):][close_column].iloc[:, 0] \
                .resample('ME') \
                .last() \
                .pct_change() \
                .dropna()
                )

    # Return calculated beta
    return asset_cov / benchmark_variance