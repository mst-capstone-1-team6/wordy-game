from __future__ import annotations
from typing import List

class WordDict():
    """To create a new WordDict use either WordDict.from_file() or WordDict.from_list()"""
    def __init__(self):
        self.words = []
    
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
    
    def testWord(self, test: str) -> bool:
        if test.upper() in self.words:
            return True
        else:
            return False

    def find_one_letter(self, set_let: str, index_in_word: List[int]) -> WordDict:
        """Find all words in the dictionary which contain the given letter
           at somewhere in the given range of indexes"""
        set_let = set_let.upper()
        #Generate list of all words containing the given letter
        results = [word for word in self.words if word.find(set_let) != -1]
        #Restrict words to only contain the letter at the given indexes
        results = [word for word in results if len(set([i for i, x in enumerate(word) if x == set_let]).intersection(index_in_word)) > 0]
        
        return WordDict.from_list(results)
    
    def find_many_letters(self, lets: List[str], offsets: List[int]) -> WordDict:
        """Find all words in the dictionary which contain the given letters at the given relative offsets
           eg. find_many_letters(["a", "l"], [0, 1]) will return a list like ["ale", "all", "allow", "evaluate", "seasonal", ...]
               find_many_letters(["e", "s"], [0, 4]) will return a list like ["warehouse", "tunnelers", "snivelers", ...]
               find_many_letters(["l", "a", "e"], [-2, -1, 3]) will return a list like ["lawbreaking", "planeness", "plaintext"]
        """
        lets = [let.upper() for let in lets]
        #Generate list of all words containing the given letters of a valid length
        temp = self.trim_by_letters(lets)
        temp = temp.trim_by_length(min = max(offsets) - min(offsets))
        #Restrict words to only have the correct letters at the correct offsets
        results = []
        for word in temp:
            #Create the lists of letter locations: adjusting for the offsets
            pos_sets = []
            for i, set_let in enumerate(lets):
                temp_set = set()
                for j, let in enumerate(word):
                    if set_let == let:
                        #Subtracting the offsets lines everything up to the index of the starting letter
                        temp_set.add(j - offsets[i])
                pos_sets.append(temp_set)
            if len(set.intersection(*pos_sets)) > 0:
                results.append(word)
        return WordDict.from_list(results)
 