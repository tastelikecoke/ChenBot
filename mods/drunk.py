import re
import random

class Drunk:
    words = ""
    raws = []
    tokens = []
    chain = {}
    def __init__(self):
        with open("anime.txt", "r") as animeFile:
            self.words = animeFile.read()
            self.words = re.sub(r'[^A-Za-z0-9\']+', ' ', self.words)
            self.raws = re.split(r"\s+", self.words)
            for token in self.raws:
                self.tokens.append(token.lower())
            for i in range(len(self.tokens)-2):
                if (self.tokens[i],self.tokens[i+1]) not in self.chain:
                    self.chain[(self.tokens[i],self.tokens[i+1])] = []
                    self.chain[self.tokens[i]] = []

                self.chain[(self.tokens[i],self.tokens[i+1])].append(self.tokens[i+2])
                self.chain[self.tokens[i]].append(self.tokens[i+1])
    def markov(self, length, cue1=None, cue2=None):
        previousToken = random.choice(self.tokens)
        currentToken = random.choice(self.tokens)
        output = ""
        if cue1:
            previousToken = cue1
            output += previousToken
        if cue2:
            currentToken = cue2
        for i in range(length):
            output = ' '.join([output, currentToken])
            choices = []
            if (previousToken, currentToken) in self.chain:
                choices.extend(self.chain[(previousToken, currentToken)])
            else:
                choices.extend(self.chain[(currentToken)])
            currentToken = random.choice(choices)
        return output
