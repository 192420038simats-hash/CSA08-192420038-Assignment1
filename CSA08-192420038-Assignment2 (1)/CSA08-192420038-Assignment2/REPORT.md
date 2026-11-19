# Python Programming – Assignment 2 (CO2) – Report

**Course:** CSA0806 Python Programming  **Name:** Dhatri  **Register number:** 192420038
**Python:** 3.12.3  **Libraries:** standard library only  **Submission date:** 30/10/2026
**GitHub repository:** https://github.com/<your-username>/CSA08-192420038-Assignment2

All programs were executed and the console output stored in each task folder. Function-call counts are machine-independent; times were measured on one machine and will differ on yours (re-run and replace them). Add your own screenshots.

### Q1 – Decisions with Many Boundaries (K4)

**Predictions (made before running).** 100 and 101 units, 200 and 201 units were each tested with and without a ration card / member above 80. Predicted: ≤100 → full subsidy; 101–200 → partial only with card; >200 → special subsidy only with an 80+ member, otherwise none.

**Why separate `if`s give more than one result.** Each `if` is evaluated independently, so several conditions can be true for the same household; in `if-elif-else` the chain stops at the first true branch, so exactly one result is possible. The faulty version forgot the lower bound `101 <=` on the second slab, so a 50-unit household with a ration card receives both a full and a partial subsidy (marked `<-- DOUBLE` in the output).

**Observed.** All 9 cases match the predictions in `if-elif-else`, table lookup and `match-case`; only the separate-`if` version produces two results.

**Design decision.** I chose `if-elif-else` with combined Boolean conditions (a conditional expression for the ration card / 80+ member) over nested `if`s: the three slabs sit at one indentation level, a slab limit is changed in one place, and no household can fall into two branches.

**Alternative concept and complexity.**

| Approach | Time per decision (k slabs) | Space | Measured, k = 3 |
|---|---|---|---|
| if-elif-else | O(k) | O(1) | 0.062 µs |
| match-case with guards | O(k) | O(1) | 0.066 µs |
| list of (limit, decision) pairs scanned in a loop | O(k) | O(k) | 0.116 µs |
| same table searched with `bisect` | O(log k) | O(k) | see scaling table |

The scaling table in the output shows the worst-case scan growing linearly (0.40 µs at k = 10 to 271.5 µs at k = 10,000) while `bisect` stays near 0.1 µs. For three slabs `if-elif-else` is clearest and fastest; for many slabs a table is easier to change and `bisect` is faster.

#### Source code (`Q1/q1.py`)

```python
"""Q1 - State electricity subsidy eligibility (K4 Analyse)."""
import timeit
from bisect import bisect_left


def separate_ifs(units, ration, senior):
    """Faulty developer version: independent if statements (no lower bound on slab 2)."""
    result = []
    if units <= 100:
        result.append("full subsidy")
    if units <= 200 and ration:            # BUG: missing 101 <= units
        result.append("partial subsidy")
    if units > 200 and senior:
        result.append("special subsidy (80+ member)")
    return result or ["no subsidy"]


def chained(units, ration, senior):
    """Correct version: exactly one branch can run."""
    if units <= 100:
        return "full subsidy"
    elif 101 <= units <= 200:
        return "partial subsidy" if ration else "no subsidy"
    else:
        return "special subsidy (80+ member)" if senior else "no subsidy"


SLABS = [(100, "full subsidy"), (200, "slab-2"), (float("inf"), "slab-3")]


def table_lookup(units, ration, senior):
    for limit, name in SLABS:
        if units <= limit:
            if name == "slab-2":
                return "partial subsidy" if ration else "no subsidy"
            if name == "slab-3":
                return "special subsidy (80+ member)" if senior else "no subsidy"
            return name


def match_version(units, ration, senior):
    match units:
        case u if u <= 100:
            return "full subsidy"
        case u if u <= 200:
            return "partial subsidy" if ration else "no subsidy"
        case _:
            return "special subsidy (80+ member)" if senior else "no subsidy"


CASES = [  # (units, ration card, member above 80, predicted decision)
    (50, False, False, "full subsidy"),
    (100, False, False, "full subsidy"),
    (101, True, False, "partial subsidy"),
    (101, False, False, "no subsidy"),
    (200, True, False, "partial subsidy"),
    (200, False, False, "no subsidy"),
    (201, False, True, "special subsidy (80+ member)"),
    (201, False, False, "no subsidy"),
    (50, True, False, "full subsidy"),   # extra case that exposes the bug
]

if __name__ == "__main__":
    print(f"{'Units':>5} {'Card':>5} {'80+':>5} | {'Separate ifs':<45} | {'if-elif-else':<30} | Predicted? ")
    print("-" * 115)
    for u, r, s, pred in CASES:
        a, b = separate_ifs(u, r, s), chained(u, r, s)
        flag = " <-- DOUBLE" if len(a) > 1 else ""
        ok = "OK" if b == pred == table_lookup(u, r, s) == match_version(u, r, s) else "MISMATCH"
        print(f"{u:>5} {str(r):>5} {str(s):>5} | {str(a):<45} | {b:<30} | {ok}{flag}")

    print("\nTime per decision (microseconds, 200,000 calls each, k = 3 slabs):")
    for f in (chained, table_lookup, match_version):
        t = timeit.timeit(lambda: [f(u, True, False) for u in (50, 150, 250)], number=200_000 // 3)
        print(f"  {f.__name__:<14} {t / 200_000 * 1e6:8.3f} us")

    print("\nScaling with k slabs (list scan O(k) vs bisect O(log k)), worst-case query:")
    for k in (10, 100, 1000, 10000):
        limits = list(range(100, 100 * k + 1, 100))
        q = limits[-1]
        scan = timeit.timeit(lambda: next(i for i, L in enumerate(limits) if q <= L), number=2000)
        bis = timeit.timeit(lambda: bisect_left(limits, q), number=2000)
        print(f"  k={k:>6}: scan {scan / 2000 * 1e6:10.3f} us   bisect {bis / 2000 * 1e6:8.3f} us")
```

