import unittest
import unittest.mock as mock
import logging
import sys

from unittest.mock import MagicMock
from valid_moves import *

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class TestRotations(unittest.TestCase):

    # (2, 1), (-1, 2), (-2, -1), (1, -2)
    def test_rotations_2x1(self):
        pattern = [[1, 0], [2, 0], [2, 1]]
        rotations = generate_rotations(pattern)
        print(rotations)
        self.assertEqual(
            rotations,
            [[[0, 1], [0, 2], [-1, 2]], [[-1, 0], [-2, 0], [-2, -1]], [[0, -1], [0, -2], [1, -2]]])

    # (1, 1), (-1, 1), (-1, -1), (1, -1)
    def test_rotations_1x1(self):
        pattern = [[1, 1]]
        rotations = generate_rotations(pattern)
        print(rotations)
        self.assertEqual(
            rotations,
            [[[-1, 1]], [[-1, -1]], [[1, -1]]])
