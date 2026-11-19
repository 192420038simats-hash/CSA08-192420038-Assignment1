"""Q7 - time for 1,000 and 100,000 contacts: dictionary grouping vs comparing every pair."""
import random, time, sys
from contacts import merge_contacts, merge_pairwise

FIRST = ["Ravi", "Meena", "Arun", "Latha", "Kumar", "Divya", "Suresh", "Anita", "Karthik", "Priya"]
LAST = ["Kumar", "S", "R", "Iyer", "Raj", "Devi", "N", "M"]


def fmt_number(d, rnd):
    return rnd.choice([f"+91 {d[:5]} {d[5:]}", d, f"0{d[:5]} {d[5:]}", f"+91-{d[:5]}-{d[5:]}", f"{d[:3]}-{d[3:6]}-{d[6:]}"])


def make_contacts(n, seed=9):
    """n contacts = n/2 people, each stored twice with different spelling/format and at least one shared number."""
    rnd = random.Random(seed)
    people = n // 2
    numbers = rnd.sample(range(7_000_000_000, 10_000_000_000), people * 2)
    out = []
    for p in range(people):
        n1, n2 = str(numbers[2 * p]), str(numbers[2 * p + 1])
        name = f"{rnd.choice(FIRST)} {rnd.choice(LAST)}"
        out.append({"name": name, "numbers": [fmt_number(n1, rnd)], "emails": [f"p{p}@mail.com"] if p % 3 == 0 else []})
        out.append({"name": rnd.choice(["Dr. ", "", "mr "]) + name.lower(), "numbers": [fmt_number(n1, rnd), fmt_number(n2, rnd)]})
    rnd.shuffle(out)
    return out, people


print("Dictionary grouping (union-find on normalised numbers and e-mails)")
print(f"{'contacts':>9} {'people expected':>16} {'people found':>13} {'time s':>9}")
for n in (1000, 100_000):
    contacts, people = make_contacts(n)
    t0 = time.perf_counter(); merged = merge_contacts(contacts); el = time.perf_counter() - t0
    print(f"{n:>9} {people:>16} {len(merged):>13} {el:>9.4f}")
    assert len(merged) == people

print("\nPairwise comparison of every pair of contacts")
print(f"{'contacts':>9} {'pairs compared':>15} {'time s':>9} {'groups':>8} {'same people as dictionary':>26}")
last = None
for n in (1000, 2000, 4000):
    contacts, people = make_contacts(n)
    t0 = time.perf_counter(); g = merge_pairwise(contacts); el = time.perf_counter() - t0
    print(f"{n:>9} {n*(n-1)//2:>15,} {el:>9.3f} {len(g):>8} {str(len(g) == people):>26}")
    last = (n, el)
n, el = last
est = el * (100_000 / n) ** 2
print(f"\nExtrapolation for 100,000 contacts (time grows with n^2): about {est:,.0f} s = {est/60:,.0f} minutes ({100000*99999//2:,} pairs)")

contacts, _ = make_contacts(100_000)
import tracemalloc
tracemalloc.start(); merge_contacts(contacts); _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
print(f"peak extra memory of the dictionary method for 100,000 contacts: {peak/1024/1024:.1f} MiB (O(n))")
