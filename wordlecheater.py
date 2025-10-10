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

def getPattern(wordIn, patternIn, existingPattern):
    containsAtMost = {chr(a): 5 for a in range(ord('a'), ord('z') + 1)}
    containsAtLeast = {chr(a): 0 for a in range(ord('a'), ord('z') + 1)}
    for i, char in enumerate(wordIn):
        charLower = char.lower()
        severity = patternIn[i]
        if severity == 0:
            if containsAtLeast[charLower] == 0:
                containsAtMost[charLower] = 0
            else:
                containsAtMost[charLower] = containsAtLeast[charLower]
                existingPattern[i].setMisplaced(charLower)
        else:
            if severity == 1:
                existingPattern[i].setMisplaced(charLower)
            else:
                existingPattern[i].setAbsolute(charLower)
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

test = True if sys.argv[1] == "-t" else False

lines = []
with open('words.txt', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

random.shuffle(lines)

patternStructure = [Place() for i in range(5)]
containsAtMost = {chr(a): 5 for a in range(ord('a'), ord('z') + 1)}
containsAtLeast = {chr(a): 0 for a in range(ord('a'), ord('z') + 1)}

userIn = ""

if test:
    print(lines[0])

while(True):
    userIn = input("" if test else "Enter a word or type \"exit\"\n")

    if userIn.lower() == "exit":
        exit()

    wordIn = ''.join(char for char in userIn.strip().lower() if char.isalpha())

    userIn = input("" if test else "Enter the pattern\n0 for grey, 1 for yellow, 2 for green\nex: 02110\n")
    patternIn = [int(a) for a in list(userIn.strip()) if a.isdecimal()]
    
    patternStructure, newLeast, newMost = getPattern(wordIn, patternIn, patternStructure)
    containsAtLeast = {a: max(x, containsAtLeast[a]) for (a, x) in newLeast.items()}
    containsAtMost = {a: min(x, containsAtMost[a]) for (a, x) in newMost.items()}
    regex = patternToRegex(patternStructure)
    filteredLines = [line for line in lines if (all(line.count(a) >= x for (a, x) in containsAtLeast.items()) and re.search(regex, line) and all(line.count(a) <= x for (a, x) in containsAtMost.items()))]
    if not test:
        print(regex)
        print(containsAtLeast)
        print(containsAtMost)
        print(*filteredLines, sep='\n')
    else:
        print(filteredLines[0], flush=True)
