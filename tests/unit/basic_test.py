
# https://docs.python.org/3/library/unittest.html

import unittest

from wordy.base.board import Board


class TestBoard(unittest.TestCase):

    def test(self):
        board = Board(15, {})
        board = board.place_tiles({
            (0, 0): "A",
            (14, 14): "B",
        })
        print(str(board))


if __name__ == '__main__':
    unittest.main()
