
import unittest
from numpy import linspace
from numpy.testing import assert_array_equal
from monte_carlo_simulator.data.sim_data import SimData

class TestSimData(unittest.TestCase):

    test_sim_data = SimData()
    test_array = linspace(-1.0, 1.0, num=5)

    def test_sim_data_array_input(self):
        self.test_sim_data.sim_data = self.test_array
        assert_array_equal(self.test_array, self.test_sim_data.sim_data)

    def test_sim_data_list_input(self):
        try:
            self.test_sim_data.sim_data = [1, 2, 3, 4, 5]
        except ValueError as e:
            self.assertEqual(str(e), "Monte Carlo simulation data must be of type numpy.ndarray")

    def test_sim_data_dict_input(self):
        try:
            self.test_sim_data.sim_data = {"one": 1, "two": 2}
        except ValueError as e:
            self.assertEqual(str(e), "Monte Carlo simulation data must be of type numpy.ndarray")

    def test_sim_data_bool_input(self):
        try:
            self.test_sim_data.sim_data = True
        except ValueError as e:
            self.assertEqual(str(e), "Monte Carlo simulation data must be of type numpy.ndarray")

    def test_sim_data_int_input(self):
        try:
            self.test_sim_data.sim_data = 1
        except ValueError as e:
            self.assertEqual(str(e), "Monte Carlo simulation data must be of type numpy.ndarray")
    
    def test_sim_data_float_input(self):
        try:
            self.test_sim_data.sim_data = -0.6
        except ValueError as e:
            self.assertEqual(str(e), "Monte Carlo simulation data must be of type numpy.ndarray")

    def test_sim_data_none_input(self):
        try:
            self.test_sim_data.sim_data = None
        except ValueError as e:
            self.assertEqual(str(e), "Monte Carlo simulation data must be of type numpy.ndarray")

if __name__ == "__main__":
    unittest.main()