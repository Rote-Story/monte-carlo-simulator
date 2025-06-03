
import tkinter as tk
from tkinter import ttk

from monte_carlo_simulator.service.interface.subject_inter import Subject


class SimFrame(ttk.Frame):
    """
    Main simulation GUI window. Contains user I/O frames arranged
    in a grid format.
    """

    def __init__(self, master: tk.Tk, simulator: Subject):

        super().__init__(master=master, height=1000, width=1525)
        self.simulator = simulator

