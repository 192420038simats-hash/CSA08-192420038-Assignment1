"""Q1 alternative: deque(maxlen=7) window, and readings stored in a dictionary keyed by date."""
import time, sys, datetime
from collections import deque
from rainfall import generate_readings, moving_average_naive, moving_average_running


def moving_average_deque(readings, w=7):
    """Window kept in deque(maxlen=w): the oldest value drops out automatically; sum is O(w) per step."""
    win, out = deque(maxlen=w), []
    for x in readings:
        win.append(x)
        if len(win) == w:
            out.append(sum(win) / w)
    return out


def moving_average_deque_running(readings, w=7):
    """deque + running sum: O(1) per step."""
    win, s, out = deque(maxlen=w), 0.0, []
    for x in readings:
        if len(win) == w:
            s -= win[0]
        win.append(x); s += x
        if len(win) == w:
            out.append(s / w)
    return out


def moving_average_dict(by_date, w=7):
    """Readings in {date: mm}; the window is found by date, so late days are handled by simply adding a key."""
    days = sorted(by_date)
    return [sum(by_date[d] for d in days[i:i + w]) / w for i in range(len(days) - w + 1)]


r = generate_readings(365000)
start = datetime.date(2026, 1, 1)
by_date = {start + datetime.timedelta(days=i): v for i, v in enumerate(r)}
ref = moving_average_naive(r)
print(f"{'method':<22}{'time s':>9}   extra memory                       same result?")
for name, fn, arg, mem in [
    ("slice + sum (naive)", moving_average_naive, r, "O(w) per window + result O(n)"),
    ("running sum (list)", moving_average_running, r, "O(1) + result O(n)"),
    ("deque(maxlen=7)", moving_average_deque, r, "O(w) window + result O(n)"),
    ("deque + running sum", moving_average_deque_running, r, "O(w) window + result O(n)"),
    ("dict keyed by date", moving_average_dict, by_date, "O(n) dict + sorted keys O(n)"),
]:
    t0 = time.perf_counter(); out = fn(arg); el = time.perf_counter() - t0
    ok = len(out) == len(ref) and max(abs(a - b) for a, b in zip(out, ref)) < 1e-6
    print(f"{name:<22}{el:>9.4f}   {mem:<34} {ok}")
print(f"\nsys.getsizeof: list of 365,000 floats {sys.getsizeof(r):,} bytes (pointers only); dict of 365,000 dates {sys.getsizeof(by_date):,} bytes (table only)")
