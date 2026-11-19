# Task A2 – Design the Cleaning and Normalisation (K4)

**Files:** `TaskA2/design.md`, `compare_missing_strategies.py`, `normalisation_demo.py`; the implementation is `TaskB1/cleaning.py`.

## A2.1 Cleaning rules

| Problem | Rule | Justification |
|---|---|---|
| **Missing value** (blank, `NA`, `N/A`, `ERR`, `--`) | Convert to *missing*. Then **forward fill** (use the previous valid value of the same station and column) for **at most 3 consecutive hours**; a longer gap stays `NULL`. | Air quality changes slowly from hour to hour, so a value of 1–3 hours ago is a good estimate; beyond 3 hours the value is a guess, so it is left missing and the number of valid readings is reported. *Median fill* flattens real peaks and *dropping* shrinks the count and can bias the daily mean when gaps are not random (see the alternative). |
| **Impossible value** | PM2.5, PM10, NO₂ outside 0–999 µg/m³ and temperature outside −10 to 55 °C (after conversion) are sensor faults: set to *missing* (and then treated by the rule above). Never clip to the limit. | A negative concentration is physically impossible; 9999 is beyond the instrument range. Clipping would invent a measurement. |
| **Duplicate rows** | Rows with the same station, date and hour: **keep the first**, remove the others, count them in the report. | One reading per hour is the rule; the first one received is the original, a repeat is a transmission error. |
| **Fahrenheit temperatures** | For stations whose `temp_unit` is `F`: °C = (°F − 32) × 5 / 9, rounded to 0.1, **before** the range check. A check warns if any station mean is above 50. | The unit is a property of the station (from `stations.csv`), not guessed from single values; converting first means 300 °F is rejected as 148.9 °C. |
| Date written as dd/mm/yyyy | Accept `YYYY-MM-DD`, `DD/MM/YYYY`, `DD-MM-YYYY`; store ISO; reject any other text. | One format lets dates sort and group; a row with no valid date cannot be placed in time, so it is rejected and counted. |
| Hour outside 0–23 | Reject the row, count it. | The hour is part of the row's identity. |

**Pseudocode of the rules**
```
ALGORITHM CleanStationFile(text, fahrenheit)
1  IF text is empty THEN RAISE CleaningError;  IF header <> (date, hour, pm25, pm10, no2, temp) THEN RAISE CleaningError
2  rows <- empty list;  seen <- empty set
3  FOR EACH line IN text AFTER the header DO
4      day <- ParseDate(line.date);  IF day is invalid THEN count "bad date"; CONTINUE
5      hour <- INTEGER(line.hour);   IF hour NOT IN 0..23 THEN count "bad hour"; CONTINUE
6      IF (day, hour) IN seen THEN count "duplicate"; CONTINUE
7      ADD (day, hour) TO seen
8      FOR EACH column IN (pm25, pm10, no2, temp) DO
9          v <- ToNumber(line.column)                    (blank, NA, ERR, -- give "missing")
10         IF column = temp AND fahrenheit THEN v <- (v - 32) * 5 / 9
11         IF v is not missing AND v NOT IN valid range of column THEN v <- missing
12     APPEND the row TO rows
13 RETURN rows

ALGORITHM ForwardFill(rows of ONE station sorted by day, hour; limit = 3)
1  FOR EACH column DO  last <- none;  gap <- 0
2     FOR EACH row IN rows DO
3         IF row.column is missing THEN  gap <- gap + 1;  IF last exists AND gap <= limit THEN row.column <- last
4         ELSE  last <- row.column;  gap <- 0
```

## A2.2 Normalisation of PM2.5
**Min–max:** v′ = (v − min) / (max − min); the result lies in **[0, 1]**; 0 is the smallest and 1 the largest value. **z-score:** z = (v − mean) / σ (population standard deviation); the result has mean 0 and standard deviation 1; it is *unbounded* and measures "how many standard deviations from normal".

