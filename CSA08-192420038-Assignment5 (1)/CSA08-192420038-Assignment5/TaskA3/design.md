# Task A3 – Design the Analysis and Visualisation (K4)

**Files:** `TaskA3/design.md`, `summary_python_vs_sql.py`; the charts are drawn in `TaskB1/charts.py`.

## A3.1 Choice of charts

| Question of the board | Chart | Why this chart |
|---|---|---|
| **Trend of PM2.5 over a month** | **Line chart**: x = day, y = daily mean PM2.5, one line per selected station plus the network mean and a line at the 60 µg/m³ standard | Time is ordered and continuous; a line shows direction, peaks and weekly rhythm. Daily means (not 24 × 31 hourly points) remove hourly noise. A bar chart would hide the continuity. |
| **Comparison of stations** | **Horizontal bar chart** of the monthly mean per station, sorted, bars above 60 coloured red; plus a **box plot** of the hourly values per station when the *spread* matters | Categories without order are compared by length, which the eye reads best; sorting gives a ranking. A box plot adds median, quartiles and extreme hours that a single mean hides. |
| **Relationship between temperature and PM2.5** | **Scatter plot**: x = daily mean temperature, y = daily mean PM2.5, one point per station-day, with the correlation coefficient r in the title | Two numeric variables; a scatter shows the shape, strength and outliers of a relationship. A line chart would suggest an order that does not exist. |
| **Hours with the worst air** | **Bar chart of the mean PM2.5 for each hour of the day (0–23)**, the 3 highest bars coloured | The hour is a category on a cycle; 24 bars show the daily pattern (rush-hour peaks). A histogram is for the *distribution of values*, not for the hour of the day. |

(A histogram of all PM2.5 values would be chosen to see how the values are distributed, e.g. to detect skew; it is not needed for the four questions.) Every chart needs a title, labelled axes with units and, where relevant, the standard line, so that it can be read without the report.

## A3.2 The daily summary table
| Column | Meaning |
|---|---|
| `station_id`, `day` | key of the row |
| `pm25_min`, `pm25_max` | lowest and highest valid hourly value of the day |
| `pm25_mean` | mean of the valid hourly values |
| `n_valid` | **number of valid readings** (0–24); a mean based on 4 values must not be read like one based on 24 |

It is produced in the database by **one grouped query**, ignoring `NULL`:
```
SELECT station_id, day, MIN(pm25), MAX(pm25), AVG(pm25), COUNT(pm25)
FROM readings GROUP BY station_id, day          (COUNT(pm25) counts only non-missing values)
```
Pseudocode of what the database does: *read each row once; put it in the group of its (station_id, day); update the group's minimum, maximum, sum and count; at the end divide sum by count for every group.* The result (12 stations × 31 days = 372 rows) can be stored as a table or a view.

## Alternative – the daily summary computed in Python loops
```
rows <- FETCH ALL rows from the database                 O(n) time and O(n) memory (every row in Python)
groups <- empty dictionary
FOR EACH row DO  IF pm25 is not missing THEN APPEND pm25 TO groups[(station, day)]
FOR EACH group DO  summary <- (MIN, MAX, SUM / LENGTH, LENGTH)
```
```text
stations       rows |  Python loops: time  peak memory |  SQL GROUP BY: time  peak memory | same result
       1      8,760 |             0.028 s       1.8 MB |             0.006 s      0.09 MB | True
      12    105,120 |             0.375 s      21.6 MB |             0.094 s      1.16 MB | True
     120  1,051,200 |             4.230 s     218.3 MB |             0.988 s     11.56 MB | True
```

| Rows | Python loops: time / peak memory | SQL GROUP BY: time / peak memory | Same result |
|---|---|---|---|
| 8,760 | 0.028 s / 1.8 MB | 0.006 s / 0.09 MB | yes |
| 105,120 | 0.375 s / 21.6 MB | 0.094 s / 1.16 MB | yes |
| 1,051,200 | 4.230 s / 218.3 MB | 0.988 s / 11.56 MB | yes |

**Time:** both are O(n) – each row is handled once, and 10× more rows took about 10× more time – but SQLite does the loop in compiled code, so it was 4–5 times faster. **Memory:** the Python version holds all n readings in memory – O(n) (218 MB for a million rows); SQL holds only one running total per group and returns the result – O(groups) = O(stations × days) (11.6 MB, of which most is the result list). For 3.9 million rows a year (A5/B4 scale) the Python version would need about 0.8 GB, SQL stays small. Python loops are acceptable only for small data or when the summary needs logic that SQL cannot express.

