"""The word lists and score() of complete_code.py, importable without running the demo loop."""
POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}


def score(text):
    """+1 per positive word, -1 per negative word; a preceding negator flips it."""
    words = text.lower().replace(".", " ").replace(",", " ").split()
    total = 0
    # TODO 1 done: value of each word (+1, -1 or 0); if the previous word is a negator, flip the sign; add to total
    for i, w in enumerate(words):
        value = 1 if w in POSITIVE else -1 if w in NEGATIVE else 0
        if i > 0 and words[i - 1] in NEGATORS:
            value = -value
        total += value
    return total


def label(text):
    s = score(text)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"


