
import tkinter as tk
import sv_ttk

from monte_carlo_simulator.gui import *
from monte_carlo_simulator.model import Stock, MarketIndex, RiskFreeSecurity
from monte_carlo_simulator.service import Simulator
from monte_carlo_simulator.data_fetcher import MarketDataFetcher, CachedLimiterSession

if __name__ == '__main__':

    # Create session to manage requests
    session = CachedLimiterSession.get_session()

    # Instantiate data fetcher to get yfinance data
    data_fetcher = MarketDataFetcher(session)

    # Instantiate data storage classes
    financial_asset = Stock()
    market_index = MarketIndex()
    risk_free_security = RiskFreeSecurity()

    # Instantiate main subject class
    monte_carlo_sim_subject = Simulator(
        market_data_fetcher=data_fetcher,
        financial_asset=financial_asset,
        market_index=market_index,
        risk_free_sec=risk_free_security
        )
    
    # Set up root GUI window
    root = tk.Tk()
    root.title('Monte Carlo Simulator')

    # Set GUI theme
    sv_ttk.set_theme('dark')

    # Create primary simulation frame, pack it so that it behaves like the window background
    sim_frame = SimFrame(root, simulator=monte_carlo_sim_subject)
    sim_frame.pack(fill='both', expand=True)

    # Create GUI frames
    button_frame = ButtonFrame(sim_frame)
    error_frame_obs = ErrorFrame(sim_frame)
    radio_button_frame = RadioButtonFrame(sim_frame)
    assumptions_frame_obs = AssumptionsFrame(sim_frame)
    sim_vis_frame_obs = SimVisFrame(sim_frame)
    asset_vis_frame_obs = BacktestVisFrame(sim_frame)
    input_frame = InputFrame(sim_frame)

    # Create gui buttons
    sim_button = SimButton(
        master=button_frame, 
        run_sim_func=sim_frame.run_forecast
        )
    asset_button = BacktestButton(
        master=button_frame, 
        backtest_func=sim_frame.run_backtest_sim
        )

    # Set up buttons on button frame
    button_frame.setup_buttons(asset_button, sim_button)
    
    # Set up frames on main simulation frame
    sim_frame.setup_frames(button_frame, 
                    error_frame_obs, 
                    radio_button_frame, 
                    assumptions_frame_obs, 
                    sim_vis_frame_obs, 
                    asset_vis_frame_obs, 
                    input_frame
                    )
    
    # Attach observers to subject
    monte_carlo_sim_subject.attach(assumptions_frame_obs)
    monte_carlo_sim_subject.attach(sim_vis_frame_obs)
    monte_carlo_sim_subject.attach(asset_vis_frame_obs)
    monte_carlo_sim_subject.attach(error_frame_obs)

    # Set the minimum size for the window and center it on the screen
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry(f'+{x_cordinate}+{y_cordinate-20}')

    # Run application
    root.mainloop()