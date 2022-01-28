import json
from typing import List

with open("all_words.json", "r") as f:
    words: List[str] = json.load(f)
with open("answers.json", "r") as f:
    answers: List[str] = json.load(f)
    words.extend(answers)


def getWordScore(word: str):
    score = 0
    letters_done = []
    for letter in word:
        if letter in letters_done:
            continue
        letters_done.append(letter)
        score += freqs[letter]
    return score


def deepFlatten(lst):
    ret = []
    for item in lst:
        if isinstance(item, list) or isinstance(item, str) and len(item) > 1:
            ret.extend(deepFlatten(item))
        else:
            ret.append(item)
    return ret


# calculate frequencies of all letters in answers
freqs = {}
for word in answers:
    letters_done = []
    for letter in word:
        if letter in letters_done:
            continue
        letters_done.append(letter)

        if letter not in freqs:
            freqs[letter] = 0
        freqs[letter] += 1
# sort freqs
sorted_freqs = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
print([a for a, b in sorted_freqs[:20]])  # dgbfw

# score all words in words
scores = {word: getWordScore(word) for word in words}

top_words = []
# sort scores
sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
top_words.append(sorted_scores[0][0])

n = 3
for i in range(1, n):
    filtered_scores = []
    for word, score in sorted_scores:
        # if letters in word are in top_word, filter them
        if any(letter in deepFlatten(top_words) for letter in word):
            continue
        filtered_scores.append((word, score))
    sorted_scores = filtered_scores
    top_words.append(sorted_scores[0][0])
print(top_words)

sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

filtered_scores = []
for word, score in sorted_scores:
    if all(letter in word for letter in ["d", "g", "b"]):
        filtered_scores.append((word, score))
print(filtered_scores[0][0])
