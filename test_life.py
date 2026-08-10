import unittest

from life import PATTERNS, step


class StillLifeTests(unittest.TestCase):
    def test_block_is_stable(self):
        block = PATTERNS["block"]
        self.assertEqual(step(block, 10, 10), block)


class OscillatorTests(unittest.TestCase):
    def test_blinker_has_period_two(self):
        blinker = PATTERNS["blinker"]
        self.assertNotEqual(step(blinker, 10, 10), blinker)
        self.assertEqual(step(step(blinker, 10, 10), 10, 10), blinker)


if __name__ == "__main__":
    unittest.main()
