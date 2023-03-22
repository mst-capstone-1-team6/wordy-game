from __future__ import annotations
from typing import List

class WordDict():
    """To create a new WordDict use either WordDict.fromFile() or WordDict.fromList()"""
    def __init__(self):
        self.words = []
    
    @classmethod
    def fromFile(cls, fileName: str) -> WordDict:
        new = cls.__new__(cls)
        with open(fileName, "r") as f:
            new.words: List[str] = [i.rstrip() for i in f.readlines()]
        return new
    
    @classmethod
    def fromList(cls, words: List[str]) -> WordDict:
        new = cls.__new__(cls)
        new.words = words
        return new
    
    def trimByLength(self, min: int = 0, max: int = 15) -> WordDict:
        """Returns a new dictonary which contains only the words in self which fall between the given lengths"""
        return WordDict.fromList([word for word in self.words if len(word) < max and len(word) > min])
    
    #TODO: Make work
    def trimByLetters(self, lets: List[str] = []) -> WordDict:
        """Returns a new dictionary which contains only the words in self which contain exactly the given letters"""
        letSet = set(lets)
        return WordDict.fromList([word for word in self.words if letSet.issuperset(word)])
    
    def testWord(self, test: str) -> bool:
        if test.upper() in self.words:
            return True
        else:
            return False

    def findOneLetter(self, setLet: str, indexInWord: List[int]) -> List[str]:
        """Find all words in the dictionary which contain the given letter
           at somewhere in the given range of indexes"""
        setLet = setLet.upper()
        #Generate list of all words containing the given letter
        results = [word for word in self.words if word.find(setLet) != -1]
        #Restrict words to only contain the letter at the given indexes
        results = [word for word in results if len(set([i for i, x in enumerate(word) if x == setLet]).intersection(indexInWord)) > 0]
        
        return results
    
    def findManyLetters(self, lets: List[str], offsets: List[int]):
        """Find all words in the dictionary which contain the given letters at the given relative offsets
           eg. findManyLetters(["a", "l"], [0, 1]) will return a list like ["ale", "all", "allow", "evaluate", "seasonal", ...]
               findManyLetters(["e", "s"], [0, 4]) will return a list like ["warehouse", "tunnelers", "snivelers", ...]
               findManyLetters(["l", "a", "e"], [-2, -1, 3]) will return a list like ["lawbreaking", "planeness", "plaintext"]
        """
        lets = [let.upper() for let in lets]
        #Generate list of all words containing the given letters
        temp = [word for word in self.words if all([1 if word.find(let) != -1 else 0 for let in lets])]
        #Restrict words to only have the correct letters at the correct offsets
        results = []
        for word in temp:
            #If the largest offset if larger than the word, we can safely discard that word
            if len(word) <= max(offsets) - min(offsets):
                continue
            #Create the lists of letter locations: adjusting for the offsets
            posSets = []
            for i, setLet in enumerate(lets):
                tempSet = set()
                for j, let in enumerate(word):
                    if setLet == let:
                        #Subtracting the offsets lines everything up to the index of the starting letter
                        tempSet.add(j - offsets[i])
                posSets.append(tempSet)
            if len(set.intersection(*posSets)) > 0:
                results.append(word)
        return results
