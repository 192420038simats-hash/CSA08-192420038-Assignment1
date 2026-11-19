"""Lexicon-based sentiment scorer with negation, and an extractive summariser (designs A5.1)."""
import re

POSITIVE = {"good", "clean", "cleaner", "fast", "helpful", "improved", "better", "great", "quick", "quickly", "polite", "fresh", "safe",
            "thank", "thanks", "excellent", "resolved", "pleasant", "easy", "useful", "clear", "fixed", "wonderful", "patiently"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken", "polluted", "worse", "terrible", "awful", "foul", "toxic", "unsafe",
            "unbearable", "choking", "stinks", "stink", "ignored", "dangerous", "worried", "noise", "coughing", "cough", "ill", "wrong", "burning",
            "dusty", "dust", "fumes", "garbage"}
NEGATORS = {"not", "never", "no", "cannot", "nobody", "nothing"}


def words_of(text):
    return re.findall(r"[a-z']+", text.lower())


def score(text, window=1):
    """+1 per positive word, -1 per negative word; a negator within the previous `window` words flips it.
    window = 1 is the version of the 'Complete the Code'; window = 2 also handles 'not very good'."""
    words, total = words_of(text), 0
    for i, w in enumerate(words):
        value = 1 if w in POSITIVE else -1 if w in NEGATIVE else 0
        if value and any(p in NEGATORS for p in words[max(0, i - window):i]):
            value = -value
        total += value
    return total


def label(text, window=1):
    s = score(text, window)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"


STOP = set("the a an and or but is are was were be been to of in on at for with from by this that these those it its i my our we you your they "
           "their he she his her as so very also just please sir hello good morning thank thanks has have had will can could would not no do does did "
           "there here again still now today every all any some what when which who how if then than about near".split())


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def summarise(text, k=1):
    """Extractive summary: the k sentences with the highest total frequency of important (non-stop) words, in original order."""
    sents = sentences(text)
    if len(sents) <= k:
        return " ".join(sents)
    freq = {}
    for w in words_of(text):
        if w not in STOP and len(w) > 2:
            freq[w] = freq.get(w, 0) + 1
    scored = [(sum(freq.get(w, 0) for w in words_of(s)), -i, s) for i, s in enumerate(sents)]     # ties: earlier sentence wins
    best = sorted(scored, reverse=True)[:k]
    return " ".join(s for _, _, s in sorted(best, key=lambda t: -t[1]))


def first_k(text, k=1):
    return " ".join(sentences(text)[:k])
