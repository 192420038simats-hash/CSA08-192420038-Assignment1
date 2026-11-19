"""A2 alternative: dropping missing readings versus forward fill versus median fill.
Experiment with a KNOWN truth: take complete hourly data, delete some values (in runs of 1-4 hours), fill, and compare the
daily means with the true daily means."""
import os, random, statistics, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "TaskB1"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
from cleaning import fill_missing
import synth


def punch_holes(rows, fraction, rnd, evening=False):
    """Set about `fraction` of the pm25 values to None, in runs of 1-4 consecutive hours.
    evening=True: the gaps start only in the evening peak (hours 18-20) - the data are NOT missing at random."""
    out = [dict(r) for r in rows]; target, n = int(len(rows) * fraction), 0
    starts = [i for i, r in enumerate(out) if r["hour"] in (18, 19, 20)] if evening else range(len(out))
    starts = list(starts)
    while n < target and (n < len(starts) * 2 or not evening):
        start = rnd.choice(starts); run = rnd.randint(1, 4)
        for j in range(start, min(start + run, len(out))):
            if out[j]["pm25"] is not None: out[j]["pm25"] = None; n += 1
    return out


def daily_means(rows):
    d = {}
    for r in rows:
        if r["pm25"] is not None: d.setdefault(r["day"], []).append(r["pm25"])
    return {k: statistics.fmean(v) for k, v in d.items()}


base = [dict(zip(("sid", "day", "hour", "pm25", "pm10", "no2", "temp_c"), r)) for r in synth.rows(1, days=180)]
for r in base:
    if r["pm25"] is None: r["pm25"] = 60.0                       # make the truth complete
truth = daily_means(base)
rnd = random.Random(3)
print(f"{'pattern':<14}{'missing':>8} {'strategy':>8} | {'mean abs error of daily means (ug/m3)':>38} {'bias':>7}")
for label, evening in (("random gaps", False), ("evening gaps", True)):
    for frac in (0.05, 0.15) if evening else (0.05, 0.15, 0.30):
        holey = punch_holes(base, frac, rnd, evening)
        for strat in ("drop", "ffill", "median"):
            filled = fill_missing(holey, strat)
            est = daily_means(filled)
            errs = [est[d] - truth[d] for d in truth if d in est]
            print(f"{label:<14}{frac:>8.0%} {strat:>8} | {statistics.fmean(abs(e) for e in errs):>38.2f} {statistics.fmean(errs):>+7.2f}")

print("\nTime for 4 columns (rows are dictionaries) and extra memory for the filled copy")
print(f"{'rows':>9} {'drop s':>9} {'ffill s':>9} {'median s':>9}")
for n in (10_000, 100_000, 400_000):
    big = [dict(zip(("sid", "day", "hour", "pm25", "pm10", "no2", "temp_c"), r)) for r in synth.rows(max(1, n // 8760), days=365)][:n]
    t = []
    for strat in ("drop", "ffill", "median"):
        t0 = time.perf_counter(); fill_missing(big, strat); t.append(time.perf_counter() - t0)
    print(f"{n:>9,} {t[0]:>9.3f} {t[1]:>9.3f} {t[2]:>9.3f}")
