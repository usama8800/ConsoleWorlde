import json
import os
import random
from typing import List

# if on windows
if os.name == "nt":
    import msvcrt as console
else:
    import getch as console


class ANSI:
    RESET = "\x1b[0m"
    UNDERLINE = "\x1b[4m"
    GREEN = "\x1b[7;30;42m"
    YELLOW = "\x1b[7;30;43m"
    PREV_LINE = "\x1b[F"
    ERASE_LINE = "\x1b[K"
    START_LINE = "\x1b[G"
    ERASE_SCREEN = "\x1b[2J\x1b[;H"


with open("all_words.json", "r") as f:
    all_words: List[str] = json.load(f)
with open("answers.json", "r") as f:
    answers: List[str] = json.load(f)


def getch():
    ch = console.getch()
    try:
        char = ch.decode("utf-8")
    except AttributeError:
        char = ch
    return char


def getInput():
    x = ""
    print(f"_ _ _ _ _{ANSI.START_LINE}", end="", flush=True)
    while True:
        char = getch()
        if char == "\x1b":
            return False

        if char in ["\r", "\n"] and (x in all_words or x in answers):
            print(f"{ANSI.START_LINE}{ANSI.ERASE_LINE}", end="", flush=True)
            return x

        if char == "\b":
            if len(x) < 5:
                print("\b", end="", flush=True)
            x = x[:-1]
            print(f"\b{ANSI.UNDERLINE} {ANSI.RESET}\b", end="", flush=True)

        if len(x) >= 5:
            continue
        if not char.isalpha():
            continue
        x += char
        print(f"{ANSI.UNDERLINE}{char.upper()}{ANSI.RESET}", end="", flush=True)
        if len(x) < 5:
            print(" ", end="", flush=True)


def rateWord(x: str, chosen: str):
    ret = []
    for i, letter in enumerate(x):
        indices = [j for j, v in enumerate(chosen) if v == letter]

        if i in indices:
            ret.append(1)
        elif len(indices) > 0:
            ret.append(0)
        else:
            ret.append(-1)
    return ret


def printRatedWord(x: str, rates: list[int]):
    for letter, rate in zip(x, rates):
        prefix = ANSI.UNDERLINE
        if rate == 1:
            prefix += ANSI.GREEN
        if rate == 0:
            prefix += ANSI.YELLOW
        print(prefix + letter.upper() + "\x1b[0m ", end="")
    print("\n")


def attempt(chosen: str):
    x = getInput()
    if x == False:
        return -1
    rates = rateWord(x, chosen)
    printRatedWord(x, rates)
    if 0 in rates or -1 in rates:
        return 0
    return 1


print(ANSI.ERASE_SCREEN)
while True:
    print(ANSI.ERASE_SCREEN)
    chosen = random.choice(answers)
    tries = 6
    while tries > 0:
        tries -= 1
        ret = attempt(chosen)
        if ret == 1:
            print("Correct\n")
            break
        if ret == -1:
            tries = 0
    else:
        print(f"Word was {chosen.upper()}\n")
    print("Press enter to start new game (q/n/esc to quit)")
    char = getch()
    if char.lower() in ["\x1b", "q", "n"]:
        break