#### Console output (`Q1/output.txt`)

```
Units  Card   80+ | Separate ifs                                  | if-elif-else                   | Predicted? 
-------------------------------------------------------------------------------------------------------------------
   50 False False | ['full subsidy']                              | full subsidy                   | OK
  100 False False | ['full subsidy']                              | full subsidy                   | OK
  101  True False | ['partial subsidy']                           | partial subsidy                | OK
  101 False False | ['no subsidy']                                | no subsidy                     | OK
  200  True False | ['partial subsidy']                           | partial subsidy                | OK
  200 False False | ['no subsidy']                                | no subsidy                     | OK
  201 False  True | ['special subsidy (80+ member)']              | special subsidy (80+ member)   | OK
  201 False False | ['no subsidy']                                | no subsidy                     | OK
   50  True False | ['full subsidy', 'partial subsidy']           | full subsidy                   | OK <-- DOUBLE

Time per decision (microseconds, 200,000 calls each, k = 3 slabs):
  chained           0.062 us
  table_lookup      0.116 us
  match_version     0.066 us

Scaling with k slabs (list scan O(k) vs bisect O(log k)), worst-case query:
  k=    10: scan      0.397 us   bisect    0.052 us
  k=   100: scan      2.387 us   bisect    0.076 us
  k=  1000: scan     26.851 us   bisect    0.098 us
  k= 10000: scan    271.512 us   bisect    0.106 us
```

---

### Q2 – Loops that Count Attempts (K3)

**Design.** `while attempts < limit` is the natural loop because blank entries must not be counted and the limit can change. The counter is incremented only *after* the blank check. `continue` skips blank entries, `break`/`return` leaves on success, the loop `else` runs only when no success occurred and locks the account for 30 minutes, and `pass` is the placeholder for the SMS alert in the `for range(3)` version (which needs an inner `while` to re-ask blank entries).

**When `while` is more natural, and the counter bug.** The number of *counted* attempts is not the number of loop passes, so a `while` loop is more natural. If `attempts += 1` is placed before the blank check, blank entries consume attempts (demonstrated: `LOCKED after 3 entries (blanks wrongly counted)` where the correct version verifies on attempt 2).

**Changed condition.** A correct security answer raises `limit` from 3 to 5 once; the `while` design adopts this with one line, whereas `range(3)` is fixed at creation. Observed: 4 wrong + correct code → locked with limit 3, verified on attempt 5 with limit 5.

**Alternative: recursion.** `verify_recursive` calls itself for the next attempt. Time is O(a) for all versions; stack space is O(a) for recursion (one frame per attempt) versus O(1) for the loops.

#### Source code (`Q2/q2.py`)

```python
"""Q2 - OTP attempt loops (K3 Apply)."""
CORRECT = "482913"


def verify_while(entries, security_ok=False):
    """while version. Blank entries are skipped (continue) and not counted.
    A correct security answer raises the limit from 3 to 5 (changed condition)."""
    entries = iter(entries)
    limit = 5 if security_ok else 3
    attempts = 0
    while attempts < limit:
        code = next(entries, None)
        if code is None:                   # keypad timed out: stop asking
            break
        code = code.strip()
        if code == "":
            continue                       # blank: NOT an attempt
        attempts += 1                      # counted only after the blank check
        if code == CORRECT:
            return f"VERIFIED on attempt {attempts}"
        print(f"   wrong OTP ({attempts}/{limit})")
    else:
        return "ACCOUNT LOCKED for 30 minutes"   # loop-else: ran out of attempts
    return "SESSION ENDED (no input)"


def verify_for(entries):
    """for range(3) version; blank entries need an inner while to be re-asked."""
    entries = iter(entries)
    for attempt in range(1, 4):
        code = ""
        while code == "":
            code = next(entries, "?").strip()
        if code == CORRECT:
            return f"VERIFIED on attempt {attempt}"
        if attempt == 3:
            pass                           # placeholder: SMS alert would be sent here
        print(f"   wrong OTP ({attempt}/3)")
    else:
        return "ACCOUNT LOCKED for 30 minutes"


def verify_recursive(entries, attempt=1, limit=3):
    """Recursive alternative: O(a) stack frames."""
    if attempt > limit:
        return "ACCOUNT LOCKED for 30 minutes"
    code = next(entries, "?").strip()
    if code == "":
        return verify_recursive(entries, attempt, limit)
    if code == CORRECT:
        return f"VERIFIED on attempt {attempt}"
    print(f"   wrong OTP ({attempt}/{limit})")
    return verify_recursive(entries, attempt + 1, limit)


def verify_counter_bug(entries):
    """Demonstrates the wrong counter placement: blanks consume attempts."""
    attempts = 0
    for code in entries:
        attempts += 1                      # BUG: incremented before blank check
        if code.strip() == "":
            continue
        if code.strip() == CORRECT:
            return f"VERIFIED on attempt {attempts}"
        if attempts == 3:
            break
    return f"LOCKED after {attempts} entries (blanks wrongly counted)"


if __name__ == "__main__":
    scenarios = {
        "correct on 2nd try": ["111111", CORRECT],
        "blank entries ignored": ["", "  ", "000000", CORRECT],
        "three wrong -> lock": ["1", "2", "3", CORRECT],
    }
    for name, data in scenarios.items():
        print(f"\nScenario: {name}")
        print("  while    :", verify_while(list(data)))
        print("  for      :", verify_for(list(data)))
        print("  recursive:", verify_recursive(iter(data)))

    print("\nChanged condition (security answer correct -> 5 attempts):")
    data = ["1", "2", "3", "4", CORRECT]
    print("  limit 3:", verify_while(list(data)))
    print("  limit 5:", verify_while(list(data), security_ok=True))

    print("\nWrong counter placement demo (blank, blank, wrong, correct):")
    print("  buggy  :", verify_counter_bug(["", "", "9", CORRECT]))
    print("  correct:", verify_while(["", "", "9", CORRECT]))
```

