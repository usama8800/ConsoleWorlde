import json
import os
import random
import sys
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
    GREY = "\x1b[7;30;98m"
    PREV_LINE = "\x1b[F"
    NEXT_LINE = "\x1b[E"
    ERASE_LINE = "\x1b[K"
    START_LINE = "\x1b[G"
    ERASE_SCREEN = "\x1b[2J\x1b[;H"
    ERASE_BELOW = "\x1b[J"


with open("all_words.json", "r") as f:
    all_words: List[str] = json.load(f)
with open("answers.json", "r") as f:
    answers: List[str] = json.load(f)

greens = []
yellows = []
greys = []


def getch():
    ch = console.getch()
    try:
        char = ch.decode("utf-8")
    except AttributeError:
        char = ch
    return char


def printKeyboard():
    r1 = "qwertyuiop"
    r2 = "asdfghjkl"
    r3 = " zxcvbnm"
    print(ANSI.NEXT_LINE * 2, end="")
    for i, row in enumerate([r1, r2, r3]):
        if i > 0:
            print(" ", end="")
        for letter in row:
            if letter in greens:
                print(ANSI.GREEN, end="")
            if letter in yellows:
                print(ANSI.YELLOW, end="")
            if letter in greys:
                print(ANSI.GREY, end="")
            print(letter.upper(), end=" " + ANSI.RESET)
        print("")
    print(ANSI.PREV_LINE * 5, end="")


def getInput():
    x = ""
    print(f"_ _ _ _ _{ANSI.START_LINE}", end="")
    printKeyboard()
    while True:
        print("", end="", flush=True)
        char = getch()
        if char == "\x1b":
            return False

        if char in ["\r", "\n"] and (x in all_words or x in answers):
            print(f"{ANSI.START_LINE}{ANSI.ERASE_BELOW}", end="")
            return x

        if char in ["\b", "\x7f"]:
            if len(x) == 0:
                continue
            if len(x) < 5:
                print("\b", end="")
            x = x[:-1]
            print(f"\b{ANSI.UNDERLINE} {ANSI.RESET}\b", end="")

        if len(x) >= 5:
            continue
        if not char.isalpha():
            continue
        x += char
        print(f"{ANSI.UNDERLINE}{char.upper()}{ANSI.RESET}", end="")
        if len(x) < 5:
            print(" ", end="")


def rateWord(x: str, chosen: str):
    ret = [-1] * 5
    chosen_indices_done = []
    for i, letter in enumerate(x):
        if chosen[i] == letter:
            ret[i] = 1
            chosen_indices_done.append(i)
    for i, letter in enumerate(x):
        if ret[i] == 1:
            continue
        for j, letter1 in enumerate(chosen):
            if j in chosen_indices_done:
                continue
            if letter1 == letter:
                ret[i] = 0
                chosen_indices_done.append(j)
                break
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
    for letter, rate in zip(x, rates):
        if letter in greens or letter in greys:
            continue
        if rate == 1:
            greens.append(letter)
            if letter in yellows:
                yellows.remove(letter)
        if rate == 0 and letter not in yellows:
            yellows.append(letter)
        if rate == -1:
            greys.append(letter)
    printRatedWord(x, rates)
    if 0 in rates or -1 in rates:
        return 0
    return 1


def main(defaultChosenWord=None):
    global greens, yellows, greys
    print(ANSI.ERASE_SCREEN)
    while True:
        print(ANSI.ERASE_SCREEN)
        greens = []
        yellows = []
        greys = []
        if defaultChosenWord:
            chosen = defaultChosenWord
        else:
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
                print(ANSI.ERASE_BELOW, end="")
        else:
            if tries < 5:
                print(f"Word was {chosen.upper()}\n")
        print("Press enter to start new game (q/n/esc to quit)")
        char = getch()
        if char.lower() in ["\x1b", "q", "n"]:
            print(ANSI.ERASE_SCREEN)
            break


def test(chosen: str, x: str):
    rating = rateWord(x, chosen)
    print(rating)
    printRatedWord(x, rating)


if __name__ == "__main__":
    args = sys.argv[1:]
    testWord = None
    chosenWord = None
    for arg in args:
        key = arg
        val = None
        if arg.startswith("--"):
            key = arg[2 : arg.index("=")]
            val = arg[arg.index("=") + 1 :]

        if key == "test":
            testWord = val
        elif key == "word":
            chosenWord = val
        else:
            print(f"Unknown argument {key}")
            exit(1)
    if testWord is not None and chosenWord is None:
        print("You must specify a word to test")
        exit(1)

    if testWord is not None:
        test(chosenWord, testWord)
    else:
        main(chosenWord)
