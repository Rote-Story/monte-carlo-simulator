
from tkinter import ttk

from monte_carlo_simulator.gui.inter.observer_inter import Observer

class ErrorFrame(ttk.Frame, Observer):
    """Frame to display error and status messages"""

    def __init__(self, master):
        super().__init__(master)
        self.create_error_label()

    def create_error_label(self):
        # Label to output error messages, set on main grid
        self.error_label = ttk.Label(
            self,
            text=''
            )

        # Position error text output on grid
        self.error_label.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

    def update(self, subject):
        # Check if error_message is has been added
        if subject.error_message != None and type(subject.error_message) == str:

            # Show error message
            self.error_label.config(text=subject.error_message)

            # Reset error message
            subject.error_message=None