# CSA08 – Python Programming – Assignment 2 (CO2)

| | |
|---|---|
| **Name** | Dhatri |
| **Register number** | 192420038 |
| **Course** | CSA0806 Python Programming |
| **Python version** | 3.12.3 (match-case in Q1 needs 3.10+) |
| **Libraries** | Standard library only – see `requirements.txt` |
| **Submission date** | 30/10/2026 |

## How to run
```
cd Q1 && python q1.py      # likewise q2.py ... q7.py in Q2 ... Q7
```
Each folder holds the source file, `output.txt` (captured console output) and, for Q7, `q7_raw_data.csv`.
Add your own screenshots to each folder (`Q1/screenshot.png`, ...). The full write-up is in `REPORT.md`.

## Results at a glance
| Task | Result |
|---|---|
| Q1 | Separate `if`s give two subsidies for a 50-unit household with a ration card; `if-elif-else` gives exactly one. All 9 boundary cases match predictions. |
| Q2 | `while`, `for` and recursive OTP loops agree on 3 scenarios; blank entries are not counted; `else` locks the account; limit 5 after security answer. |
| Q3 | Expected output reproduced exactly; 6/6 designed inputs match predictions; regex agrees with slicing. |
| Q4 | Same 3,048,890-character text from all builders; `join` fastest; `+=` shows quadratic growth once the CPython optimisation is defeated. |
| Q5 | Shared default list demonstrated through `__defaults__`; fixed with `None`; three customers independent; scope demos. |
| Q6 | naive 242,785 calls vs memo 26 for n = 25; RecursionError at n = 1000 (limit 1000); loop solution. |
| Q7 | Recursive Fibonacci-type counter redesigned as a loop: 2,692,537 calls -> 29 steps for n = 30. |

## Commit history suggestion
`git commit` once per task, for example: "Q1: subsidy rule and boundary tests", "Q2: OTP loops", ... "Q7: redesign and validation".
