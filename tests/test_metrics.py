import unittest

from evoWFs.metrics import jaccard_index, precision, recall 

class TestMetrics(unittest.TestCase):

    def test_jaccard_index(self):
        self.assertEqual(jaccard_index({1, 2, 3}, {1, 2, 3} ), 1.0)
        self.assertEqual(jaccard_index({1, 2, 3, 4}, {1, 2} ), 0.5)
        self.assertEqual(jaccard_index({3, 4}, {1, 2}), 0.0)

    def test_precision(self):
        self.assertEqual(precision({1, 2, 3}, {1, 2, 3, 4} ), 1.0)
        self.assertEqual(precision({1, 2, 3, 4}, {1, 2, 3} ), 0.75)
        self.assertEqual(precision({1, 2, 3}, {4, 5} ), 0.0)

    def test_recall(self):
        self.assertEqual(recall({1, 2, 3, 4}, {1, 2, 3} ), 1.0)
        self.assertEqual(recall({1, 2, 3}, {1, 2, 3, 4} ), 0.75)
        self.assertEqual(recall({1, 2, 3}, {4, 5} ), 0.0)

if __name__ == '__main__':
    unittest.main()
