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

    def test_toad_has_period_two(self):
        toad = PATTERNS["toad"]
        self.assertNotEqual(step(toad, 10, 10), toad)
        self.assertEqual(step(step(toad, 10, 10), 10, 10), toad)

    def test_beacon_has_period_two(self):
        beacon = PATTERNS["beacon"]
        self.assertNotEqual(step(beacon, 10, 10), beacon)
        self.assertEqual(step(step(beacon, 10, 10), 10, 10), beacon)


if __name__ == "__main__":
    unittest.main()
