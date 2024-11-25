import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from res_time_analysis import ResolutionTimeAnalysis

class TestResolutionTimeAnalysis(unittest.TestCase):

    @patch('res_time_analysis.DataLoader')
    @patch('matplotlib.pyplot.hist')
    @patch('matplotlib.pyplot.show')
    def test_run(self, mock_show, mock_hist, mock_data_loader):
        # Mock issue data
        mock_issues = [
            MagicMock(state='closed', created_date='2023-10-01', updated_date='2023-10-10'),
            MagicMock(state='closed', created_date='2023-10-05', updated_date='2023-10-15'),
            MagicMock(state='open', created_date='2023-10-07', updated_date=None),
            MagicMock(state='closed', created_date='2023-10-10', updated_date='2023-10-20')
        ]
        
        mock_data_loader.return_value.get_issues.return_value = mock_issues
        analysis = ResolutionTimeAnalysis()
        analysis.run()

        expected_resolution_times = [9, 10, 10]
        actual_resolution_times = [
            (pd.to_datetime(issue.updated_date) - pd.to_datetime(issue.created_date)).days
            for issue in mock_issues if issue.state == 'closed'
        ]
        self.assertEqual(expected_resolution_times, actual_resolution_times)
        mock_hist.assert_called_once_with(expected_resolution_times, bins=20, edgecolor='black')
        mock_show.assert_called_once()

    @patch('res_time_analysis.DataLoader')
    @patch('matplotlib.pyplot.hist')
    @patch('matplotlib.pyplot.show')
    def test_empty_data(self, mock_show, mock_hist, mock_data_loader):
        mock_data_loader.return_value.get_issues.return_value = []
        analysis = ResolutionTimeAnalysis()
        analysis.run()
        mock_hist.assert_called_once_with([], bins=20, edgecolor='black')  # Adjusted to expect an empty call
        mock_show.assert_called_once()

    @patch('res_time_analysis.DataLoader')
    @patch('matplotlib.pyplot.hist')
    @patch('matplotlib.pyplot.show')
    def test_all_open_issues(self, mock_show, mock_hist, mock_data_loader):
        # Mock issues are all open
        mock_issues = [
            MagicMock(state='open', created_date='2023-10-01', updated_date=None),
            MagicMock(state='open', created_date='2023-10-02', updated_date=None)
        ]
        mock_data_loader.return_value.get_issues.return_value = mock_issues
        analysis = ResolutionTimeAnalysis()
        analysis.run()
        mock_hist.assert_called_once_with([], bins=20, edgecolor='black')  # Expecting an empty histogram call
        mock_show.assert_called_once()

    @patch('res_time_analysis.DataLoader')
    @patch('matplotlib.pyplot.hist')
    @patch('matplotlib.pyplot.show')
    def test_invalid_date_formats(self, mock_show, mock_hist, mock_data_loader):
        # Mock issues with invalid dates
        mock_issues = [
            MagicMock(state='closed', created_date='2023-10-01', updated_date='10-25-2023'), # Wrong date format
            MagicMock(state='closed', created_date='wrong-date', updated_date='2023-10-15')   # Non-date string
        ]
        mock_data_loader.return_value.get_issues.return_value = mock_issues
        analysis = ResolutionTimeAnalysis()
        with self.assertRaises(ValueError):  # Ensure your class raises this error for invalid dates
            analysis.run()

if __name__ == '__main__':
    unittest.main()
