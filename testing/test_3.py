import unittest
from unittest.mock import patch, MagicMock
import networkx as nx
import json
from tree_visualizer import IssueTreeVisualizer

class TestTreeVisualizer(unittest.TestCase):

    def setUp(self):
        # Setup mock data and temporary file paths.
        self.mock_issues = [
            {
                "number": 1,
                "title": "Test Issue 1",
                "state": "open",
                "created_date": "2024-01-01T12:00:00",
                "events": [
                    {"event_type": "commented", "event_date": "2024-01-02T12:00:00", "author": "user1"},
                    {"event_type": "cross-referenced", "event_date": "2024-01-03T12:00:00", "author": "user2", "comment": "See #2"}
                ]
            },
            {
                "number": 2,
                "title": "Test Issue 2",
                "state": "closed",
                "created_date": "2023-12-31T12:00:00",
                "events": []
            }
        ]
        self.temp_file = "temp_issues.json"
        with open(self.temp_file, "w") as f:
            json.dump(self.mock_issues, f)

    def tearDown(self):
        import os
        os.remove(self.temp_file)

    @patch("tree_visualizer.plt.show")
    def test_run(self, mock_show):
        visualizer = IssueTreeVisualizer(self.temp_file, issue_limit=10)
        try:
            visualizer.run()
        except Exception as e:
            self.fail(f"Run method failed with exception: {e}")

    def test_load_issues(self):
        # Test loading issues from a file.
        visualizer = IssueTreeVisualizer(self.temp_file)
        issues = visualizer.load_issues()
        self.assertEqual(len(issues), 2)
        self.assertEqual(issues[0]["title"], "Test Issue 1")

    def test_filter_by_date(self):
        # Test date filtering.
        visualizer = IssueTreeVisualizer(self.temp_file, start_date="2024-01-01", end_date="2024-12-31")
        self.assertTrue(visualizer.filter_by_date("2024-01-02T12:00:00"))
        self.assertFalse(visualizer.filter_by_date("2023-12-31T23:59:59"))
        self.assertFalse(visualizer.filter_by_date("2025-01-01T00:00:00"))
        with self.assertRaises(ValueError):
            visualizer.filter_by_date("invalid-date")
        self.assertFalse(visualizer.filter_by_date(None))

    def test_build_graph(self):
        visualizer = IssueTreeVisualizer(self.temp_file, issue_limit=10)
        issues = visualizer.load_issues()
        G = visualizer.build_graph(issues)
        self.assertEqual(len(G.nodes), 4)
        self.assertEqual(len(G.edges), 3)
        self.assertIn(1, G.nodes)
        self.assertIn("1_commented_2024-01-02T12:00:00", G.nodes)
        self.assertIn((1, "1_commented_2024-01-02T12:00:00"), G.edges)

    @patch("tree_visualizer.plt.show")
    def test_draw_graph(self, mock_show):
        visualizer = IssueTreeVisualizer(self.temp_file, issue_limit=10)
        issues = visualizer.load_issues()
        G = visualizer.build_graph(issues)
        try:
            visualizer.draw_graph(G)
        except Exception as e:
            self.fail(f"Graph drawing failed with exception: {e}")

    def test_skip_irrelevant_events(self):
        visualizer = IssueTreeVisualizer(self.temp_file, start_date="2024-01-01", end_date="2024-12-31")
        issues = [
            {
                "number": 1,
                "created_date": "2024-01-01T12:00:00",
                "events": [{"event_type": "irrelevant", "event_date": "2024-01-02T12:00:00"}]
            }
        ]
        G = visualizer.build_graph(issues)
        self.assertEqual(len(G.nodes), 1)
        self.assertEqual(len(G.edges), 0)

if __name__ == "__main__":
    unittest.main()
