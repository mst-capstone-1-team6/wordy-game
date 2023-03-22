import unittest

from wordy.base.worddict import WordDict


class TestBoard(unittest.TestCase):

    def test(self):
        d = WordDict("../assets/dicts/full_dict.txt")
        print(d.testWord("hello"))
        print(d.findPossibleWords("a", [1, 2, 3]))


if __name__ == '__main__':
    unittest.main()