#### Console output (`Q2/output.txt`)

```

Scenario: correct on 2nd try
   wrong OTP (1/3)
  while    : VERIFIED on attempt 2
   wrong OTP (1/3)
  for      : VERIFIED on attempt 2
   wrong OTP (1/3)
  recursive: VERIFIED on attempt 2

Scenario: blank entries ignored
   wrong OTP (1/3)
  while    : VERIFIED on attempt 2
   wrong OTP (1/3)
  for      : VERIFIED on attempt 2
   wrong OTP (1/3)
  recursive: VERIFIED on attempt 2

Scenario: three wrong -> lock
   wrong OTP (1/3)
   wrong OTP (2/3)
   wrong OTP (3/3)
  while    : ACCOUNT LOCKED for 30 minutes
   wrong OTP (1/3)
   wrong OTP (2/3)
   wrong OTP (3/3)
  for      : ACCOUNT LOCKED for 30 minutes
   wrong OTP (1/3)
   wrong OTP (2/3)
   wrong OTP (3/3)
  recursive: ACCOUNT LOCKED for 30 minutes

Changed condition (security answer correct -> 5 attempts):
   wrong OTP (1/3)
   wrong OTP (2/3)
   wrong OTP (3/3)
  limit 3: ACCOUNT LOCKED for 30 minutes
   wrong OTP (1/5)
   wrong OTP (2/5)
   wrong OTP (3/5)
   wrong OTP (4/5)
  limit 5: VERIFIED on attempt 5

Wrong counter placement demo (blank, blank, wrong, correct):
  buggy  : LOCKED after 3 entries (blanks wrongly counted)
   wrong OTP (1/3)
  correct: VERIFIED on attempt 2
```

---

### Q3 – Vehicle Registration Number Validator (K4)

**Predictions.** `tn 09 ab 1234`, `KA-01-M-0007`, `Tn09Ab1234` → valid; `TN9AB1234` (district has one digit), `TN 22 1234 AB` (digits before letters), `TN-09-ABC-1234` (3-letter series) → rejected. All six observed results match.

**Immutability.** A `str` cannot be modified after creation (`text[0] = 'T'` raises `TypeError`), so every string method returns a new string; `text.upper()` therefore leaves `text` unchanged unless the result is assigned. Immutability makes strings hashable and safe to share.

**Slices.** `s[-4:]` is the last four characters (the serial number) for 9- and 10-character plates; `s[4:-4]` is the series: one character for a 9-character plate (`'A'`) and two for a 10-character plate (`'AB'`).

**Alternative: regular expression.** `re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", reg)` agrees with the slicing version on all six inputs. Both are O(L) time and O(1) extra space. The pattern is shorter and is itself the specification (easier to change), while slicing is easier to step through; note `isalpha()`/`isdigit()` also accept some non-ASCII characters, whereas the regex classes do not.

#### Source code (`Q3/q3.py`)

