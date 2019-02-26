import unittest

from helpers import get_angle_by_three_points


class TestAngleByThreePoints(unittest.TestCase):
    def test_common(self):
        self.assertEqual(
            get_angle_by_three_points((1, 3), (1, 1), (5, 2)),
            75
        )


if __name__ == '__main__':
    unittest.main()
