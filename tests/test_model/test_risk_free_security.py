
import unittest
from pandas import DataFrame
from pandas.testing import assert_frame_equal
import numpy as np

from monte_carlo_simulator.model import RiskFreeSecurity


class TestRiskFreeSecurity(unittest.TestCase):

    risk_free_sec = RiskFreeSecurity()
    test_dataframe = DataFrame(np.linspace(0.0, 3.0, num=5))
    test_zeros_dataframe = DataFrame(np.zeros((4, 4)))

    # Test his_data attributes
    def test_rfr_data_dataframe_input(self):
        self.risk_free_sec.rfr_data = self.test_dataframe
        assert_frame_equal(self.test_dataframe, self.risk_free_sec.rfr_data)

    def test_rfr_data_zeros_dataframe_input(self):
        self.risk_free_sec.rfr_data = self.test_zeros_dataframe
        assert_frame_equal(self.test_zeros_dataframe, self.risk_free_sec.rfr_data)

    def test_rfr_data_list_input(self):
        try:
            self.risk_free_sec.rfr_data = [[0, 0, 0, 0], [0, 0, 0, 0]]
        except TypeError as e:
            self.assertEqual(str(e), 'Historic risk-free rate data must be a pandas DataFrame object')
    
    def test_rfr_data_dict_input(self):
        try:
            self.risk_free_sec.rfr_data = {'zero': 0, 'one': 1}
        except TypeError as e:
            self.assertEqual(str(e), 'Historic risk-free rate data must be a pandas DataFrame object')
    
    def test_rfr_data_int_input(self):
        try:
            self.risk_free_sec.rfr_data = 0
        except TypeError as e:
            self.assertEqual(str(e), 'Historic risk-free rate data must be a pandas DataFrame object')

    def test_rfr_data_float_input(self):
        try:
            self.risk_free_sec.rfr_data = 0.0
        except TypeError as e:
            self.assertEqual(str(e), 'Historic risk-free rate data must be a pandas DataFrame object')

    def test_rfr_data_none_input(self):
        try:
            self.risk_free_sec.rfr_data = None
        except TypeError as e:
            self.assertEqual(str(e), 'Historic risk-free rate data must be a pandas DataFrame object')

    # Test rfr_symbol attributes
    def test_rfr_symbol_valid_str_input(self):
        self.risk_free_sec.rfr_symbol = '^GSPC'
        self.assertEqual('^GSPC', self.risk_free_sec.rfr_symbol)

    def test_rfr_symbol_white_space_str_input(self):
        try: 
            self.risk_free_sec.rfr_symbol = '       '
        except ValueError as e:
            self.assertEqual(str(e), 'Risk-free rate symbol must not be blank')

    def test_rfr_symbol_empty_str_input(self):
        try: 
            self.risk_free_sec.rfr_symbol = ''
        except ValueError as e:
            self.assertEqual(str(e), 'Risk-free rate symbol must not be empty')

    def test_rfr_symbol_list_input(self):
        try:
            self.risk_free_sec.rfr_symbol = [[0, 0, 0, 0], [0, 0, 0, 0]]
        except TypeError as e:
            self.assertEqual(str(e), 'Risk-free rate symbol must be a string object')
    
    def test_rfr_symbol_dict_input(self):
        try:
            self.risk_free_sec.rfr_symbol = {'zero': 0, 'one': 1}
        except TypeError as e:
            self.assertEqual(str(e), 'Risk-free rate symbol must be a string object')
    
    def test_rfr_symbol_int_input(self):
        try:
            self.risk_free_sec.rfr_symbol = 0
        except TypeError as e:
            self.assertEqual(str(e), 'Risk-free rate symbol must be a string object')

    def test_rfr_symbol_float_input(self):
        try:
            self.risk_free_sec.rfr_symbol = 0.0
        except TypeError as e:
            self.assertEqual(str(e), 'Risk-free rate symbol must be a string object')

    def test_rfr_symbol_none_input(self):
        try:
            self.risk_free_sec.rfr_symbol = None
        except TypeError as e:
            self.assertEqual(str(e), 'Risk-free rate symbol must be a string object')

    # Test risk_free_rate 
    def test_risk_free_rate_float_input(self):
        self.risk_free_sec.risk_free_rate = 0.15
        self.assertEqual(0.15, self.risk_free_sec.risk_free_rate)

    def test_risk_free_rate_int_input(self):
        self.risk_free_sec.risk_free_rate = 0
        self.assertEqual(0, self.risk_free_sec.risk_free_rate)

    def test_risk_free_rate_list_input(self):
        try:
            self.risk_free_sec.risk_free_rate = [[0, 0, 0, 0], [0, 0, 0, 0]]
        except TypeError as e:
            self.assertEqual(str(e), 'Risk-free rate must be a numeric data type')
    
    def test_risk_free_rate_dict_input(self):
        try:
            self.risk_free_sec.risk_free_rate = {'zero': 0, 'one': 1}
        except TypeError as e:
            self.assertEqual(str(e), 'Risk-free rate must be a numeric data type')

    def test_risk_free_rate_str_input(self):
        try:
            self.risk_free_sec.risk_free_rate = '0.15'
        except TypeError as e:
            self.assertEqual(str(e), 'Risk-free rate must be a numeric data type')

    def test_risk_free_rate_none_input(self):
        try:
            self.risk_free_sec.risk_free_rate = None
        except TypeError as e:
            self.assertEqual(str(e), 'Risk-free rate must be a numeric data type')
