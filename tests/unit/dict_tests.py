import unittest

from wordy.base.worddict import WordDict


class TestDict(unittest.TestCase):
    def test(self):
        d = WordDict("assets/dicts/full_dict.txt")
        print(d.test_word("hello"))
        print(d.find_one_letter("a", [1, 2, 3]))
        print(d.find_many_letters(["a", "y", "e"], [0, 1, 3]))


if __name__ == '__main__':
    unittest.main()