```python
"""Q3 - Vehicle registration number validator (K4 Analyse). No regular expressions."""


def normalise(text):
    """'tn 09 ab 1234' -> 'TN09AB1234' (spaces and hyphens removed, upper case)."""
    return text.replace(" ", "").replace("-", "").upper()


def is_valid(reg):
    """Valid form: 2 letters, 2 digits, 1 or 2 letters, 4 digits (e.g. TN09AB1234)."""
    if len(reg) not in (9, 10):
        return False
    series_len = len(reg) - 8                      # 1 or 2 letters
    state = reg[:2]
    district = reg[2:4]
    series = reg[4:4 + series_len]
    number = reg[-4:]
    return (state.isalpha() and district.isdigit()
            and series.isalpha() and number.isdigit())


def format_reg(reg):
    """Receipt format, e.g. 'TN 09 AB 1234' (valid numbers only)."""
    return " ".join([reg[:2], reg[2:4], reg[4:-4], reg[-4:]])


if __name__ == "__main__":
    print("--- Assignment program ---")
    for raw in ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]:
        reg = normalise(raw)
        print(f"{raw:15} -> {reg:11} {'valid' if is_valid(reg) else 'INVALID'}")

    print("\n--- Six designed inputs: prediction vs observed + receipt format ---")
    tests = [("tn 09 ab 1234", True), ("KA-01-M-0007", True), ("Tn09Ab1234", True),
             ("TN9AB1234", False), ("TN 22 1234 AB", False), ("TN-09-ABC-1234", False)]
    for raw, expected in tests:
        reg = normalise(raw)
        got = is_valid(reg)
        receipt = format_reg(reg) if got else "-"
        print(f"{raw:16} -> {reg:12} predicted={str(expected):5} observed={str(got):5} "
              f"{'PASS' if got == expected else 'FAIL'}  receipt: {receipt}")

    print("\n--- Slicing inquiry ---")
    for s in ("TN09A1234", "TN09AB1234"):
        print(f"len={len(s):2} s={s}  s[-4:]={s[-4:]!r}  s[4:-4]={s[4:-4]!r}")

    print("\n--- Immutability ---")
    text = "tn 09"
    result = text.upper()
    print(f"text={text!r}  text.upper()={result!r}  text after call={text!r}")
    try:
        text[0] = "T"
    except TypeError as e:
        print("text[0] = 'T' ->", type(e).__name__ + ":", e)

    print("\n--- Alternative: regular expression ---")
    import re
    pattern = r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}"
    agree = all((re.fullmatch(pattern, normalise(r)) is not None) == is_valid(normalise(r))
                for r, _ in tests)
    print("regex and slicing agree on all six inputs:", agree)
```

#### Console output (`Q3/output.txt`)

```
--- Assignment program ---
tn 09 ab 1234   -> TN09AB1234  valid
KA-01-M-0007    -> KA01M0007   valid
TN9AB1234       -> TN9AB1234   INVALID
TN 22 1234 AB   -> TN221234AB  INVALID

--- Six designed inputs: prediction vs observed + receipt format ---
tn 09 ab 1234    -> TN09AB1234   predicted=True  observed=True  PASS  receipt: TN 09 AB 1234
KA-01-M-0007     -> KA01M0007    predicted=True  observed=True  PASS  receipt: KA 01 M 0007
Tn09Ab1234       -> TN09AB1234   predicted=True  observed=True  PASS  receipt: TN 09 AB 1234
TN9AB1234        -> TN9AB1234    predicted=False observed=False PASS  receipt: -
TN 22 1234 AB    -> TN221234AB   predicted=False observed=False PASS  receipt: -
TN-09-ABC-1234   -> TN09ABC1234  predicted=False observed=False PASS  receipt: -

--- Slicing inquiry ---
len= 9 s=TN09A1234  s[-4:]='1234'  s[4:-4]='A'
len=10 s=TN09AB1234  s[-4:]='1234'  s[4:-4]='AB'

--- Immutability ---
text='tn 09'  text.upper()='TN 09'  text after call='tn 09'
text[0] = 'T' -> TypeError: 'str' object does not support item assignment

--- Alternative: regular expression ---
regex and slicing agree on all six inputs: True
```

---

### Q4 – Building Long Text: `+` or `join()` (K4)

**Prediction.** `join()` fastest; `+=` slower and growing faster than linearly, because strings are immutable and each append conceptually copies the whole string.

**Results (average of 3 runs, this machine, Python 3.12.3).**

| Lines | (a) `+=` s | (b) `join` s | (c) f-string + join s | `StringIO` s | Same text |
|---|---|---|---|---|---|
| 1,000 | 0.00007 | 0.00001 | 0.00015 | 0.00005 | True |
| 10,000 | 0.00065 | 0.00008 | 0.00155 | 0.00052 | True |
| 200,000 | 0.01342 | 0.00315 | 0.03805 | 0.01201 | True |

Assignment program (200,000 lines): `+=` average 0.0109 s, `join` average 0.0038 s. Column (c) is slower because it also performs the formatting of every line (items are not pre-built).

**Explanation.** Because `str` is immutable, `text += p` must produce a new string. CPython has an optimisation: if the string has only one reference it is resized in place, so `+=` looks nearly linear in the first table. The second experiment defeats the optimisation by holding another reference (`alias = text`): time then roughly quadruples whenever n doubles (0.0048 s, 0.0176 s, 0.0699 s, 0.3162 s for 5,000, 10,000, 20,000, 40,000 lines), which is the O(n²) characters-copied behaviour. The optimisation is an implementation detail (absent in other Python implementations and fragile), so `join()` – one allocation and one copy per piece, O(n) always – remains the recommended practice.

**Alternative: file / `StringIO`.** Writing each line straight to a file needs O(1) extra memory and O(n) time; `StringIO` is O(n) time and O(n) memory. Peak memory for 200,000 lines: `+=` 2.91 MiB (in-place), `join` 5.82 MiB (parts list plus result), `StringIO` 6.54 MiB. `join` trades memory for guaranteed linear time.

#### Source code (`Q4/q4.py`)

