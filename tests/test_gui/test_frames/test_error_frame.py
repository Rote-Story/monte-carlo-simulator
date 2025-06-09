

import unittest
from unittest.mock import MagicMock, PropertyMock
import tkinter as tk

from monte_carlo_simulator.gui.frames.error_frame_obs import ErrorFrame
from monte_carlo_simulator.gui.frames.sim_frame import SimFrame
from monte_carlo_simulator.service.simulator_subj import Simulator

class TestErrorFrame(unittest.TestCase):

    def setUp(self):
        # Create mock simulator dependency
        self.mock_simulator = MagicMock(spec=Simulator)

        # Initialize test main window, replace test methods with mocks
        self.root = tk.Tk()
        self.app = SimFrame(master=self.root, simulator=self.mock_simulator)
        self.root.withdraw() # Prevent window from being shown

        # Initialize error frame
        self.error_frame = ErrorFrame(self.app)

        # Create error frame labels
        self.error_frame.create_error_label()

    def tearDown(self):
        self.error_frame.destroy()
        self.app.destroy()
        self.root.destroy()

    def test_error_frame_label_positioning(self):
        self.assertEqual(self.error_frame.error_label.grid_info()['row'], 0)
        self.assertEqual(self.error_frame.error_label.grid_info()['column'], 0)

    def test_error_frame_label_initial_text_is_empty(self):
        self.assertEqual(self.error_frame.error_label.cget('text'), '')

    def test_error_frame_update_error_message_label_config(self):
        type(self.mock_simulator).error_message = PropertyMock(return_value='An exception occurred: Exception')
        self.error_frame.update(self.mock_simulator)
        self.assertEqual(self.error_frame.error_label.cget('text'), 'An exception occurred: Exception')

    def test_error_frame_update_subject_error_message_is_none(self):
        type(self.mock_simulator).error_message = PropertyMock(return_value=None)
        self.error_frame.update(self.mock_simulator)
        self.assertEqual(self.error_frame.error_label.cget('text'), '')

    def test_error_frame_update_subject_error_message_is_int(self):
        type(self.mock_simulator).error_message = PropertyMock(return_value=0)
        self.error_frame.update(self.mock_simulator)
        self.assertEqual(self.error_frame.error_label.cget('text'), '')

    def test_error_frame_update_subject_error_message_is_bool(self):
        type(self.mock_simulator).error_message = PropertyMock(return_value=False)
        self.error_frame.update(self.mock_simulator)
        self.assertEqual(self.error_frame.error_label.cget('text'), '')

    def test_error_frame_update_subject_error_message_is_float(self):
        type(self.mock_simulator).error_message = PropertyMock(return_value=0.1)
        self.error_frame.update(self.mock_simulator)
        self.assertEqual(self.error_frame.error_label.cget('text'), '')

    def test_error_frame_update_subject_error_message_is_list(self):
        type(self.mock_simulator).error_message = PropertyMock(return_value=['error_message'])
        self.error_frame.update(self.mock_simulator)
        self.assertEqual(self.error_frame.error_label.cget('text'), '')

    def test_error_frame_update_subject_error_message_is_dict(self):
        type(self.mock_simulator).error_message = PropertyMock(return_value={'first': 'error'})
        self.error_frame.update(self.mock_simulator)
        self.assertEqual(self.error_frame.error_label.cget('text'), '')

    def test_error_frame_update_subject_error_message_is_tuple(self):
        type(self.mock_simulator).error_message = PropertyMock(return_value=('one', 'error'))
        self.error_frame.update(self.mock_simulator)
        self.assertEqual(self.error_frame.error_label.cget('text'), '')

if __name__ == '__main__':
    unittest.main()