
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import Figure

from monte_carlo_simulator.gui.inter.observer_inter import Observer


class SimVisFrame(ttk.Frame, Observer):
    """Frame for monte carlo visualization outputs of future performance"""

    def __init__(self, master):
        super().__init__(master, width=800, height=600)

    def update(self, subject) -> None:
        # Check if sim_data has been changed since last visualization run
        if isinstance(subject.sim_figure, Figure):
            
            # Plot data, show on the SimVisFrame
            sim_canvas = FigureCanvasTkAgg(subject.sim_figure, master=self)
            sim_canvas.draw()
            sim_canvas.get_tk_widget().grid(row=0, column=0)


class BacktestVisFrame(ttk.Frame, Observer):
    """
    Data visualization frame. Displays output from Monte
    Carlo simulations for training and testing data.
    """

    def __init__(self, master):
        super().__init__(master, width=700, height=400)

    def update(self, subject):
        # Check if historical asset price data matches most recent visualization
        # and that no errors occurred 
        if isinstance(subject.backtest_figure, Figure):

            # Embed the plot in the tkinter window
            backtest_canvas = FigureCanvasTkAgg(subject.backtest_figure, master=self)
            backtest_canvas.draw()
            backtest_canvas.get_tk_widget().grid(row=0, column=0)