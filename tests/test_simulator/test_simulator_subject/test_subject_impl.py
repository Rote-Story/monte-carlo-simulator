import unittest
from unittest.mock import Mock

from monte_carlo_simulator.model import MarketIndex, Stock, RiskFreeSecurity
from monte_carlo_simulator.data_fetcher import MarketDataFetcher
from monte_carlo_simulator.gui.frames.error_frame_obs import ErrorFrame
from monte_carlo_simulator.gui.inter.observer_inter import Observer
from monte_carlo_simulator.service.simulator_subj import Simulator


class TestSubjectImplementation(unittest.TestCase):

    def setUp(self):
        # Create mock dependencies for Simulator
        self.mock_data_fetcher = Mock(spec=MarketDataFetcher)
        self.mock_stock_data = Mock(spec=Stock)
        self.mock_market_data = Mock(spec=MarketIndex)
        self.mock_rfr_data = Mock(spec=RiskFreeSecurity)

        # Create mock observers to test subject/observer methods
        self.mock_observer = Mock(spec=Observer)
        self.mock_error_observer = Mock(spec=ErrorFrame)
        
        # Create a new "blank" simulator_subject for each test
        self.test_simulator_subject = Simulator(
            market_data_fetcher=self.mock_data_fetcher, 
            financial_asset=self.mock_stock_data,
            market_index=self.mock_market_data, 
            risk_free_sec=self.mock_rfr_data
            )

    def test_attach_valid_observer(self):
        self.test_simulator_subject.attach(self.mock_observer)
        result = self.test_simulator_subject._observers[0]
        self.assertIs(self.mock_observer, result)
    
    def test_attach_duplicate_observer(self):
        # Call attach twice with the same observer as an argument
        self.test_simulator_subject.attach(self.mock_observer)
        self.test_simulator_subject.attach(self.mock_observer)

        # The observer should exist in the _observers list
        result = self.test_simulator_subject._observers
        self.assertIs(self.mock_observer, result[0])

        # The _observers list should have only one element
        self.assertEqual(len(result), 1)

    def test_attach_multiple_observers(self):
        # Call attach twice with the different observers
        self.test_simulator_subject.attach(self.mock_observer)
        self.test_simulator_subject.attach(self.mock_error_observer)

        # Both observers should exist in the _observers list
        result = self.test_simulator_subject._observers
        self.assertIs(self.mock_observer, result[0])
        self.assertIs(self.mock_error_observer, result[1])

        # The _observers list should have two elements
        self.assertEqual(len(result), 2)

    def test_detach_removes_observer(self):
        # Populate _observers list with .attach() method
        self.test_simulator_subject.attach(self.mock_observer)
        self.test_simulator_subject.attach(self.mock_error_observer)

        # Remove one observer
        self.test_simulator_subject.detach(self.mock_observer)

        # The remaining observer should be mock_error_observer
        self.assertIs(self.test_simulator_subject._observers[0], self.mock_error_observer)

        # _observers list should have only one element
        self.assertEqual(len(self.test_simulator_subject._observers), 1)

    def test_detach_value_error_invalid_input(self):
        # Mock error message display functionality 
        self.mock_error_observer.update.side_effect = self.test_simulator_subject.error_message
        
        # Populate _observers list
        self.test_simulator_subject.attach(self.mock_error_observer)

        # Try to detach observer not in list
        self.test_simulator_subject.detach(self.mock_observer)

        # Error message 
        self.assertEqual(self.test_simulator_subject.error_message, f'{self.mock_observer} not in list of observers.')
        self.mock_error_observer.update.assert_called_once_with(self.test_simulator_subject)
            

    def test_notify_calls_update_once(self):
        # Attach observers to list
        self.test_simulator_subject.attach(self.mock_observer)

        self.test_simulator_subject.notify() # Notify observer

        # Verify update was called once with the appropriate argument
        self.mock_observer.update.assert_called_once_with(self.test_simulator_subject)


if __name__ == '__main__':
    unittest.main()