```python
"""Q4 - Building long text: += versus join() (K4 Analyse)."""
import io
import sys
import time
import tracemalloc

items = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]


def build_plus(parts):
    text = ""
    for p in parts:
        text += p + ";"
    return text


def build_join(parts):
    return ";".join(parts) + ";"          # single str.join() call (TODO 1)


def build_fstring(n):
    """(c) an f-string per line, collected and joined."""
    return "".join([f"Item{i}:Rs{i % 50};" for i in range(n)])


def build_stringio(parts):
    buf = io.StringIO()
    for p in parts:
        buf.write(p + ";")
    return buf.getvalue()


def timed(fn, *args):
    start = time.perf_counter()
    out = fn(*args)
    return out, time.perf_counter() - start


if __name__ == "__main__":
    print("Python", sys.version.split()[0])
    a, t_plus = timed(build_plus, items)
    b, t_join = timed(build_join, items)
    print("same text:", a == b, "| length:", len(b))
    print(f"+= time: {t_plus:.4f} s   join time: {t_join:.4f} s")

    print("\nAverage of 3 runs (seconds) with the assignment program:")
    tp = [timed(build_plus, items)[1] for _ in range(3)]
    tj = [timed(build_join, items)[1] for _ in range(3)]
    print(f"  += runs: {[round(x, 4) for x in tp]} avg {sum(tp) / 3:.4f}")
    print(f"  join runs: {[round(x, 4) for x in tj]} avg {sum(tj) / 3:.4f}")

    print("\nThree implementations at three sizes (avg of 3 runs, seconds):")
    print(f"{'lines':>8} | {'(a) +=':>9} | {'(b) join':>9} | {'(c) f-string':>12} | {'StringIO':>9} | same")
    for n in (1_000, 10_000, 200_000):
        sub = items[:n]
        row, outs = [], []
        for fn, arg in ((build_plus, sub), (build_join, sub), (build_fstring, n), (build_stringio, sub)):
            ts = []
            for _ in range(3):
                out, t = timed(fn, arg)
                ts.append(t)
            row.append(sum(ts) / 3)
            outs.append(out)
        print(f"{n:>8} | {row[0]:9.5f} | {row[1]:9.5f} | {row[2]:12.5f} | {row[3]:9.5f} | {len(set(outs)) == 1}")

    print("\nWhy += can look fast: CPython optimisation (single reference -> in-place realloc).")
    print("Keeping a second reference to the string defeats it and forces a copy each time:")
    for n in (5_000, 10_000, 20_000, 40_000):
        sub = items[:n]
        text, start = "", time.perf_counter()
        for p in sub:
            alias = text                  # second reference -> in-place resize impossible
            text += p + ";"
        t = time.perf_counter() - start
        print(f"  n={n:>6}: {t:8.4f} s")

    print("\nPeak extra memory (MiB) building 200,000 lines:")
    for fn in (build_plus, build_join, build_stringio):
        tracemalloc.start()
        fn(items)
        peak = tracemalloc.get_traced_memory()[1] / 2**20
        tracemalloc.stop()
        print(f"  {fn.__name__:<14} {peak:8.2f} MiB")
```

#### Console output (`Q4/output.txt`)

```
Python 3.12.3
same text: True | length: 3048890
+= time: 0.0131 s   join time: 0.0070 s

Average of 3 runs (seconds) with the assignment program:
  += runs: [0.0122, 0.0102, 0.0102] avg 0.0109
  join runs: [0.0038, 0.0039, 0.0035] avg 0.0038

Three implementations at three sizes (avg of 3 runs, seconds):
   lines |    (a) += |  (b) join | (c) f-string |  StringIO | same
    1000 |   0.00007 |   0.00001 |      0.00015 |   0.00005 | True
   10000 |   0.00065 |   0.00008 |      0.00155 |   0.00052 | True
  200000 |   0.01342 |   0.00315 |      0.03805 |   0.01201 | True

Why += can look fast: CPython optimisation (single reference -> in-place realloc).
Keeping a second reference to the string defeats it and forces a copy each time:
  n=  5000:   0.0048 s
  n= 10000:   0.0176 s
  n= 20000:   0.0699 s
  n= 40000:   0.3162 s

Peak extra memory (MiB) building 200,000 lines:
  build_plus         2.91 MiB
  build_join         5.82 MiB
  build_stringio     6.54 MiB
```

---

### Q5 – Functions, Parameters and Scope (K4)

**Bug explained.** A default value is created once, when `def` is executed. `order=[]` is one list stored in the function object; each call without an argument appends to that same list. The output shows `add_item_buggy` returning the *same* list object twice (`True`) and `__defaults__` now holding `['Tea', 'Vada']`. (The assignment writes `.defaults`; the real attribute is `__defaults__`.)

**Fix.** Use `order=None` and create `[]` inside the function. Three customers in sequence produce three independent orders.

**Parameters.** Positional (`bill([20, 15, 30])`), keyword (`bill(prices=..., gst_rate=0.12)`), default (`gst_rate=0.05`); several values are returned as a tuple and unpacked (`total, gst = bill(...)`).

**Scope.** A name assigned inside a function is local (`local_demo` leaves the global at 0). Rebinding a global needs `global` (otherwise `UnboundLocalError`); `nonlocal` rebinds a variable of the enclosing function. Globals are avoided because any function can change them, which hides bugs and makes testing difficult.

**Alternatives.** Passing the list explicitly puts ownership with the caller; a closure (`make_order`) keeps one private list per customer. All designs are O(1) per item, and O(m) space per customer for m items (the closure adds one small function object).

