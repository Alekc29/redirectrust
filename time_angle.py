import unittest


def angle(h: int, m: int) -> float:
    h_angle = 30 * (h % 12) + 0.5 * m
    m_angle = 6 * m
    angle = abs(h_angle - m_angle)
    return min(angle, 360 - angle)


class TestGetLenta(unittest.TestCase):

    def test_angle(self):
        self.assertEqual(angle(6, 33), 90.0)

unittest.main()