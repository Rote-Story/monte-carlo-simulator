

# Global variable, the number of trading days in a year (approximately 252
# days)
ANNUAL_TRADING_DAYS = 252

# The measure to use for user time-frame inputs: 1=years, 12=months, 365=days.
# Used to calculate the number of trading days matching the entered investment
# time horizon.
YEAR = 1
MONTHS_PER_YEAR = 12 
DAYS_PER_YEAR = 365


# Time periods dictionary for processing user input
TIME_PERIODS = {
    'Last 1 day': '1d',
    'Last 5 days': '5d',
    'Last 1 month': '1mo',
    'Last 3 months': '3mo',
    'Last 6 months': '6mo',
    'Last 1 year': '1y',
    'Last 2 years': '2y',
    'Last 5 years': '5y',
    'Last 10 years': '10y',
    'Year to date': 'ytd',
    'Maximum available data': 'max'
    }

# Typical securities used for "risk-free" rate calculations
RFR_SECURITIES = {
    '13-week U.S. Treasuries' : '^IRX',
    '5-year U.S. Treasuries'  : '^FVX',
    '10-year U.S. Treasuries' : '^TNX',
    '30-year U.S. Treasuries' : '^TYX' 
    }

# Common market indexes; used as benchmark in calculations
MARKET_INDEXES = {
    'S&P 500' : '^GSPC',
    'Dow Jones' : '^DJI',
    'Russel 2000' : '^RUT',
    'NASDAQ 100' : '^NDQ',
    'NASDAQ Composite' : '^IXIC',
    'Wilshire 5000' : '^FTW5000',
    'NYSE Composite' : '^NYA',
    'S&P Global 1200' : '^SPG1200',
    'Índice de Precios y Cotizaciones': '^MXX',
    'Indice de Precios Selectivo de Acciones' : '^IPSA', 
    'CAC 40' : '^FCHI',
    'Hang Seng': '^HSI',
    'SSE Commposite' : '000001.SS',
    'CSI 300' : '000300.SS',
    'Nikkei 225' : '^N225',
    'KOSPI Composite' : '^KS11',
    'BSE SENSEX' : '^BSESN',
    'NIFTY 50' : '^NSEI',
    'FTSE 100' : '^FTSE',
    'DAX' : '^GDAXI',
    'IBEX' : 'IBEX',
    'EGX 30' : '^CASE 30'
    } 