#### Source code (`Q5/q5.py`)

```python
"""Q5 - Functions, parameters and scope (K4 Analyse)."""


def add_item_buggy(item, order=[]):
    order.append(item)
    return order


def add_item(item, order=None):
    if order is None:           # TODO 1: new list per call when none supplied
        order = []
    order.append(item)
    return order


def make_order():
    """Closure alternative: the list lives in the enclosing scope."""
    order = []

    def add(item):
        order.append(item)
        return list(order)
    return add


def bill(prices, gst_rate=0.05):
    """Returns two values (a tuple): total and GST."""
    total = sum(prices)
    return total, round(total * gst_rate, 2)


counter = 0


def local_demo():
    counter = 99               # new LOCAL name; global untouched
    return counter


def global_demo():
    global counter             # needed to rebind the global name
    counter += 1


def no_global_demo():
    try:
        counter += 1           # UnboundLocalError: assignment makes it local
    except UnboundLocalError as e:
        return f"UnboundLocalError: {e}"


def outer():
    n = 0

    def inner():
        nonlocal n             # rebinds the enclosing function's variable
        n += 1
    inner()
    inner()
    return n


if __name__ == "__main__":
    print(add_item_buggy("Tea"), add_item_buggy("Vada"))
    print(add_item("Tea"), add_item("Vada"))
    print("add_item_buggy.__defaults__ ->", add_item_buggy.__defaults__)
    print("add_item.__defaults__       ->", add_item.__defaults__)
    print("same list object returned twice:", add_item_buggy("X") is add_item_buggy("Y"))

    print("\nThree customers in sequence (independent orders):")
    for items in (["Tea", "Vada"], ["Coffee"], ["Idli", "Dosa", "Tea"]):
        order = None
        for it in items:
            order = add_item(it, order)
        print("  ", order)

    print("\nClosure alternative (one add() per customer):")
    c1, c2 = make_order(), make_order()
    c1("Tea"); c2("Coffee"); c1("Vada")
    print("  customer 1:", c1("Samosa"), "| customer 2:", c2("Bun"))

    print("\nParameter styles:")
    print("  positional :", bill([20, 15, 30]))
    print("  keyword    :", bill(prices=[20, 15, 30], gst_rate=0.12))
    total, gst = bill([20, 15, 30])
    print(f"  unpacked   : total={total} gst={gst}")

    print("\nScope demos:")
    print("  local_demo() ->", local_demo(), "| global counter =", counter)
    global_demo()
    print("  after global_demo() -> counter =", counter)
    print("  without global ->", no_global_demo())
    print("  nonlocal outer() ->", outer())
```

#### Console output (`Q5/output.txt`)

```
['Tea', 'Vada'] ['Tea', 'Vada']
['Tea'] ['Vada']
add_item_buggy.__defaults__ -> (['Tea', 'Vada'],)
add_item.__defaults__       -> (None,)
same list object returned twice: True

Three customers in sequence (independent orders):
   ['Tea', 'Vada']
   ['Coffee']
   ['Idli', 'Dosa', 'Tea']

Closure alternative (one add() per customer):
  customer 1: ['Tea', 'Vada', 'Samosa'] | customer 2: ['Coffee', 'Bun']

Parameter styles:
  positional : (65, 3.25)
  keyword    : (65, 7.8)
  unpacked   : total=65 gst=3.25

Scope demos:
  local_demo() -> 99 | global counter = 0
  after global_demo() -> counter = 1
  without global -> UnboundLocalError: cannot access local variable 'counter' where it is not associated with a value
  nonlocal outer() -> 2
```

---

### Q6 – Recursion and Its Limits (K5)

**Design.** Base case: `ways(n) = 1` for n ≤ 1. Recursive case: `ways(n) = ways(n-1) + ways(n-2)`. Hand check n = 1..6: 1, 2, 3, 5, 8, 13 – the program agrees. The printed call tree for n = 5 contains 15 calls; `w3` appears twice and `w2` three times, so the plain version repeats work.

**Growth investigation.** Prediction: naive calls = 2·ways(n) − 1 (grows by φ ≈ 1.618 per step); memoised calls = n + 1. Observed values match exactly: n = 10 → 177 / 11; n = 20 → 21,891 / 21; n = 25 → 242,785 / 26; n = 30 → 2,692,537 / 31.

**Deployment decision (n = 1,000).** `ways_memo(1000)` raises `RecursionError` because `sys.getrecursionlimit()` is 1000 and the recursion needs about 1000 nested frames plus those already in use. Raising the limit (5000) works here, but deep recursion can exhaust the C stack. **Decision: use the loop** (O(1) space, no limit, about 8× faster than the memoised version: 0.000034 s vs 0.000268 s for n = 1,000) and keep the memoised recursion only for explanation and verification. ways(1000) has 209 digits; Python integers do not overflow.

**Alternative: loop with two values.**

| Version | Time | Space | n = 1000 |
|---|---|---|---|
| Plain recursion | O(φⁿ) | O(n) stack | impractical (n = 30 already 0.145 s) |
| Memoised recursion | O(n) | O(n) cache + O(n) stack | needs raised limit, 0.000268 s |
| Loop, last two values | O(n) | O(1) | 0.000034 s |

