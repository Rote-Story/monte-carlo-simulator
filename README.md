# Project Title

Monte Carlo Simulator Desktop Application

## Description

This app is designed to run Monte Carlo simulations for securities like stocks using data from yahoo finance. Financial asset information is downloaded using the yfinance module and displayed using tkinter gui as well as matplotlib and seaborn charts. Monte Carlo simulations aim to capture the range of likely future possibilities by using the standard deviation, current value, and expected future returns to simulate different price movements from today until the end of the investment horizon. This model is meant to give a sense of future asset price movements, but like all models, its forecasting ability is limited by the information underpinning its assumptions. For example, it assumes that historical volatility will be a good predictor of future volatility, and that expected future returns can be accurately estimated. Estimators of future returns, like the Capital Asset Pricing Model, have their own limitations which impact the accuracy of the final result. Many of the assumptions made by the model are displayed upon running the simulation so that the user can take these into account when assessing the accuracy and usefulness of the model's output.

## Installation

### Prerequisites:

- Python 3.10 or higher
  - Python can be downloaded from the [Python Download Page](https://www.python.org/downloads/) (external link)
- Python Modules:
  - yfinance (>=0.2.55,<0.3.0)
  - seaborn (>=0.13.2,<0.14.0)
  - pandas (>=2.2.3,<3.0.0)
  - scipy (>=1.15.2,<2.0.0)
  - numpy (>=2.2.4,<3.0.0)
  - matplotlib (>=3.10.1,<4.0.0)
  - requests-cache (>=1.2.1,<2.0.0)
  - pyrate-limiter (<3.0)
  - requests-ratelimiter (>=0.7.0,<0.8.0)
  - sv-ttk (>=2.6.0,<3.0.0)
  - mplfinance (>=0.12.10b0,<0.13.0)

### Requirements Installation

Specfic versions of the prerequesite packages can be found in the `requirements.txt` file. These can be installed using the following steps:

1. **Ensure you have the `requirements.txt` file** in your project directory.

2. **Install dependencies**

- **For Windows or macOS/Linux**: `bash pip install -r requirements.txt`

## Usage

The GUI has four primary widgets:

1. The first widget is an input window for the ticker symbol (string), investment time horizon in years (int), historical timeframe to use in calculations, and the desired timeframe in days used calculate the standard deviation (int).
2. The second widget displays actual historical asset performance matching the investment time horizon - the testing period - charted against predicted price paths based on training data which predates the testing period.
3. The third widget is the future simulation output, which uses the full range of available data to forecast future performance and display the range of predicted price paths falling within two standard deviations of the mean.
4. The fourth widget displays the assumptions used to generate the simulation, things like beta, historic volatility, the "risk-free rate," and the expected returns on the security.

The simulator uses a normal distribution to simulate Brownian Motion, meaning that it is unsuitable for asset classes that have a tendency to revert to the mean, like bonds, whose valuation trends closer to the par value as the bond approaches its maturity date. It is assumed that the chosen security has the "Close" and "Adj Close" listed on Yahoo Finance as daily security prices, securities like U.S. treasuries are unsuitable due to their "Close" being listed as the annual interest rate rather than the price of the security. Additionally,

## Issue Submissions

To submit any suggestions for improvement, questions, reports of bugs or other issues, please email me or send me a message on github (contact information below). I believe that programming and software development are a lifelong learning process, and there is always room to grow and improve.

## Contact Information

Email: [triberry@yahoo.com](triberry@yahoo.com)
GitHub: [Rote-Story](https://github.com/Rote-Story)

## License

Distributed under an MIT license.

## Acknowledgments

This project relied heavily on the yfinance, matplotlib, seaborn, tkinter, numpy, and of course python libraries. Additionally, the styling relied on the sv-tkk module, These resources were invaluable for the creation of this application.
