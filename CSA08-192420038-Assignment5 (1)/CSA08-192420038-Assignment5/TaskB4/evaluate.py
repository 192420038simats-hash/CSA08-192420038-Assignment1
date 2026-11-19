"""B4.1 - sentiment scorer and summariser on 52 complaints, compared with my own reading; first-k alternative."""
import time
from collections import Counter
from complaints import COMPLAINTS
from sentiment import label, summarise, first_k, words_of

n = len(COMPLAINTS)
print(f"{n} complaints; my own reading: {dict(Counter(g for _, g, _ in COMPLAINTS))}\n")
for window in (1, 2):
    pred = [label(t, window) for t, _, _ in COMPLAINTS]
    agree = sum(p == g for p, (_, g, _) in zip(pred, COMPLAINTS))
    print(f"Sentiment scorer, negation window {window}: agrees with me on {agree} of {n} = {agree / n:.1%}")
    cm = Counter((g, p) for p, (_, g, _) in zip(pred, COMPLAINTS))
    print(f"   {'my reading \\ scorer':<22}{'positive':>9}{'negative':>9}{'neutral':>9}")
    for g in ("positive", "negative", "neutral"):
        print(f"   {g:<22}{cm[(g, 'positive')]:>9}{cm[(g, 'negative')]:>9}{cm[(g, 'neutral')]:>9}")
pred1 = [label(t, 1) for t, _, _ in COMPLAINTS]
print("\nComplaints labelled differently from my reading (window 1):")
for p, (t, g, _) in zip(pred1, COMPLAINTS):
    if p != g:
        print(f"   scorer {p:<8} me {g:<8} | {t[:100]}")

print("\nSummariser: does the 1-sentence summary contain the key topic word?")
def covers(fn, k):
    return sum(topic in words_of(fn(t, k)) or topic in fn(t, k).lower() for t, _, topic in COMPLAINTS)
for k in (1, 2):
    a, b = covers(summarise, k), covers(first_k, k)
    print(f"   k = {k}:  most-frequent-words summary {a:>2} of {n} = {a/n:.0%}     first-{k}-sentences summary {b:>2} of {n} = {b/n:.0%}")
for i in (2, 5, 9):
    t, g, topic = COMPLAINTS[i]
    print(f"\n   complaint : {t}\n   frequent  : {summarise(t, 1)}\n   first     : {first_k(t, 1)}")

print("\nTime per complaint and for a month of 50,000 complaints")
texts = [t for t, _, _ in COMPLAINTS] * 1000                      # 52,000 complaints
for name, fn in (("sentiment label()", label), ("summarise(k=1)", summarise), ("first_k(k=1)", first_k)):
    t0 = time.perf_counter()
    for t in texts: fn(t)
    el = time.perf_counter() - t0
    print(f"   {name:<20}{el / len(texts) * 1e6:>8.1f} microseconds per complaint   {el / len(texts) * 50_000:>6.2f} s for 50,000 complaints")

# ---------- how reliable is the 94 % ? ----------
print("\n--- fairness checks ---")
from complete_code_lexicon import label as label_small          # the small word lists of the 'Complete the Code'
agree = sum(label_small(t) == g for t, g, _ in COMPLAINTS)
print(f"1. Only the 11 words of the 'Complete the Code' lists: agrees on {agree} of {n} = {agree / n:.1%}")
from holdout import HOLDOUT
for window in (1, 2):
    agree = sum(label(t, window) == g for t, g, _ in HOLDOUT)
    print(f"2. 12 NEW complaints written after the word lists were frozen (window {window}): agrees on {agree} of {len(HOLDOUT)} = {agree / len(HOLDOUT):.1%}")
for t, g, _ in HOLDOUT:
    p = label(t, 1)
    if p != g:
        print(f"      scorer {p:<8} me {g:<8} | {t[:95]}")
print("   (the first 52 complaints were read while the 60-word lists were chosen, so 94 % is optimistic)")
