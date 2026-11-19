"""A2.2 - min-max and z-score normalisation of the PM2.5 of one station, with and without an extreme value."""
import os, sqlite3, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "TaskB1"))
from cleaning import min_max, z_score

con = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "TaskB1", "airquality.db"))
day = [v for (v,) in con.execute("SELECT pm25 FROM readings WHERE station_id='ADY' AND day='2026-10-05' ORDER BY hour")]
print("Adyar, 5 Oct 2026, 24 hourly PM2.5 (first 8):", day[:8])
for label, series in (("normal day", day), ("same day + one real smoke event of 480", day + [480.0])):
    mm, zs = min_max(series), z_score(series)
    print(f"\n{label}: n = {len(series)}")
    print(f"  raw value        :", [f"{v:g}" for v in series[:6]], "... last", f"{series[-1]:g}")
    print(f"  min-max (0 to 1) :", mm[:6], "... last", mm[-1])
    print(f"  z-score          :", zs[:6], "... last", zs[-1])
    print(f"  min-max: values of the ordinary hours lie between {min(mm[:24]):.3f} and {max(mm[:24]):.3f}")
