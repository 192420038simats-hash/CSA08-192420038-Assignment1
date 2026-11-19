"""Q3 - Kisan call centre: word frequencies (get / setdefault), complaints per district and per crop, top k."""
import string

STOP_WORDS = {"not", "high", "the", "a", "is", "are", "of", "to", "and", "in", "for", "my", "has", "have", "was", "very"}


def words_of(text):
    """Lower-case words with surrounding punctuation removed; empty tokens dropped."""
    return [w for w in (t.strip(string.punctuation).lower() for t in text.split()) if w]


def count_with_get(texts, stop=STOP_WORDS):
    """Word -> count using dict.get(word, 0) + 1."""
    counts = {}
    for text in texts:
        for w in words_of(text):
            if w not in stop:
                counts[w] = counts.get(w, 0) + 1
    return counts


def count_with_setdefault(texts, stop=STOP_WORDS):
    """Same result, written with dict.setdefault(word, 0)."""
    counts = {}
    for text in texts:
        for w in words_of(text):
            if w not in stop:
                counts[w] = counts.setdefault(w, 0) + 1
    return counts


def top_k(counts, k):
    """k most frequent (word, count), highest count first, ties alphabetical."""
    return sorted(counts.items(), key=lambda p: (-p[1], p[0]))[:k]


def group_by(records, key):
    """Dictionary of lists: group complaint records by the field `key` using setdefault."""
    groups = {}
    for rec in records:
        groups.setdefault(rec[key], []).append(rec["text"])
    return groups


if __name__ == "__main__":
    complaints = [
        {"district": "Thanjavur", "crop": "paddy", "text": "Seeds not received, seeds delayed!"},
        {"district": "Madurai", "crop": "cotton", "text": "Fertiliser price HIGH"},
        {"district": "Thanjavur", "crop": "paddy", "text": "seeds price high; subsidy not received."},
        {"district": "Salem", "crop": "turmeric", "text": ""},
        {"district": "Madurai", "crop": "cotton", "text": "Pump is not working. Pump repair delayed"},
    ]
    texts = [c["text"] for c in complaints]
    a, b = count_with_get(texts), count_with_setdefault(texts)
    print("get() version      :", top_k(a, 5))
    print("setdefault() version:", top_k(b, 5), " same:", a == b)
    by_district = group_by(complaints, "district")
    print("\ncomplaints per district:", {d: len(v) for d, v in by_district.items()})
    for d, v in by_district.items():
        print(f"  {d}: {v}")
    print("complaints per crop    :", {c: len(v) for c, v in group_by(complaints, "crop").items()})
    print("\nviews:")
    d = {"seeds": 3, "price": 2}
    ks, vs, its = d.keys(), d.values(), d.items()
    print("  keys()  :", ks, " values():", vs, " items():", its)
    d["subsidy"] = 1
    print("  after adding a key the views change too (they are live):", ks, vs)
    print("\nedge cases")
    print("  empty text           ->", count_with_get([""]), count_with_get([]))
    print("  upper/lower case     ->", count_with_get(["Seeds SEEDS seeds"]))
    print("  punctuation          ->", count_with_get(["seeds, seeds. (seeds)! 'seeds'"]))
