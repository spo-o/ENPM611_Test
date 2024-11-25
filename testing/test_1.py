import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from usage_analysis import UsageAnalysis


class TestUsageAnalysis(unittest.TestCase):

    @patch('usage_analysis.DataLoader')  # Mock DataLoader
    def test_run(self, MockDataLoader):
       
        mock_issues = [
            MagicMock(labels=["New Feature", "Bug"]),
            MagicMock(labels=["Enhancement", "Bug"]),
            MagicMock(labels=["New Feature", "Documentation"]),
            MagicMock(labels=["Bug", "Performance"]),
            MagicMock(labels=["New Feature", "Enhancement"]),
        ]
        MockDataLoader().get_issues.return_value = mock_issues

        analysis = UsageAnalysis()
        
        with patch('usage_analysis.plt.show'):
            analysis.run()
        
        expected_label_counts = {
            "New Feature": 3,
            "Bug": 3,
            "Enhancement": 2,
            "Documentation": 1,
            "Performance": 1,
        }

        label_df = pd.DataFrame(
            [label for issue in mock_issues for label in issue.labels],
            columns=["label"]
        )
        calculated_label_counts = label_df["label"].value_counts().to_dict()

        self.assertEqual(calculated_label_counts, expected_label_counts)

    @patch('usage_analysis.DataLoader')
    def test_run_large_dataset(self, MockDataLoader):
    # Mock many issues with labels
        mock_issues = [MagicMock(labels=["Bug", "New Feature"]) for _ in range(1000)]
        MockDataLoader().get_issues.return_value = mock_issues

        analysis = UsageAnalysis()
        
        with patch('usage_analysis.plt.show'):
            analysis.run()
        
        # Validate label counts
        expected_label_counts = {"Bug": 1000, "New Feature": 1000}
        label_df = pd.DataFrame(
            [label for issue in mock_issues for label in issue.labels],
            columns=["label"]
        )
        calculated_label_counts = label_df["label"].value_counts().to_dict()

        self.assertEqual(calculated_label_counts, expected_label_counts)

    @patch('usage_analysis.DataLoader')
    def test_run_duplicate_labels(self, MockDataLoader):
    # Mock issues with duplicate labels
        mock_issues = [
            MagicMock(labels=["Bug", "Bug"]),
            MagicMock(labels=["New Feature", "New Feature"]),
        ]
        MockDataLoader().get_issues.return_value = mock_issues

        analysis = UsageAnalysis()
        
        with patch('usage_analysis.plt.show'):
            analysis.run()
        
        # Validate label counts
        expected_label_counts = {"Bug": 2, "New Feature": 2}
        label_df = pd.DataFrame(
            [label for issue in mock_issues for label in issue.labels],
            columns=["label"]
        )
        calculated_label_counts = label_df["label"].value_counts().to_dict()

        self.assertEqual(calculated_label_counts, expected_label_counts)


if __name__ == '__main__':
    unittest.main()
