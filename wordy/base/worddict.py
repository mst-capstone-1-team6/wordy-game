from typing import Tuple, Dict, Optional, Literal, List

class WordDict():
    def __init__(self, dictFile: str):
        with open(dictFile, "r") as f:
            self.words: List[str] = [i.rstrip() for i in f.readlines()]
    
    def testWord(self, test: str) -> bool:
        if test.upper() in self.words:
            return True
        else:
            return False

    #TODO: Add multiple letter functionality from distance between letters
    def findPossibleWords(self, setLet: str, indexInWord: List[int]):
        """Find all words in the dictionary which contain the given letter
           at somewhere in the given range of indexes"""
        setLet = setLet.upper()
        #Generate list of all words containing the given letter
        results = [word for word in self.words if word.find(setLet) != -1]

        #Restrict words to only contain the letter at the given indexes
        results = [word for word in results if len(set([i for i, x in enumerate(word) if x == setLet]).intersection(indexInWord)) > 0]
        
        return results