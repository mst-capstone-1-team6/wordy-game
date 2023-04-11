from __future__ import annotations
from dataclasses import dataclass

from pathlib import Path
from typing import List, Set, Optional


@dataclass
class WordInfo():
    word_str: str
    start_offsets: set


class WordDict():
    """To create a new WordDict use either WordDict.from_file() or WordDict.from_list()"""
    def __init__(self):
        self.words = []


    def add_word(self, word):
        self.words.append(word)


    @classmethod
    def from_file(cls, fileName: str) -> WordDict:
        new = cls.__new__(cls)
        with open(fileName, "r") as f:
            new.words: List[str] = [i.rstrip() for i in f.readlines()]
        return new


    @classmethod
    def from_list(cls, words: List[str]) -> WordDict:
        new = cls.__new__(cls)
        new.words = [word.upper() for word in words]
        return new


    @classmethod
    def can_be_spelled(word, letters: List) -> bool:
        for l in word.upper():
            if l not in letters: 
                return False
            else: 
                letters.delete(l) 
        return True
    

    def trim_by_hand(self, hand: List) -> WordDict:
        """Returns a new dictionary which contains only the words in self which can be spelled with letters given"""
        return WordDict.from_list([word for word in self.words if WordDict.can_be_spelled(word, hand)])


    def trim_by_length(self, min: int = 0, max: int = 15) -> WordDict:
        """Returns a new dictonary which contains only the words in self which fall between the given lengths"""
        return WordDict.from_list([word for word in self.words if len(word) < max and len(word) > min])


    def trim_by_letters(self, lets: List[str] = []) -> WordDict:
        """Returns a new dictionary which contains only the words in self which contain the given letters"""
        return WordDict.from_list([word for word in self.words if all([1 if word.find(let) != -1 else 0 for let in lets])])


    def test_word(self, test: str) -> bool:
        return test.upper() in self.words


    def find_one_letter(self, set_let: str, position_on_board: int) -> List[WordInfo]:
        """Find all words in the dictionary which contain the given letter and their start positions on the board
           eg. find_one_letter("a", 4) will return a list like [WordInfo("apple", {4}), WordInfo("watermelon", {3}), WordInfo("year", {2}), ...]"""
        set_let = set_let.upper()
        #Generate list of all words containing the given letter
        temp = [word for word in self.words if word.find(set_let) != -1]
        #Restrict words to only contain the letter at the given indexes
        results = []
        for word in temp:
            index_set = set()
            for i, x in enumerate(word):
                if x == set_let:
                    index_set.add(i)
            if len(index_set) == 0:
                continue
            start_set = {position_on_board - index for index in index_set}
            results.append(WordInfo(word, start_set))
        return results


    def find_many_letters(self, lets: List[str], offsets: List[int]) -> List[WordInfo]:
        """Find all words in the dictionary which contain the given letters at the given relative offsets
           eg. find_many_letters(["a", "l"], [0, 1]) will return a list like [WordInfo("ale", {0}), WordInfo("evaluate", {-2}), WordInfo("seasonal", {-6}), ...]
               find_many_letters(["n", "a"], [0, 1]) will return a list like [WordInfo("banana", {-2, -4}), WordInfo("functional", {-7}), ...]
        """
        lets = [let.upper() for let in lets]
        max_offset = max(offsets)
        min_offset = min(offsets)
        #Generate list of all words containing the given letters of a valid length and letters
        temp = self.trim_by_letters(lets)
        temp = temp.trim_by_length(min = max_offset - min_offset)
        #Restrict words to only have the correct letters at the correct offsets
        results = []
        for word in temp.words:
            valid_start_offsets = set()
            for word_index, word_starting_letter in enumerate(word):
                start_offset = min_offset - word_index
                is_valid = True
                for offset, placed_letter in zip(offsets, lets):
                    index = offset - start_offset
                    if index >= len(word) or word[index] != placed_letter:
                        is_valid = False
                        break
                if is_valid:
                    valid_start_offsets.add(start_offset)
            if valid_start_offsets:
                results.append(WordInfo(word, valid_start_offsets))

        return results


def file_to_set(path: Path, word_dict: Optional[WordDict]) -> Set[str]:
    r = set()
    with path.open('r') as file:
        for line in file.readlines():
            line = line.rstrip()
            if line and not line.startswith("#"):
                word = line.upper()
                r.add(word)
                if word_dict is not None:
                    if not word_dict.test_word(word):  # word is not in dictionary
                        word_dict.add_word(word)
                    else:  # base word exists in dictionary. (Not worth checking if word is not in directionary)
                        plural = word + "s"
                        if word_dict.test_word(plural):
                            r.add(plural)
                        weird_plural = word[:-1] + "ies"
                        if word_dict.test_word(weird_plural):
                            r.add(weird_plural)
    return r

