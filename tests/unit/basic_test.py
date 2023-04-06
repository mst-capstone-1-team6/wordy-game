
# https://docs.python.org/3/library/unittest.html

import unittest

from wordy.base.board import Board, over_positions
from wordy.base.game import LETTER_SCORING


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

    def test_letter_scoring(self):
        for letter_ascii in range(ord('A'), ord('Z') + 1):
            letter = chr(letter_ascii)
            assert any(letter in letters for letters in LETTER_SCORING.values()), f"letter: {letter} not present"


if __name__ == '__main__':
    unittest.main()
