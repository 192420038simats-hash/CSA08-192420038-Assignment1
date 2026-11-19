"""B1.1 - the cleaning rules on a small file that contains every problem of A1.1 (station reports Fahrenheit).
Shows the data before and after cleaning."""
from collections import Counter
from cleaning import clean_text, fill_missing

text = open("small_test.csv", encoding="utf-8").read()
print("BEFORE (raw file, one line per row):")
for i, line in enumerate(text.splitlines()):
    note = {1: "ok (temperature in Fahrenheit)", 2: "pm25 = NA", 3: "pm25 blank", 4: "pm25 negative", 5: "pm25 and pm10 too large",
            6: "pm25 is the word ERR", 7: "exact duplicate of line 1", 8: "date written dd/mm/yyyy", 9: "hour 24 does not exist",
            10: "spaces around the number", 11: "no2 = NA, temp 300 F impossible", 12: "ok"}.get(i, "")
    print(f"  {i:>2}  {line:<34}{note}")

c = Counter()
rows = clean_text(text, fahrenheit=True, counter=c)
filled = fill_missing(rows, "ffill", counter=c)
print("\nAFTER cleaning (no fill)           AFTER forward fill (limit 3 hours)")
print(f"  {'day':<11}{'h':>2}{'pm25':>7}{'pm10':>7}{'no2':>6}{'temp_c':>8}   |{'pm25':>7}{'pm10':>7}{'no2':>6}{'temp_c':>8}")
fmt = lambda v: "None" if v is None else f"{v:g}"
for a, b in zip(rows, filled):
    print(f"  {a['day']:<11}{a['hour']:>2}{fmt(a['pm25']):>7}{fmt(a['pm10']):>7}{fmt(a['no2']):>6}{fmt(a['temp_c']):>8}   |"
          f"{fmt(b['pm25']):>7}{fmt(b['pm10']):>7}{fmt(b['no2']):>6}{fmt(b['temp_c']):>8}")
print("\ncounters:", dict(c))

# checks (expected values calculated by hand)
assert len(rows) == 10                                  # 12 data lines - 1 duplicate - 1 bad hour
assert rows[0]["temp_c"] == 24.0                        # (75.2 - 32) * 5/9 = 24.0
assert rows[6]["day"] == "2026-10-01" and rows[6]["hour"] == 6        # dd/mm/yyyy date normalised
assert rows[3]["pm25"] is None                           # -12 is impossible
assert rows[4]["pm25"] is None and rows[4]["pm10"] is None      # 9999 and 1500 are impossible
assert rows[7]["pm25"] == 62.0                           # spaces removed
assert rows[8]["no2"] is None and rows[8]["temp_c"] is None      # NA and 300 F = 148.9 C
assert filled[1]["pm25"] == filled[2]["pm25"] == filled[3]["pm25"] == 48.0   # forward fill from hour 0, 3 hours
assert filled[4]["pm25"] is None                         # the 4th missing hour in a row is NOT filled (limit 3)
print("all checks passed")