*When to use which.* **Min–max** when a bounded scale is needed (to put PM2.5, PM10 and NO₂ on one 0–1 chart or into a pollution index, or for algorithms that expect 0–1 inputs) and the data have no extreme outliers, because one extreme value squeezes all the others into a narrow band. **z-score** when the aim is to compare stations or hours with different levels and spreads, to **detect outliers** (|z| > 3), or when the data are roughly bell-shaped; it is less distorted by one extreme value because it uses mean and σ. In the database the **original values are kept** (real units are needed for the 60 µg/m³ standard); normalised values are computed when analysing. Demonstration on Adyar's hours of one day, with and without one real smoke event of 480 µg/m³:
```text
Adyar, 5 Oct 2026, 24 hourly PM2.5 (first 8): [25.3, 56.2, 48.4, 45.0, 70.5, 30.9, 61.7, 49.0]

normal day: n = 24
  raw value        : ['25.3', '56.2', '48.4', '45', '70.5', '30.9'] ... last 30.7
  min-max (0 to 1) : [0.062, 0.627, 0.484, 0.422, 0.888, 0.165] ... last 0.161
  z-score          : [-1.456, 0.875, 0.287, 0.03, 1.954, -1.033] ... last -1.048
  min-max: values of the ordinary hours lie between 0.000 and 1.000

same day + one real smoke event of 480: n = 25
  raw value        : ['25.3', '56.2', '48.4', '45', '70.5', '30.9'] ... last 480
  min-max (0 to 1) : [0.007, 0.075, 0.058, 0.05, 0.106, 0.02] ... last 1.0
  z-score          : [-0.425, -0.067, -0.158, -0.197, 0.098, -0.36] ... last 4.843
  min-max: values of the ordinary hours lie between 0.000 and 0.119
```

With the extreme value, min–max squeezes the 24 ordinary hours into 0.00–0.12 (the differences between ordinary hours almost disappear), while the z-score still marks the event clearly (z = 4.8) and keeps the ordinary hours spread between −0.47 and +0.17 (a range of 0.63, against 0.12 for min–max).

## A2.3 Standard formats
| Item | Standard in the cleaned data |
|---|---|
| Date | ISO 8601 `YYYY-MM-DD`, text (e.g. `2026-10-01`); hour as an integer 0–23 |
| Station name | standard name in Title Case with single spaces (`Anna Nagar`, `T Nagar`), plus a 3-letter upper-case id (`ANN`); file names use lower case and underscores |
| Numbers | PM2.5, PM10, NO₂ in µg/m³ and temperature in °C, one decimal place, a dot as decimal separator, no thousands separators, no units in the cell; missing = empty in CSV and `NULL` in SQL (never 0, `NA` or −999) |
| Text file | UTF-8, comma delimiter, header row, one reading per line |

## Alternative – drop missing readings instead of filling
"Dropping" means leaving the value missing so that `AVG`/`mean` ignore it: **O(n)** time (one pass, nothing to compute), **O(1)** extra space. Forward fill is also **O(n)** (one pass keeping the last value); the median needs the sorted values, **O(n log n)**, and a copy of the column. To measure the effect on the **daily averages** a complete series was made, values were deleted (in runs of 1–4 hours), each strategy was applied and the daily means compared with the true ones:
```text
pattern        missing strategy |  mean abs error of daily means (ug/m3)    bias
random gaps         5%     drop |                                   0.41   +0.02
random gaps         5%    ffill |                                   0.45   -0.09
random gaps         5%   median |                                   0.56   +0.04
random gaps        15%     drop |                                   1.22   +0.22
random gaps        15%    ffill |                                   1.18   +0.12
random gaps        15%   median |                                   1.58   +0.41
random gaps        30%     drop |                                   2.12   -0.21
random gaps        30%    ffill |                                   2.12   -0.06
random gaps        30%   median |                                   2.85   -0.14
evening gaps        5%     drop |                                   0.67   -0.56
evening gaps        5%    ffill |                                   0.52   -0.18
evening gaps        5%   median |                                   0.71   -0.52
evening gaps       15%     drop |                                   1.93   -1.42
evening gaps       15%    ffill |                                   1.59   -0.86
evening gaps       15%   median |                                   1.95   -1.27

Time for 4 columns (rows are dictionaries) and extra memory for the filled copy
     rows    drop s   ffill s  median s
   10,000     0.004     0.004     0.008
  100,000     0.045     0.049     0.102
  400,000     0.343     0.406     0.670
```

| Gaps | Strategy | Mean abs. error of daily mean (µg/m³) | Bias |
|---|---|---|---|
| random, 15 % | drop / forward fill / median | 1.22 / **1.18** / 1.58 | +0.22 / +0.12 / +0.41 |
| random, 30 % | drop / forward fill / median | 2.12 / 2.12 / 2.85 | −0.21 / −0.06 / −0.14 |
| evening peak, 15 % | drop / forward fill / median | 1.93 / **1.59** / 1.95 | −1.42 / **−0.86** / −1.27 |

When gaps are **random**, dropping and forward fill are equally good and the median is worst. When gaps fall in the **evening peak** (not random – sensors often fail under load), dropping removes the highest hours and **underestimates the daily mean by 1.4 µg/m³**; forward fill reduces that bias to 0.9. The time for 400,000 rows (four columns) was 0.34 s (drop), 0.41 s (forward fill), 0.67 s (median), showing the O(n) against O(n log n) difference. **Decision:** forward fill with a limit of 3 hours, keep `n_valid` in the summary so that days with many gaps are visible.
