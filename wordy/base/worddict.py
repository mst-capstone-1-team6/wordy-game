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
        new.words = words
        return new


    def trim_by_length(self, min: int = 0, max: int = 15) -> WordDict:
        """Returns a new dictonary which contains only the words in self which fall between the given lengths"""
        return WordDict.from_list([word for word in self.words if len(word) < max and len(word) > min])


    def trim_by_letters(self, lets: List[str] = []) -> WordDict:
        """Returns a new dictionary which contains only the words in self which contain the given letters"""
        return WordDict.from_list([word for word in self.words if all([1 if word.find(let) != -1 else 0 for let in lets])])


    def test_word(self, test: str) -> bool:
        return test.upper() in self.words


    def find_one_letter(self, set_let: str, index_in_word: List[int]) -> List[WordInfo]:
        """Find all words in the dictionary which contain the given letter
           at somewhere in the given range of indexes"""
        set_let = set_let.upper()
        #Generate list of all words containing the given letter
        results = [word for word in self.words if word.find(set_let) != -1]
        #Restrict words to only contain the letter at the given indexes
        results = [word for word in results if len(set([i for i, x in enumerate(word) if x == set_let]).intersection(index_in_word)) > 0]

        return WordDict.from_list(results)


    def find_many_letters(self, lets: List[str], offsets: List[int]) -> List[WordInfo]:
        """Find all words in the dictionary which contain the given letters at the given relative offsets
           eg. find_many_letters(["a", "l"], [0, 1]) will return a list like ["ale", "all", "allow", "evaluate", "seasonal", ...]
               find_many_letters(["e", "s"], [0, 4]) will return a list like ["warehouse", "tunnelers", "snivelers", ...]
               find_many_letters(["l", "a", "e"], [-2, -1, 3]) will return a list like ["lawbreaking", "planeness", "plaintext"]
        """
        lets = [let.upper() for let in lets]
        max_offset = max(offsets)
        min_offset = min(offsets)
        first_let = lets[offsets.index(min_offset)]
        #Generate list of all words containing the given letters of a valid length and letters
        temp = self.trim_by_letters(lets)
        temp = temp.trim_by_length(min = max_offset - min_offset)
        #Restrict words to only have the correct letters at the correct offsets
        results = []
        for word in temp.words:
            #Create the lists of letter locations: adjusting for the offsets
            pos_sets = []
            for i, set_let in enumerate(lets):
                temp_set = set()
                for j, let in enumerate(word):
                    if set_let == let:
                        #Subtracting the offsets lines everything up to the index of the starting letter of that set of letters
                        temp_set.add(j - offsets[i])
                pos_sets.append(temp_set)
            
            if len(set.intersection(*pos_sets)) > 0:
                #TODO: Fix this to return a vaid WordIfo containing the word and the set of posible start positions of the word
                #This should be equivalent to the commented set-comprehension below it I think
                """
                start_set = set{}
                for index in [i for i, x in enumerate(word) if x == first_let]:
                    temp = []
                    for i, let in enumerate(word[index:]):
                        for j, offset in enumerate(offsets):
                            if offset - min_offset == i:
                                if lets[j] == let:
                                    temp.append(1)
                                else:
                                    temp.append(0)
                    if all(temp):
                        start_set.add(min_offset - index)        
                """
                #results.append(WordInfo(word, start_set))
                results.append(word)
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

