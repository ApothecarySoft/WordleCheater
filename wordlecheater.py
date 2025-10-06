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
    containsAtMost = {chr(a): 5 for a in range(ord('a'), ord('z') + 1)}
    containsAtLeast = {chr(a): 0 for a in range(ord('a'), ord('z') + 1)}
    for i, char in enumerate(patternString):
        idx = i - specialCharCount
        charLower = char.lower()
        if banNextChar:
            if containsAtLeast[charLower] == 0:
                containsAtMost[charLower] = 0
            else:
                containsAtMost[charLower] = containsAtLeast[charLower]
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
            containsAtLeast[charLower] += 1
            containsAtMost[charLower] = max(containsAtLeast[charLower], containsAtMost[charLower])
    return existingPattern, containsAtLeast, containsAtMost

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

patternStructure = [Place() for i in range(5)]
containsAtMost = {chr(a): 5 for a in range(ord('a'), ord('z') + 1)}
containsAtLeast = {chr(a): 0 for a in range(ord('a'), ord('z') + 1)}

userIn = ""

while(True):
    userIn = input("Add your next pattern or type exit\nblack char: !char\nyellow char: lowercase char\ngreen char: uppercase char\n")

    if userIn.lower() == "exit":
        exit()

    patternIn = userIn.strip()
    patternStructure, newLeast, newMost = getPattern(patternIn, patternStructure)
    containsAtLeast = {a: max(x, containsAtLeast[a]) for (a, x) in newLeast.items()}
    containsAtMost = {a: min(x, containsAtMost[a]) for (a, x) in newMost.items()}
    regex = patternToRegex(patternStructure)
    filteredLines = [line for line in lines if (all(line.count(a) >= x for (a, x) in containsAtLeast.items()) and re.search(regex, line) and all(line.count(a) <= x for (a, x) in containsAtMost.items()))]
    print(regex)
    print(containsAtLeast)
    print(containsAtMost)
    print(*filteredLines, sep='\n')
