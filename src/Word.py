import json
import random

from flet import size
class Word:
    def __init__(self):
        with open("src/assets/words.json") as f:
            self.word_list = json.load(f)
        random.SystemRandom()

    def getRandomizeWord(self):
        return self.word_list[random.randint(0, len(self.word_list))].upper()
    def isAWord(self, guessWord:str):
        return guessWord in self.word_list

        
