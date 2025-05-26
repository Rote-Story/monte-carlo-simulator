
from matplotlib.figure import Figure
import numpy as np

from monte_carlo_simulator.const import ANNUAL_TRADING_DAYS, MONTHS_PER_YEAR


def monte_carlo_sim_vis(sim_data: np.ndarray, time_horizon: int = 12) -> Figure:
    """
    Visualizes monte carlo simulation results.
    Produces two plots, one mapping each simulation in a line plot with 
    markers for mean, as well as approximately 2 and 3 standard deviations
    from the mean.
    Assumes normallly distributed data.

    Parameters: 
        sim_data - a numpy array of forward-looking simulation output.
        test_sim_data - a numpy array of backward-looking simulation output
            for comparison with actual results, replicating the investment time
            horizon.
        asset_data - a pandas DataFrame containing price data extending backwards
            as far as the chosen investment time horizon.
        time_horizon - an integer indicating how far out the simulation 
            attempts to forecast.

    Returns: A Figure object with two plots: plot1 displays the simulated
        paths, and plot2 displays mean and percentile data.
    """
    global ANNUAL_TRADING_DAYS # The number of trading days in a year
    
    # Verify sim_data is a numpy array
    if not isinstance(sim_data, np.ndarray):
        raise TypeError(f'"sim_data" parameter must be an numpy.ndarray, not {type(sim_data)}')
   
    # Verify time_horizon is an integer
    elif not isinstance(time_horizon, int) or isinstance(time_horizon, bool):
        raise TypeError(f'"time_horizon" parameter must be an integer, not {type(time_horizon)}')
    
    # Verify time_horizon is positive
    elif time_horizon <= 0:
        raise ValueError(f'"time_horizon" parameter must be positive, not {time_horizon}')

    # Set visualization variables
    mean_prices = sim_data.mean(axis=1) # Mean of future price simulation
    one_std_below_mean = np.percentile(sim_data, 15.8665, axis=1) # -1 standard deviation below the mean
    one_std_above_mean = np.percentile(sim_data, 84.134, axis=1) # +1 standard deviation above the mean
    two_std_below_mean = np.percentile(sim_data, 2.275, axis=1) # -2 standard deviations below the mean
    two_std_above_mean = np.percentile(sim_data, 97.725, axis=1) # +2 standard deviations above the mean

    fig = Figure(figsize=(7, 4), facecolor='#1E1E1E') # Create figure object
    axs1 = fig.add_subplot(111) # Add subplot

    # Create Plot: Future Price prediction
    axs1.plot(mean_prices, label='Mean', color='#F3773E')
    axs1.fill_between(
        range(round(time_horizon / (MONTHS_PER_YEAR/ANNUAL_TRADING_DAYS))),
        one_std_below_mean,
        one_std_above_mean,
        color='#57C8FF',
        label='One Standard Deviation'
    )
    axs1.fill_between(
        range(round(time_horizon / (MONTHS_PER_YEAR/ANNUAL_TRADING_DAYS))),
        two_std_below_mean,
        two_std_above_mean,
        color='#0080BA',
        alpha=0.8,
        label='Two Standard Deviations'
    )
    axs1.set_title(
        'Future Price Simulation',
        color='white')

    # Set axis tick spacing, color, and labels for the plot
    axs1.set_xlabel('Trading Days', color='white')
    axs1.set_ylabel('Price in USD', color='white')
    axs1.set_xlim(-3, len(sim_data))
    axs1.set_ylim(two_std_below_mean.min() - 5, two_std_above_mean.max() + 5)
    axs1.tick_params(axis='x', colors='white')
    axs1.tick_params(axis='y', colors='white')

    # Set color, grid color and style for the plot
    axs1.set_facecolor('#2E2E2E')
    axs1.grid(color='#3E3E3E', linestyle='--')

    # Setup legend, adjust colors and size for graph for the plot
    legend = axs1.legend(loc='upper left', fontsize='small')
    for text in legend.get_texts():
        text.set_color('white')
    legend.get_frame().set_facecolor('#3E3E3E')

    return fig