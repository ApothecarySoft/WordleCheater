import sys
import re
import random

class Place:

    def __init__(self):
        self.severity = 0
        self.characters = []

    def setMisplaced(self, char):
        if self.severity <= 1:
            self.severity = 1
            self.characters.append(char)

    def setAbsolute(self, char):
        if self.severity < 2:
            self.severity = 2
            self.characters = [char]

    def getCharacters(self):
        return "".join(self.characters).lower()

def getPattern(patternString, existingPattern):
    banNextChar = False
    specialCharCount = 0
    for i, char in enumerate(patternString):
        idx = i - specialCharCount
        charLower = char.lower()
        if banNextChar:
            if charLower not in mustContain:
                mustNotContain.add(charLower)
            else:
                existingPattern[idx].setMisplaced(charLower)
            banNextChar = False
        elif char == '!':
            banNextChar = True
            specialCharCount += 1
        elif char.isalpha():
            if char.islower():
                existingPattern[idx].setMisplaced(charLower)
            else:
                existingPattern[idx].setAbsolute(charLower)
            if charLower in mustNotContain:
                mustNotContain.remove(charLower)
            mustContain.add(charLower)
    return existingPattern

def patternToRegex(pattern):
    regex = r""
    for val in pattern:
        if val.severity == 0:
            regex += '.'
        elif val.severity == 1:
            regex += f"[^{val.getCharacters()}]"
        else:
            regex += val.getCharacters()
    return regex


lines = []
with open('words.txt', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

random.shuffle(lines)

mustContain = set()
mustNotContain = set()
patternStructure = [Place() for i in range(5)]

userIn = ""

while(True):
    userIn = input("Add your next pattern or type exit\nblack char: !char\nyellow char: lowercase char\ngreen char: uppercase char\n")

    if userIn.lower() == "exit":
        exit()

    patternIn = userIn.strip()
    patternStructure = getPattern(patternIn, patternStructure)
    regex = patternToRegex(patternStructure)
    filteredLines = [line for line in lines if (all(ch in line for ch in mustContain) and re.search(regex, line) and all(ch not in line for ch in mustNotContain))]
    print(regex)
    print(mustContain)
    print(mustNotContain)
    print(*filteredLines, sep='\n')
