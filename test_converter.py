import unittest
from converter import Converter

class TestConverter(unittest.TestCase):
    def test_above_100_7(self):
        self.assertEqual(Converter.do(150.0), 1000)
        self.assertEqual(Converter.do(100.7), 1000)
        self.assertEqual(Converter.do(999.9), 1000)

    def test_positive_small(self):
        self.assertEqual(Converter.do(50.3), 50)
        self.assertEqual(Converter.do(0.1), 0)
        self.assertEqual(Converter.do(100.6), 100)

    def test_zero_raises(self):
        with self.assertRaises(ValueError):
            Converter.do(0.0)

    def test_negative_small(self):
        self.assertEqual(Converter.do(-10.0), -15)
        self.assertEqual(Converter.do(-30.5), -35)
        self.assertEqual(Converter.do(-0.5), -5)

    def test_below_minus_30_4(self):
        self.assertEqual(Converter.do(-30.4), -2000)
        self.assertEqual(Converter.do(-100.0), -2000)
        self.assertEqual(Converter.do(-999.9), -2000)
if __name__ == '__main__':
    unittest.main()