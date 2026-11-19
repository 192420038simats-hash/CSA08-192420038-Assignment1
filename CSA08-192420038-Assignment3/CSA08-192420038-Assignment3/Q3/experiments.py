"""Q3 - timing: dictionary loop vs list.count() for every distinct word vs collections.Counter."""
import random, time, string
from collections import Counter
from kisan import count_with_get, count_with_setdefault, words_of, STOP_WORDS

random.seed(7)
VOCAB = ["w%03d" % i for i in range(150)] + sorted(STOP_WORDS)        # about 165 distinct words


def make_calls(n):
    # skewed choice: a few words are very common, as in real complaints
    weights = [1 / (i + 1) for i in range(len(VOCAB))]
    return [" ".join(random.choices(VOCAB, weights, k=8)) for _ in range(n)]


def count_with_list_count(texts, stop=STOP_WORDS):
    """For every distinct word, scan the whole word list with list.count(): O(n * d)."""
    words = [w for t in texts for w in words_of(t) if w not in stop]
    return {w: words.count(w) for w in set(words)}


def count_with_counter(texts, stop=STOP_WORDS):
    return dict(Counter(w for t in texts for w in words_of(t) if w not in stop))


print(f"{'complaints':>11} {'words':>9} {'distinct':>9} {'dict get s':>11} {'setdefault s':>13} {'list.count s':>13} {'Counter s':>10}  all equal")
for n in (1000, 10000, 100000):
    texts = make_calls(n)
    res = {}
    times = {}
    for name, fn in [("get", count_with_get), ("setdef", count_with_setdefault), ("listcount", count_with_list_count), ("counter", count_with_counter)]:
        t0 = time.perf_counter(); res[name] = fn(texts); times[name] = time.perf_counter() - t0
    words = sum(len(t.split()) for t in texts)
    eq = res["get"] == res["setdef"] == res["listcount"] == res["counter"]
    print(f"{n:>11} {words:>9} {len(res['get']):>9} {times['get']:>11.4f} {times['setdef']:>13.4f} {times['listcount']:>13.4f} {times['counter']:>10.4f}  {eq}")
