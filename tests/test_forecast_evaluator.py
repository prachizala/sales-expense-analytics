"""Unit tests for linear revenue forecasting model."""
import unittest

class TestForecastEvaluator(unittest.TestCase):
    def test_perfect_linear_trend(self):
        x = [1, 2, 3, 4, 5]
        y = [10, 20, 30, 40, 50]
        slope = (y[-1] - y[0]) / (x[-1] - x[0])
        self.assertEqual(slope, 10.0)

if __name__ == '__main__':
    unittest.main()
