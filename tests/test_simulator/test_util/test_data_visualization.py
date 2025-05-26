import unittest
import numpy as np
import monte_carlo_simulator.service.util.data_visualizer as vis

class TestMonteCarloSimVisualization(unittest.TestCase):

	# Get stored sim_data for testing
	sim_data = np.genfromtxt(
		fname='.\\tests\\test_simulator\\testing_data\\sim_data.csv', 
		delimiter=',', 
		dtype=np.float64, 
		usecols=range(1,1001), 
		skip_header=True, 
		skip_footer=True
		)
	
	# Get expected percentile values from test data
	one_std_below_mean = np.percentile(sim_data, 15.8665, axis=1)
	one_std_above_mean = np.percentile(sim_data, 84.134, axis=1)
	two_std_below_mean = np.percentile(sim_data, 2.275, axis=1)
	two_std_above_mean = np.percentile(sim_data, 97.725, axis=1)

	# Create the sim data visualizations
	fig = vis.monte_carlo_sim_vis(sim_data, 12)

	# Get current axis limits
	axs1_xlim = fig.axes[0].get_xlim()
	axs1_ylim = fig.axes[0].get_ylim()
		
	def test_x_label(self):
		self.assertEqual(self.fig.axes[0].get_xlabel(), 'Trading Days')

	def test_y_label(self):
		self.assertEqual(self.fig.axes[0].get_ylabel(), 'Price in USD')

	def test_axs1_title(self):
		self.assertEqual(self.fig.axes[0].get_title(), 'Future Price Simulation')

	def test_legend_was_created(self):
		self.assertIsNotNone(self.fig.legend())

	def test_monte_carlo_sim_vis_invalid_data_dict(self):
		with self.assertRaises(TypeError) as e:
			vis.monte_carlo_sim_vis({'1':1, 'two':2})
			self.assertRegex(str(e), r'"sim_data" parameter must be a DataFrame, not \.*')

	def test_monte_carlo_sim_vis_invalid_data_negative_int(self):
		with self.assertRaises(TypeError) as e:
			vis.monte_carlo_sim_vis(-1)
			self.assertRegex(str(e), r'"sim_data" parameter must be a DataFrame, not \.*')

	def test_monte_carlo_sim_vis_invalid_data_int(self):
		with self.assertRaises(TypeError) as e:
			vis.monte_carlo_sim_vis(0)
			self.assertRegex(str(e), r'"sim_data" parameter must be a DataFrame, not \.*')

	def test_monte_carlo_sim_vis_invalid_data_tuple(self):
		with self.assertRaises(TypeError) as e:
			vis.monte_carlo_sim_vis(([1],0))
			self.assertRegex(str(e), r'"sim_data" parameter must be a DataFrame, not \.*')

	def test_monte_carlo_sim_vis_invalid_data_boolean(self):
		with self.assertRaises(TypeError) as e:
			vis.monte_carlo_sim_vis(False)
			self.assertRegex(str(e), r'"sim_data" parameter must be a DataFrame, not \.*')

	def test_monte_carlo_sim_vis_invalid_data_None(self):
		with self.assertRaises(TypeError) as e:
			vis.monte_carlo_sim_vis(None)
			self.assertRegex(str(e), r'"sim_data" parameter must be a DataFrame, not \.*')
	
	def test_monte_carlo_sim_vis_invalid_time_horizon_dict(self):
		with self.assertRaises(TypeError) as e:
			vis.monte_carlo_sim_vis(self.sim_data, {'1':1, 'two':2})
			self.assertRegex(str(e), r'"time_horizon" parameter must be an integer, not \.*')

	def test_monte_carlo_sim_vis_time_horizon_negative_int(self):
		with self.assertRaises(ValueError) as e:
			vis.monte_carlo_sim_vis(self.sim_data, -1)
			self.assertRegex(str(e), r'"time_horizon" parameter must be positive, not \.*')

	def test_monte_carlo_sim_vis_invalid_time_horizon_tuple(self):
		with self.assertRaises(TypeError) as e:
			vis.monte_carlo_sim_vis(self.sim_data, ([1],0))
			self.assertRegex(str(e), r'"time_horizon" parameter must be an integer, not \.*')

	def test_monte_carlo_sim_vis_invalid_time_horizon_boolean(self):
		with self.assertRaises(TypeError) as e:
			vis.monte_carlo_sim_vis(self.sim_data, False)
			self.assertRegex(str(e), r'"time_horizon" parameter must be an integer, not \.*')

	def test_monte_carlo_sim_vis_invalid_time_horizon_None(self):
		with self.assertRaises(TypeError) as e:
			vis.monte_carlo_sim_vis(self.sim_data, None)
			self.assertRegex(str(e), r'"time_horizon" parameter must be an integer, not \.*')

	def test_x_lim(self):
		self.assertGreater(self.axs1_xlim[1], self.axs1_xlim[0])

	def test_y_lim(self):
		self.assertGreater(self.axs1_ylim[1], self.axs1_ylim[0])


if __name__ == '__main__':
    unittest.main()