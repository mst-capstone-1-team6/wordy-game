
# https://docs.python.org/3/library/unittest.html

import unittest

from wordy.base.board import Board, over_positions


class TestBoard(unittest.TestCase):

    def test(self):
        board = Board(15, {})
        board = board.place_tiles({
            (0, 0): "A",
            (14, 14): "B",
        })
        print(str(board))

    def test_over_positions(self):
        assert [(0, 0), (1, 0), (2, 0)] == list(over_positions((0, 0), (2, 0)))


if __name__ == '__main__':
    unittest.main()