#### Source code (`Q6/q6.py`)

```python
"""Q6 - Recursion and its limits (K5 Evaluate)."""
import sys
import time
from functools import lru_cache

calls = 0


def ways_naive(n):
    """Ways to climb n temple steps taking 1 or 2 steps at a time."""
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)


@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1
    if n <= 1:                           # TODO 1: same base/recursive case, calling ways_memo
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)


def ways_loop(n):
    a = b = 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def tree(n, depth=0):
    print("  " * depth + f"w{n}")
    if n > 1:
        tree(n - 1, depth + 1)
        tree(n - 2, depth + 1)


if __name__ == "__main__":
    print("Python", sys.version.split()[0])
    calls = 0; print("naive:", ways_naive(25), "calls =", calls)
    ways_memo.cache_clear()
    calls = 0; print("memo :", ways_memo(25), "calls =", calls)

    print("\nHand check n = 1..6 :", [ways_naive(n) for n in range(1, 7)], "(expected 1 2 3 5 8 13)")
    print("\nCall tree for n = 5:")
    tree(5)

    print("\nGrowth investigation (function calls):")
    print(f"{'n':>3} {'ways(n)':>10} {'naive calls':>12} {'2*ways-1':>10} {'memo calls':>11} {'n+1':>5}")
    for n in (10, 20, 25, 30):
        calls = 0; w = ways_naive(n); cn = calls
        ways_memo.cache_clear(); calls = 0; ways_memo(n); cm = calls
        print(f"{n:>3} {w:>10} {cn:>12} {2 * w - 1:>10} {cm:>11} {n + 1:>5}")

    print("\nDeployment decision, n = 1000:")
    print("sys.getrecursionlimit() =", sys.getrecursionlimit())
    ways_memo.cache_clear()
    try:
        ways_memo(1000)
    except RecursionError as e:
        print("RecursionError:", e)
    reference = ways_loop(1000)
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(5000)
    ways_memo.cache_clear()
    print("memo with limit 5000 equals loop result:", ways_memo(1000) == reference)
    sys.setrecursionlimit(old)
    print("digits in ways(1000):", len(str(reference)))

    print("\nTiming for n = 1000 (average of 200 runs, seconds):")
    t = time.perf_counter()
    for _ in range(200): ways_loop(1000)
    print(f"  loop : {(time.perf_counter() - t) / 200:.6f}")
    sys.setrecursionlimit(5000)
    t = time.perf_counter()
    for _ in range(200):
        ways_memo.cache_clear(); ways_memo(1000)
    print(f"  memo : {(time.perf_counter() - t) / 200:.6f}")
    t = time.perf_counter(); ways_naive(30)
    print(f"  naive n=30 (single run): {time.perf_counter() - t:.4f}")
```

#### Console output (`Q6/output.txt`)

```
Python 3.12.3
naive: 121393 calls = 242785
memo : 121393 calls = 26

Hand check n = 1..6 : [1, 2, 3, 5, 8, 13] (expected 1 2 3 5 8 13)

Call tree for n = 5:
w5
  w4
    w3
      w2
        w1
        w0
      w1
    w2
      w1
      w0
  w3
    w2
      w1
      w0
    w1

Growth investigation (function calls):
  n    ways(n)  naive calls   2*ways-1  memo calls   n+1
 10         89          177        177          11    11
 20      10946        21891      21891          21    21
 25     121393       242785     242785          26    26
 30    1346269      2692537    2692537          31    31

Deployment decision, n = 1000:
sys.getrecursionlimit() = 1000
RecursionError: maximum recursion depth exceeded
memo with limit 5000 equals loop result: True
digits in ways(1000): 209

Timing for n = 1000 (average of 200 runs, seconds):
  loop : 0.000034
  memo : 0.000268
  naive n=30 (single run): 0.1454
```

---

### Q7 – Diagnose, Redesign and Validate (K5)

**Selected program:** the plain recursive `ways_naive` from Q6.

**A. Diagnosis.** Calls grow from 177 (n = 10) to 2,692,537 (n = 30); every extra 5 steps multiplies the calls by 11.09 (= φ⁵), i.e. exponential growth. Only 31 distinct sub-problems exist for n = 30, so 2,692,506 calls (99.9988%) repeat earlier work. The count that grows is the number of calls; work per call is constant.

**B. Objective.** For n = 30 use no more than n + 1 = 31 operations, and make n = 1,000 run with the default recursion limit (1000) without `RecursionError`.

**C. Redesign.** Exploit overlapping sub-problems: `ways(n)` depends only on the previous two values, so compute bottom-up with two variables.

```
function ways(n):
    a ← 1; b ← 1
    repeat n − 1 times: (a, b) ← (b, a + b)
    return b
```
No extra memory beyond two integers (O(1)); trade-off: it no longer mirrors the definition and does not store earlier answers for repeated queries (a cache would).

**D. Prediction.** About 29 loop steps for n = 30 (over 90,000× fewer operations) and 999 steps for n = 1,000 without error.

**E. Validation (same inputs, `q7_raw_data.csv`).**

