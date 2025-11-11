import sys
import re
import random
import argparse
from multiprocessing import Pool
import itertools

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

def filterList(list, regex, containsAtLeast, containsAtMost):
    return [line for line in lines if (all(line.count(a) >= x for (a, x) in containsAtLeast.items()) and re.search(regex, line) and all(line.count(a) <= x for (a, x) in containsAtMost.items()))]

def theOldWay(test, lines):
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
        filteredLines = filterList(lines, regex, containsAtLeast, containsAtMost)
        if not test:
            print(regex)
            print(containsAtLeast)
            print(containsAtMost)
            print(*filteredLines, sep='\n')
        else:
            print(filteredLines[0], flush=True)

def allCombinations():
    return ["".join(a) for a in itertools.product([str(i) for i in range(3)], repeat=5)]

def smartWorker(item):
    global lines
    totalPossibilities = 0
    for combination in combinations:
        patternIn = [int(a) for a in list(combination.strip()) if a.isdecimal()]
        patternStructure = [Place() for i in range(5)]
        containsAtMost = {chr(a): 5 for a in range(ord('a'), ord('z') + 1)}
        containsAtLeast = {chr(a): 0 for a in range(ord('a'), ord('z') + 1)}
        patternStructure, containsAtLeast, containsAtMost = getPattern(item, patternIn, patternStructure)
        regex = patternToRegex(patternStructure)
        filteredList = filterList(lines, regex, containsAtLeast, containsAtMost)
        totalPossibilities += len(filteredList)
    return [item, totalPossibilities]

def smartMode():
    global lines

    random.shuffle(lines)

    patternStructure = [Place() for i in range(5)]
    containsAtMost = {chr(a): 5 for a in range(ord('a'), ord('z') + 1)}
    containsAtLeast = {chr(a): 0 for a in range(ord('a'), ord('z') + 1)}

    userIn = ""

    while(True):
        userIn = input("Enter a word or type \"exit\"\n")

        if userIn.lower() == "exit":
            exit()

        wordIn = ''.join(char for char in userIn.strip().lower() if char.isalpha())

        userIn = input("Enter the pattern\n0 for grey, 1 for yellow, 2 for green\nex: 02110\n")
        patternIn = [int(a) for a in list(userIn.strip()) if a.isdecimal()]
        
        patternStructure, newLeast, newMost = getPattern(wordIn, patternIn, patternStructure)
        containsAtLeast = {a: max(x, containsAtLeast[a]) for (a, x) in newLeast.items()}
        containsAtMost = {a: min(x, containsAtMost[a]) for (a, x) in newMost.items()}
        regex = patternToRegex(patternStructure)
        lines = filterList(lines, regex, containsAtLeast, containsAtMost)

        print(regex)
        print(containsAtLeast)
        print(containsAtMost)

        with Pool() as pool:
            optimals = sorted(pool.map(smartWorker, lines), key=lambda item: -item[1])

        print(*optimals, sep='\n')

parser = argparse.ArgumentParser()

parser.add_argument("--test", "-t", action='store_true')
parser.add_argument('--new', '-n', action='store_true')

args = parser.parse_args()

combinations = allCombinations()
print(combinations)

lines = []
with open('words.txt', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

if not args.new:
    theOldWay(args.test, lines)
else:
    smartMode()

