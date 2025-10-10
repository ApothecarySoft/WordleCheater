import random
import sys

test = True if sys.argv[1] == "-t" else False

lines = []
with open('words.txt', 'r') as file:
    lines = [line.lower().strip() for line in file.readlines()]

word = random.choice(lines)
print(word, flush=True)

guessCounter = 0

while(True):
    guessCounter += 1
    guessStr = input().lower().strip()

    hint = [0 for i in range(5)]

    if guessStr == word:
        break;

    for i in range(5):
        guessChar = guessStr[i]
        wordChar = word[i]
        if guessChar == wordChar:
            hint[i] = 2
        elif guessChar in word:
            hint[i] = 1

    for guessChar in set(guessStr):
        countDiff = guessStr.count(guessChar) - word.count(guessChar)
        if countDiff > 0:
            for j in [k for k in range(5) if hint[k] == 1 and guessStr[k] == guessChar][:countDiff]:
                hint[j] = 0


    print(hint, flush=True)

if test:
    print(guessCounter, flush=True)
else:
    print("you guessed it!")