| n | Original calls | Redesign steps | Original time s | Redesign time s | Same answer |
|---|---|---|---|---|---|
| 10 | 177 | 9 | 0.00001 | 0.0000010 | True |
| 20 | 21,891 | 19 | 0.00119 | 0.0000009 | True |
| 25 | 242,785 | 24 | 0.01433 | 0.0000011 | True |
| 30 | 2,692,537 | 29 | 0.14889 | 0.0000019 | True |
| 1,000 | RecursionError | 999 | – | 0.0000456 | 209 digits |

**F. Defence.** Objective achieved: operations fell from 2,692,537 to 29 (about 92,000× fewer; about 78,000× faster at n = 30), growth became linear, memory O(1), and n = 1,000 works with the default limit. New costs: less direct correspondence to the mathematical definition, and repeated queries are recomputed. The original or memoised version may still be preferable for teaching the recurrence, for tiny n, or when many different n values are queried repeatedly and a cache answers them instantly.

#### Source code (`Q7/q7.py`)

```python
"""Q7 - Diagnose, redesign and validate: plain recursive ways_naive (K5 Evaluate)."""
import csv
import sys
import time

calls = 0


def ways_naive(n):                       # ORIGINAL
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)


def ways_loop(n):                        # REDESIGN: bottom-up, last two values only
    steps = 0
    a = b = 1
    for _ in range(n - 1):
        a, b = b, a + b
        steps += 1
    return b, steps


def seconds(fn, *args):
    t = time.perf_counter(); fn(*args); return time.perf_counter() - t


if __name__ == "__main__":
    print("A. DIAGNOSIS - growth of calls in the original")
    prev = None
    last = 0
    for n in (10, 15, 20, 25, 30):
        calls = 0; w = ways_naive(n)
        ratio = f"{calls / prev:.3f}" if prev else "-"
        print(f"  n={n:>2}  calls={calls:>9}  ratio vs previous row={ratio}")
        prev = last = calls
    distinct = 31
    print(f"  distinct sub-problems for n=30: {distinct}; repeated calls = {last - distinct} "
          f"({100 * (last - distinct) / last:.4f}%)")

    print("\nB. OBJECTIVE: n=30 -> <= 31 operations; n=1000 with default recursion limit "
          f"({sys.getrecursionlimit()}) and no RecursionError.")
    print("\nD. PREDICTION: ~29 loop steps for n=30 (>90,000x fewer); n=1000 -> 999 steps, no error.")

    print("\nE. VALIDATION - original vs redesign (same inputs)")
    print(f"{'n':>5} | {'orig calls':>11} | {'redesign steps':>14} | {'orig time s':>11} | {'new time s':>10} | same answer")
    out = []
    for n in (10, 20, 25, 30):
        calls = 0; w1 = ways_naive(n); c = calls
        to = seconds(ways_naive, n)
        w2, steps = ways_loop(n)
        tn = seconds(ways_loop, n)
        print(f"{n:>5} | {c:>11} | {steps:>14} | {to:11.5f} | {tn:10.7f} | {w1 == w2}")
        out.append((n, c, steps, round(to, 6), round(tn, 8), w1 == w2))
    w, steps = ways_loop(1000)
    try:
        ways_naive(1000); status = "finished"
    except RecursionError:
        status = "RecursionError"
    t1000 = seconds(ways_loop, 1000)
    print(f"{1000:>5} | {status:>11} | {steps:>14} | {'-':>11} | {t1000:10.7f} | digits={len(str(w))}")
    out.append((1000, status, steps, "", round(t1000, 8), True))

    with open("q7_raw_data.csv", "w", newline="") as f:
        csv.writer(f).writerows([("n", "original_calls", "redesign_steps", "orig_s", "new_s", "same")] + out)
    print("\nraw data written to q7_raw_data.csv")
```

#### Console output (`Q7/output.txt`)

```
A. DIAGNOSIS - growth of calls in the original
  n=10  calls=      177  ratio vs previous row=-
  n=15  calls=     1973  ratio vs previous row=11.147
  n=20  calls=    21891  ratio vs previous row=11.095
  n=25  calls=   242785  ratio vs previous row=11.091
  n=30  calls=  2692537  ratio vs previous row=11.090
  distinct sub-problems for n=30: 31; repeated calls = 2692506 (99.9988%)

B. OBJECTIVE: n=30 -> <= 31 operations; n=1000 with default recursion limit (1000) and no RecursionError.

D. PREDICTION: ~29 loop steps for n=30 (>90,000x fewer); n=1000 -> 999 steps, no error.

E. VALIDATION - original vs redesign (same inputs)
    n |  orig calls | redesign steps | orig time s | new time s | same answer
   10 |         177 |              9 |     0.00001 |  0.0000010 | True
   20 |       21891 |             19 |     0.00119 |  0.0000009 | True
   25 |      242785 |             24 |     0.01433 |  0.0000011 | True
   30 |     2692537 |             29 |     0.14889 |  0.0000019 | True
 1000 | RecursionError |            999 |           - |  0.0000456 | digits=209

raw data written to q7_raw_data.csv
```

---

## Marks map

| Q | Area | Marks |
|---|---|---|
| 1 | if / elif / else | 6 |
| 2 | loops, break, continue, pass, loop-else | 4 |
| 3 | string operations and slicing | 6 |
| 4 | string building, immutability | 6 |
| 5 | functions, parameters, scope | 7 |
| 6 | recursion, memoisation | 8 |
| 7 | diagnose, redesign, validate | 13 |
| | **Total** | **50** |
