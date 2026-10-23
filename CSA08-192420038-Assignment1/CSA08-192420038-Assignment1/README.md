# CSA0806 – Python Programming | Assignment 1
## Design, Implement and Validate a Payment Calculator for a Village Milk Co-operative

- Name: Dhatri
- Register number: 192420038
- Course: CSA0806 – Python Programming
- Python version: 3.12 (any 3.9+ works)
- Libraries: standard library only (`decimal`, `json`, `time`, `timeit`, `math`, `sys`, `random`, `tracemalloc`) – see `requirements.txt`
- GitHub repository name: `CSA08-192420038-Assignment1`

Run every program from inside its own task folder (`cd Task07`, then the command shown).

| Task | Run | Result in one line |
|---|---|---|
| 1 | `python data_model.py` | One tuple per entry keeps the source constant; separate variables need 600+ lines for 300 farmers |
| 2 | `python task2_decimal.py` (TODO 1), `python task2_decimal_from_float.py`, `python task2_alternatives.py`, `python make_session.py` | float total 33400.30000000061, Decimal 33400.30; Decimal(float(x)) re-imports the float error |
| 3 | `python constants.py`, `python alternatives.py` | One constants block; dynamic typing and swap demonstrated |
| 4 | `python expressions.py`, `python alternatives.py` | Step counts need round(); int() gives wrong rate for fat 3.1 |
| 5 | `python input_reader.py`, `python alternatives_timing.py` | "8,5" and "eight" rejected before conversion; aligned f-string output |
| 6 | `python functions.py`, `python alternatives.py` | Functions cost no measurable extra time |
| 7 | `python milkrate.py`, `python use_milkrate.py`, `python alternatives.py` | Output matches the expected table; table not printed on import |
| 8 | `python ten_day_total.py`, `python measure_space.py` | List version O(n) space, running total O(1) space |
| 9 | `python calculator.py`, `python test_calculator.py` | 21 test cases + 5-entry hand total 1458.75 all pass |
| 10 | `python compare.py` | float and Decimal totals differ (Rs 69.31 at 150,000 payments) |
| 11 | `python milkpay.py`, `python alternatives.py` | Recommended design: Decimal + ROUND_HALF_UP + JSON rate card |
| 12 | `python test_v2.py`, `python milkpay_v2.py` | Seasonal cards, two-decimal readings, bonus: 14 tests pass |

Each folder also contains `output_<program>.txt` (captured output). Task 8 has the flowchart image and Task 12 the module (UML) diagram. Each task folder has a `screenshots/` folder (rendered images of the program output; replace them with screenshots of your own runs).
