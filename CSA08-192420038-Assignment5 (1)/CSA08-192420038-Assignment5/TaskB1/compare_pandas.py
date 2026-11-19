"""B1 alternative: cleaning with the csv module + loops versus pandas (vectorised). 1,000 / 100,000 / 1,000,000 rows.
Each measurement runs in its own process so that memory can be read from the operating system (peak resident memory)."""
import os, random, resource, subprocess, sys, tempfile, time
from datetime import date, timedelta
HERE = os.path.dirname(os.path.abspath(__file__))


def make_raw(path, n, seed=5):
    rnd = random.Random(seed)
    with open(path, "w", newline="") as f:
        f.write("date,hour,pm25,pm10,no2,temp\n")
        for i in range(n):
            day, hour = divmod(i, 24)
            d = (date(2000, 1, 1) + timedelta(days=day)).isoformat()
            vals = []
            for base, sd in ((60, 15), (100, 25), (35, 8), (80, 4)):          # temp in Fahrenheit
                r = rnd.random()
                vals.append("" if r < .02 else "NA" if r < .035 else str(-round(rnd.uniform(1, 30), 1)) if r < .04 else "9999" if r < .045 else str(round(rnd.gauss(base, sd), 1)))
            f.write(f"{d},{hour},{','.join(vals)}\n")
            if rnd.random() < 0.003: f.write(f"{d},{hour},{','.join(vals)}\n")      # duplicate row


def run_csv(path):
    sys.path.insert(0, os.path.join(HERE))
    from cleaning import clean_text, fill_missing
    rows = clean_text(open(path, encoding="utf-8").read(), fahrenheit=True)
    rows = fill_missing(rows, "ffill")
    v = [r["pm25"] for r in rows if r["pm25"] is not None]
    return len(rows), len(v), sum(v) / len(v)


def run_pandas(path):
    import numpy as np, pandas as pd
    df = pd.read_csv(path, dtype=str)
    df["hour"] = pd.to_numeric(df["hour"], errors="coerce")
    df = df[(df.hour >= 0) & (df.hour <= 23)].drop_duplicates(["date", "hour"]).copy()
    for c in ("pm25", "pm10", "no2", "temp"):
        df[c] = pd.to_numeric(df[c].str.strip(), errors="coerce")
    for c in ("pm25", "pm10", "no2"):
        df.loc[(df[c] < 0) | (df[c] > 999), c] = np.nan
    df["temp"] = ((df["temp"] - 32) * 5 / 9).round(1)
    df.loc[(df["temp"] < -10) | (df["temp"] > 55), "temp"] = np.nan
    df = df.sort_values(["date", "hour"])
    for c in ("pm25", "pm10", "no2", "temp"):
        df[c] = df[c].ffill(limit=3)
    v = df["pm25"].dropna()
    return len(df), len(v), float(v.mean())


if __name__ == "__main__":
    if len(sys.argv) == 4:                                   # child process: method, file, baseline
        method, path = sys.argv[1], sys.argv[2]
        if method == "pandas": import pandas, numpy               # import cost is not counted as data memory
        base = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        t0 = time.perf_counter(); res = (run_csv if method == "csv" else run_pandas)(path); el = time.perf_counter() - t0
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print(f"{el:.4f} {(peak - base) / 1024:.1f} {res[0]} {res[1]} {res[2]:.6f}")
        sys.exit()
    tmp = tempfile.mkdtemp()
    print(f"{'rows':>10} | {'csv loops: time':>16} {'extra RAM':>10} | {'pandas: time':>13} {'extra RAM':>10} | {'speed-up':>8} | rows kept / valid pm25 / mean pm25 equal?")
    for n in (1_000, 100_000, 1_000_000):
        path = os.path.join(tmp, f"raw{n}.csv"); make_raw(path, n)
        out = {}
        for m in ("csv", "pandas"):
            out[m] = subprocess.run([sys.executable, __file__, m, path, "x"], capture_output=True, text=True).stdout.split()
        a, b = out["csv"], out["pandas"]
        same = a[2:4] == b[2:4] and abs(float(a[4]) - float(b[4])) < 1e-6
        print(f"{n:>10,} | {float(a[0]):>14.3f} s {float(a[1]):>7.1f} MB | {float(b[0]):>11.3f} s {float(b[1]):>7.1f} MB | {float(a[0]) / float(b[0]):>7.1f}x | {a[2]} / {a[3]} / {float(a[4]):.3f} -> {same}")
