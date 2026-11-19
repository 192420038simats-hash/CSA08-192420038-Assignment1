# Task A4 – Plan Debugging and Profiling (K4)

**Files:** `TaskA4/design.md`, `buggy_cleaning.py`, `run_pdb_demo.py`, `print_vs_logging.py`.

## A4.1 Debugging plan for the cleaning code
The tools are used in this order, from cheapest to most powerful:

| Tool | Use in the cleaning code | Where / when |
|---|---|---|
| `print` | a quick look at a suspicious value while writing the first version | only on a few lines and removed afterwards |
| **`assert`** | to state what must be true: `assert -10 <= c <= 55` after the Fahrenheit conversion; `assert len(rows) <= 24` for a station-day; `assert set(row) == {...}` | at the end of each cleaning step, so that a wrong result stops the program *at the step that made it* |
| **`logging`** | to record what the pipeline did: INFO "372 files read, 38 duplicates removed", WARNING "file is not UTF-8", ERROR "file skipped: missing column pm10", DEBUG per-row details | everywhere in the pipeline; levels, time stamps and the file name make the record usable later and the level switches it on or off |
| **`pdb`** (or the IDE debugger) | when an assert fails and the cause is not obvious: set a breakpoint (`b file:line`), run (`c`), print variables (`p`), step (`n`, `s`), quit (`q`) | to inspect the real values at the moment of the error without editing the code |

**Demonstration** – the function has a precedence bug (`f - 32 * 5 / 9` instead of `(f - 32) * 5 / 9`). The `assert` stops the program with a message that names the input and the impossible result; the `logging` line shows the value; `pdb` shows that the wrong formula gives 57.4 while the right one gives 24.0:
```text
DEBUG f_to_c: f_to_c(75.2) = 57.422222222222224
Traceback (most recent call last):
  File "/home/claude/a5/CSA08-192420038-Assignment5/TaskA4/buggy_cleaning.py", line 21, in <module>
    main()
  File "/home/claude/a5/CSA08-192420038-Assignment5/TaskA4/buggy_cleaning.py", line 17, in main
    print(f"{f} F ->", f_to_c(f), "C")
                       ^^^^^^^^^
  File "/home/claude/a5/CSA08-192420038-Assignment5/TaskA4/buggy_cleaning.py", line 11, in f_to_c
    assert -10 <= c <= 55, f"temperature {c:.1f} C is impossible for input {f} F"
           ^^^^^^^^^^^^^^
AssertionError: temperature 57.4 C is impossible for input 75.2 F
```
```text
commands typed into pdb:  b buggy_cleaning.py:10 | c | p f | p c | p f - 32 * 5 / 9 | p (f - 32) * 5 / 9 | n | q

> buggy_cleaning.py(1)<module>()
-> """A4 - a cleaning function with a deliberate precedence bug, used to demonstrate print / assert / logging / pdb."""
(Pdb) Breakpoint 1 at buggy_cleaning.py:10
(Pdb) > buggy_cleaning.py(10)f_to_c()
-> log.debug("f_to_c(%s) = %s", f, c)
(Pdb) 75.2
(Pdb) 57.422222222222224
(Pdb) 57.422222222222224
(Pdb) 24.0
(Pdb) > buggy_cleaning.py(11)f_to_c()
-> assert -10 <= c <= 55, f"temperature {c:.1f} C is impossible for input {f} F"
(Pdb) DEBUG f_to_c: f_to_c(75.2) = 57.422222222222224
```
A unit test with a hand-calculated expected value (75.2 °F = 24.0 °C, as in B1) would find the same bug before the program is run on real data.

## A4.2 Profiling plan
1. **`time.perf_counter()`** around each stage (reading, cleaning, filling, loading into SQLite, querying, charts) gives the time of the stages; the largest stage is the candidate. 2. **`timeit`** runs a small piece of code many times (e.g. `to_number` or `statistics.mean` against `sum()/len()`) to compare two ways of writing the same thing; it repeats the run to reduce noise. 3. **`cProfile`** (+ `pstats`) is run on the slowest stage and sorted by `tottime` (time spent inside the function itself) and `cumulative` (including the functions it calls) to find the *function* that takes most of the time, and how many times it is called. The order matters: measure first (the stages), then locate (the function), and only then change the code; B3.3 follows this plan.

## Alternative – print statements for all debugging
```
print(f"cleaned value {x}")            # in the loop, deleted or commented out when finished
```
```text
method                                           time s   extra per call (microseconds)
no debugging at all                               0.056                            0.00
print() to a file                                 0.113                            0.28
logging.debug, level DEBUG, to a file             2.015                            9.80
logging.debug, level WARNING (switched off)       0.092                            0.18
logging.disable(CRITICAL)                         0.077                            0.10
if DEBUG: print(...)  with DEBUG = False          0.056                            0.00

log file written by the DEBUG-level run: 9.8 MB for 200,000 messages
```

| Method (200,000 calls in a cleaning loop) | Time | Extra time per call |
|---|---|---|
| no debugging | 0.056 s | – |
| `print()` to a file | 0.113 s | 0.28 µs |
| `logging.debug`, level DEBUG, to a file | 2.015 s | 9.80 µs |
| `logging.debug`, level WARNING (off) | 0.092 s | 0.18 µs |
| `logging.disable(CRITICAL)` | 0.077 s | 0.10 µs |
| `if DEBUG: print(...)` with `DEBUG = False` | 0.056 s | ≈ 0 |

**Extra time:** a `print` to a file is cheap (0.28 µs), printing to a screen is usually slower still (not measured here); a *switched-on* logging call costs about 10 µs because it builds a record, formats the time stamp and writes to a file – 200,000 messages cost 2 s and 9.8 MB. So thousands of messages slow the program and the log must be kept for few hot loops. **Switching off:** with `print` the lines must be deleted or commented out (risk of forgetting one, or of deleting a needed line), or guarded by a flag. With `logging` nothing is edited: raising the level to WARNING (or `logging.disable`) makes the calls almost free (0.18 µs) and the same program can run in "quiet" or "detailed" mode, send messages to a file, and show the time and the module. `assert` statements are removed completely when Python runs with `-O`. A debugger needs no change of the program at all.
