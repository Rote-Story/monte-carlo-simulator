
import tkinter as tk
from tkinter import ttk

class RadioButtonFrame(ttk.Labelframe):
    """Radiobutton to choose which method for calculating expected returns"""

    def __init__(self, master):
        super().__init__(master, text='Select a method to calculate expected returns')
        self.calc_var = tk.StringVar() # Variable to hold selected radio button value
        self.create_rbutton_labels()
        self.create_rad_buttons()
        self.calc_var.set('Capital Asset Pricing Model')


    def create_rbutton_labels(self):
        """Labels to describe each calculation method"""

        # Capital Asset Pricing Model label
        self.capm_label = ttk.Label(
            self,
            text='risk-free rate + beta * (expected market returns - risk-free rate)'
            )

        # Dividend Discount Model label
        self.ddm_label = ttk.Label(
            self,
            text='(expected dividend / current price) + expected dividend growth rate'
            )

        # Simple Average Returns label
        self.simple_avg_label = ttk.Label(
            self,
            text='Calculates the unweighted average for the selected average window period'
            )
        
        # Weighted Average Returns label
        self.weighted_avg_label = ttk.Label(
            self,
            text='Calculates weighted average; more recent values are more heavily weighted'
            )

        # Positioning widgets on the frame
        self.capm_label.grid(row=1, column=1, padx=5, pady=5, sticky='w')        
        self.ddm_label.grid(row=2, column=1, padx=5, pady=5, sticky='w')       
        self.simple_avg_label.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.weighted_avg_label.grid(row=5, column=1, padx=5, pady=5, sticky='w')

    def update_selection(self):
        """Updates the variable to match the selection"""
        self.selected_value = self.calc_var.get()
        self.master.hide_input(self.selected_value)

    def create_rad_buttons(self):
        """Creates the radio buttons for the expected returns calculations"""
        
        self.capm_button = ttk.Radiobutton(
            self,
            text='Capital Asset Pricing Model',  
            variable=self.calc_var,
            value='Capital Asset Pricing Model',
            command=self.update_selection,
            )

        self.ddm_button = ttk.Radiobutton(
            self,
            text='Dividend Discount Model', 
            variable=self.calc_var,
            value='Dividend Discount Model',
            command=self.update_selection,
            )

        self.simple_avg_button = ttk.Radiobutton(
            self,
            text='Simple Average Returns', 
            variable=self.calc_var,
            value='Simple Average Returns',
            command=self.update_selection,
            )
        
        self.weighted_avg_button = ttk.Radiobutton(
            self,
            text='Exponential Weighted Average Returns', 
            variable=self.calc_var,
            value='Exponential Weighted Average Returns',
            command=self.update_selection,
            )

        # Positioning buttons on the grid
        self.capm_button.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.ddm_button.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.simple_avg_button.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.weighted_avg_button.grid(row=5, column=0, padx=5, pady=5, sticky='w')
