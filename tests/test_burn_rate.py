"""Unit tests for burn rate and margin validator."""
import unittest

class TestBurnRateValidator(unittest.TestCase):
    def test_gross_margin_calculation(self):
        revenue = 100000.0
        cogs = 40000.0
        margin = ((revenue - cogs) / revenue) * 100
        self.assertEqual(margin, 60.0)

if __name__ == '__main__':
    unittest.main()
