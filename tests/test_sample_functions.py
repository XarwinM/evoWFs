import unittest

from evoWFs.spec import *


class TestSimple(unittest.TestCase):

    def test_sampling(self):
        self.assertTrue( isinstance(sample_space(int), int))
        self.assertTrue( isinstance(sample_space(str), str))


if __name__ == '__main__':
    unittest.main()
