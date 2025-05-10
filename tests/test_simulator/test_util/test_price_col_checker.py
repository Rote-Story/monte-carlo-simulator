
import unittest
import pandas as pd

from monte_carlo_simulator.service.util.price_col_checker import price_col_checker

class TestPriceColumnChecker(unittest.TestCase):


    # Create test dataframes 
    close_df = pd.DataFrame({'Close': [1, 2, 3, 4, 5]})
    adj_close_df = pd.DataFrame({'Adj Close': [1, 2, 3, 4, 5]})
    both_close_df = pd.DataFrame({'Adj Close': [1, 2, 3, 4, 5], 'Close': [0, 1, 2, 3, 4]})
    empty_df = pd.DataFrame()


    def test_valid_close_df(self):
        result = price_col_checker(self.close_df)
        self.assertEqual(result, 'Close')

    def test_valid_adj_close_df(self):
        result = price_col_checker(self.adj_close_df)
        self.assertEqual(result, 'Adj Close')

    def test_valid_both_close_df(self):
        result = price_col_checker(self.both_close_df)
        self.assertEqual(result, 'Adj Close')

    def test_invalid_input_int(self):
        with self.assertRaises(TypeError) as e:
            price_col_checker(1)

            self.assertRegex(e, r'df must be of type pandas.Dataframe, not \.*')
    def test_invalid_input_float(self):
        with self.assertRaises(TypeError) as e:
            price_col_checker(0.0)

            self.assertRegex(e, r'df must be of type pandas.Dataframe, not \.*')
            
    def test_invalid_input_bool(self):
        with self.assertRaises(TypeError) as e:
            price_col_checker(True)

            self.assertRegex(e, r'df must be of type pandas.Dataframe, not \.*')
            
    def test_invalid_input_list(self):
        with self.assertRaises(TypeError) as e:
            price_col_checker([1, 2, 3])

            self.assertRegex(e, r'df must be of type pandas.Dataframe, not \.*')
            
    def test_invalid_input_dict(self):
        with self.assertRaises(TypeError) as e:
            price_col_checker({'Close': [1, 2, 3]})

            self.assertRegex(e, r'df must be of type pandas.Dataframe, not \.*')
            
    def test_invalid_input_string(self):
        with self.assertRaises(TypeError) as e:
            price_col_checker('Close')

            self.assertRegex(e, r'df must be of type pandas.Dataframe, not \.*')
            
    def test_invalid_input_empty_df(self):
        with self.assertRaises(ValueError) as e:
            price_col_checker(self.empty_df)

            self.assertRegex(e, r'df must have a "Close" or "Adj Close" column.\ndf column names: \.*')
            
if __name__ == '__main__':
    unittest.main()
