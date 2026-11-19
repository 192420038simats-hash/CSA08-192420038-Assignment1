"""Q1 - Daily rainfall records: weekly totals, wettest/driest week, 7-day moving average, dry days."""
import random

WINDOW = 7


def generate_readings(n, seed=1):
    """n daily rainfall readings in mm (about 45 % dry days)."""
    rnd = random.Random(seed)
    return [0.0 if rnd.random() < 0.45 else round(rnd.expovariate(1 / 8), 1) for _ in range(n)]


def weekly_totals(readings):
    """Totals of each complete 7-day week, using slicing."""
    return [round(sum(readings[i:i + 7]), 1) for i in range(0, len(readings) - 6, 7)]


def max_min_with_position(values):
    """Return ((max, index), (min, index)); index of the first occurrence. Empty list -> None."""
    if not values:
        return None
    hi, lo = max(values), min(values)
    return (hi, values.index(hi)), (lo, values.index(lo))


def moving_average_naive(readings, w=WINDOW):
    """Add the w values of every window again: (n-w+1)*(w-1) additions."""
    return [sum(readings[i:i + w]) / w for i in range(len(readings) - w + 1)]


def moving_average_running(readings, w=WINDOW):
    """Running sum: w-1 additions for the first window, then 1 addition and 1 subtraction per slide."""
    if len(readings) < w:
        return []
    s = sum(readings[:w])
    out = [s / w]
    for i in range(w, len(readings)):
        s += readings[i] - readings[i - w]
        out.append(s / w)
    return out


def dry_days(readings):
    """Day numbers (1-based) with 0 mm."""
    return [day for day, mm in enumerate(readings, start=1) if mm == 0]


def count_additions_naive(n, w=WINDOW):
    return max(0, n - w + 1) * (w - 1)


def count_additions_running(n, w=WINDOW):
    return 0 if n < w else (w - 1) + (n - w)       # plus (n - w) subtractions


if __name__ == "__main__":
    r = generate_readings(365)
    print("readings:", len(r), "first 10:", r[:10])
    wk = weekly_totals(r)
    print("complete weeks:", len(wk), "(365 = 52 x 7 + 1, the last single day is not a full week)")
    (hi, hi_i), (lo, lo_i) = max_min_with_position(wk)
    print(f"wettest week: week {hi_i + 1} = {hi} mm   driest week: week {lo_i + 1} = {lo} mm")
    (dhi, dhi_i), (dlo, dlo_i) = max_min_with_position(r)
    print(f"wettest day: day {dhi_i + 1} = {dhi} mm   driest day (first): day {dlo_i + 1} = {dlo} mm")
    ma = moving_average_running(r)
    print("moving averages:", len(ma), "first 3:", [round(x, 2) for x in ma[:3]])
    dd = dry_days(r)
    print("dry days:", len(dd), "first 15:", dd[:15])
    print("\nSlices of the list [10, 20, ..., 150] (15 values):")
    demo = list(range(10, 160, 10))
    print("  readings[7:14] ->", demo[7:14], "  (items at index 7..13, 14 excluded)")
    print("  readings[-7:]  ->", demo[-7:], "  (the last 7 items)")
    print("  readings[::7]  ->", demo[::7], "  (every 7th item from index 0)")
