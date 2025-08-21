# 🎲 Monte Carlo Simulator Desktop Application

> ⚠️ **Work in Progress**  
> This is an ongoing learning project exploring Monte Carlo simulations using Python. While the core features are functional, development is still in progress. Feedback is welcome!

---

## 📊 Description

This desktop application runs Monte Carlo simulations for financial assets (e.g., stocks) using historical data from Yahoo Finance. It provides a GUI interface built with `tkinter`, along with data visualization using `matplotlib` and `seaborn`.

Monte Carlo simulations aim to estimate a range of possible future asset prices by using current price, historical volatility, and expected return to simulate thousands of random price paths.

### 🧠 Important Notes & Assumptions:
- Historical volatility is assumed to be predictive of future volatility.
- Expected returns are assumed to be known or estimable (e.g., via CAPM).
- Forecasts are only as good as the data and assumptions behind them.
- Model assumptions (beta, volatility, risk-free rate, etc.) are shown in-app for transparency.

> 🧪 This model is **not intended for financial decision-making**. It's a tool for exploration and learning.

---

## 🧰 Installation

### Prerequisites

- Python 3.10 or higher: [Download Python](https://www.python.org/downloads/)
- Poetry package manager: [Install Poetry](https://python-poetry.org/docs/)
- See dependencies listed in `pyproject.toml`

### Install Steps

1. Clone the repository and navigate to the project directory.
2. Ensure `pyproject.toml` and `poetry.lock` are present.
3. Install dependencies:

   ```bash
   poetry install
   ```
--- 

## 🖥️ Usage Overview

The app GUI includes four main widgets:

#### **1. Input Panel**

   Enter:
   - Ticker symbol (e.g., AAPL)
   - Investment time horizon (years)
   - Historical timeframe for training data
   - Standard deviation period (days)

#### **3. Backtest Panel**
Shows predicted vs. actual historical performance (for a held-out test set).

#### **4. Forecast Panel**
Displays future price simulations based on the full dataset, showing price paths within ±2 standard deviations.

#### **5. Assumptions Panel**

Lists key model assumptions such as:
- Beta
- Historic volatility
- Risk-free rate
- Expected returns

> ⚠️ The simulation assumes log-normal price behavior and Brownian Motion. It is not suitable for mean-reverting assets like bonds or any asset without meaningful daily closing prices on Yahoo Finance.

---

## 🐛 Issue Submissions

If you encounter bugs, have questions, or want to suggest improvements, feel free to reach out via:
- 📧 Email: triberry@yahoo.com
- 💬 GitHub: @Rote-Story
I believe programming is a continuous learning process—your insights are welcome!



## 📄 License
This project is licensed under the MIT License.



## 🙏 Acknowledgments
Special thanks to the developers behind:
- yfinance
- matplotlib, seaborn, numpy, tkinter, pandas, scipy
- UI styled using sv-ttk

These tools made this project possible.
