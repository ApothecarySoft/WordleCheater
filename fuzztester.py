from subprocess import Popen, PIPE
import time
import os

bigGuessCount = 0
winCount = 0
maxGuessCount = 0
minGuessCount = 100000
fuzzIterations = 500
for i in range(fuzzIterations):
    wordleProc = Popen(['python3', './wordle.py', '-t'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
    cheaterProc = Popen(['python3', './wordlecheater.py', '-t'], stdout=PIPE, stderr=PIPE, stdin=PIPE)

    guessCount = 0
    while(True):
        #print("getting cheater response")
        guess = cheaterProc.stdout.readline()
        #print(guess.decode("utf-8"))
        #print("sending to wordle")
        wordleProc.stdin.write(guess)
        wordleProc.stdin.flush()
        #print("getting wordle response")
        hint = wordleProc.stdout.readline()
        #print(hint.decode("utf-8"))
        try:
            guessCount = int(str(hint.decode('utf-8')).strip())
            break
        except ValueError:
            #print("sending to cheater")
            cheaterProc.stdin.write(guess)
            cheaterProc.stdin.write(hint)
            cheaterProc.stdin.flush()
    bigGuessCount += guessCount
    maxGuessCount = max(guessCount, maxGuessCount)
    minGuessCount = min(guessCount, minGuessCount)
    if guessCount <= 6:
        winCount += 1

print(bigGuessCount / fuzzIterations)
print(maxGuessCount)
print(minGuessCount)
print(winCount / fuzzIterations)