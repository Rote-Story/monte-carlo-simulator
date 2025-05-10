

import pandas as pd


def price_col_checker(df: pd.DataFrame) -> str:
    """
    Determines whether the downloaded price data has an 'Adj Close'
    column or just a 'Close' column.

    Parameters: df - a dataframe containing historical asset price data
    
    Returns: A str that can be used to access the appropriate 
        price column for the corresponding dataset.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f'df must be of type pandas.Dataframe, not {type(df)}')
    
    elif 'Adj Close' not in df.keys() and 'Close' not in df.keys():
        raise ValueError(f'df must have a "Close" or "Adj Close" column.\ndf column names: {df.keys()}')

    elif 'Adj Close' in df.keys():
        close_column = 'Adj Close'
    
    else:
        close_column = 'Close'

    return close_column