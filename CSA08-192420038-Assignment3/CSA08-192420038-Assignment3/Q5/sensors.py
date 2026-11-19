"""Q5 - Cold-storage temperature monitor: loop, comprehension, map/filter, enumerate, other comprehensions."""
import random

LOW_ERR, HIGH_ERR = -50, 50          # readings outside this range are sensor errors
SAFE_LOW, SAFE_HIGH = 2, 8           # vaccine storage range (deg C)


def generate(n, seed=5, error_rate=0.02):
    rnd = random.Random(seed)
    return [rnd.choice([99.9, -99.9]) if rnd.random() < error_rate else round(rnd.gauss(5, 2.2), 1) for _ in range(n)]


# ---------- version 1: for loop with append ----------
def clean_loop(readings):
    celsius, fahrenheit, alarms = [], [], []
    for minute, c in enumerate(readings):
        if LOW_ERR <= c <= HIGH_ERR:
            celsius.append(c)
            fahrenheit.append(round(c * 9 / 5 + 32, 2))
            if not (SAFE_LOW <= c <= SAFE_HIGH):
                alarms.append(minute)
    return celsius, fahrenheit, alarms


# ---------- version 2: list comprehensions ----------
def clean_comprehension(readings):
    celsius = [c for c in readings if LOW_ERR <= c <= HIGH_ERR]
    fahrenheit = [round(c * 9 / 5 + 32, 2) for c in readings if LOW_ERR <= c <= HIGH_ERR]
    alarms = [m for m, c in enumerate(readings) if LOW_ERR <= c <= HIGH_ERR and not (SAFE_LOW <= c <= SAFE_HIGH)]
    return celsius, fahrenheit, alarms


# ---------- version 3: map() and filter() with lambda ----------
def clean_map_filter(readings):
    valid = lambda c: LOW_ERR <= c <= HIGH_ERR
    celsius = list(filter(valid, readings))
    fahrenheit = list(map(lambda c: round(c * 9 / 5 + 32, 2), celsius))
    alarms = [m for m, c in filter(lambda p: valid(p[1]) and not (SAFE_LOW <= p[1] <= SAFE_HIGH), enumerate(readings))]
    return celsius, fahrenheit, alarms


if __name__ == "__main__":
    sample = [4.5, 99.9, 6.1, -99.9, 1.2, 8.0, 9.4, 2.0, 5.5]
    print("sample readings:", sample)
    for name, fn in [("loop", clean_loop), ("comprehension", clean_comprehension), ("map/filter", clean_map_filter)]:
        c, f, a = fn(sample)
        print(f"{name:<14} celsius {c}\n{'':<14} fahrenheit {f}\n{'':<14} alarm minutes {a}")
    assert clean_loop(sample) == clean_comprehension(sample) == clean_map_filter(sample)
    print("\nall three versions identical on the sample: True")

    print("\nGeneral form: [expression for item in iterable if condition]")
    print("  e.g. [round(c*9/5+32, 2) for c in readings if -50 <= c <= 50]")
    c = clean_comprehension(sample)[0]
    print("\ndictionary comprehension (minute -> valid reading):", {m: t for m, t in enumerate(sample) if LOW_ERR <= t <= HIGH_ERR})
    print("set comprehension (distinct whole-degree values)  :", {round(t) for t in c})
    gen = (t for t in sample if LOW_ERR <= t <= HIGH_ERR)
    print("generator expression object                       :", gen)
    print("sum of valid readings from the generator          :", sum(gen))
    print("second pass over the same generator               :", sum(gen), "(a generator can be used only once)")

    print("\nEdge cases")
    allvalid = [4.0, 5.0, 6.0]
    allbad = [99.9, -99.9, 75.0]
    for label, data in [("all valid", allvalid), ("all invalid", allbad), ("empty", [])]:
        r = (clean_loop(data), clean_comprehension(data), clean_map_filter(data))
        print(f"  {label:<12}: {r[0]}  identical: {r[0] == r[1] == r[2]}")
