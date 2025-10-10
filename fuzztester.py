from subprocess import Popen, PIPE
import time
import os

wordleProc = Popen(['python3', './wordle.py', '-t'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
cheaterProc = Popen(['python3', './wordlecheater.py', '-t'], stdout=PIPE, stderr=PIPE, stdin=PIPE)

guessCount = 0
while(True):
    time.sleep(0.001)
    print("getting cheater response")
    guess = cheaterProc.stdout.readline()
    print(guess.decode("utf-8"))
    print("sending to wordle")
    wordleProc.stdin.write(guess)
    wordleProc.stdin.flush()
    ##wordleProc.stdin.write(linesep)
    time.sleep(0.001)
    print("getting wordle response")
    hint = wordleProc.stdout.readline()
    print(hint.decode("utf-8"))
    try:
        guessCount = int(str(hint.decode('utf-8')).strip())
        break
    except ValueError:
        print("sending to cheater")
        cheaterProc.stdin.write(guess)
        cheaterProc.stdin.write(hint)
        cheaterProc.stdin.flush()
        ##cheaterProc.stdin.write(linesep)

print(guessCount)