"""B2 - sentences that are hard for a word-list scorer: sarcasm, double negatives, mixed opinions, and more."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "TaskB4"))
from sentiment import score, label

cases = [
    ("sarcasm",            "Oh wonderful, another day of breathing smoke. Great job, board.",                    "negative"),
    ("sarcasm",            "The app is so fast that it crashed again. Great job.",                               "negative"),
    ("double negative",    "The air is not unclean today.",                                                      "positive"),
    ("double negative",    "I can't say the air is not dirty.",                                                  "negative"),
    ("negator far away",   "The air is not very clean.",                                                         "negative"),
    ("mixed opinion",      "The staff were polite but the air is terrible and the smoke continues.",             "negative"),
    ("mixed opinion",      "The app is fast and clean but the readings are wrong and the station is broken.",    "negative"),
    ("word in other sense","The smoke detector at the school works very well.",                                  "positive"),
    ("unknown words",      "Pathetic. The pollution here is a disgrace.",                                        "negative"),
    ("question",           "Is the air clean in Adyar today?",                                                   "neutral"),
    ("plain negative",     "The air is bad and dirty.",                                                          "negative"),
]
print(f"{'type':<20}{'window 1 (given)':<18}{'window 2':<12}{'my reading':<12}sentence")
wrong1 = wrong2 = 0
for kind, text, gold in cases:
    a, b = label(text, 1), label(text, 2)
    wrong1 += a != gold; wrong2 += b != gold
    print(f"{kind:<20}{a + (' ' if a == gold else ' X'):<18}{b + (' ' if b == gold else ' X'):<12}{gold:<12}{text}")
print(f"\nwrong labels (X): window 1 = {wrong1} of {len(cases)}, window 2 = {wrong2} of {len(cases)}")
