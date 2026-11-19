# CSA0806 – Python Programming | Assignment 5 (CO5)
## Data acquisition, cleaning, analysis and AI applications – city air-quality network

- Name: Dhatri
- Register number: 192420038
- Course: CSA0806 – Python Programming
- Python version: 3.12
- Libraries: pandas 3.0, matplotlib 3.11, scikit-learn 1.9 (only one program), standard library (see `requirements.txt`)
- GitHub repository name: `CSA08-192420038-Assignment5`

**Order of running:** `cd data && python generate_data.py` (creates the 372 raw files) → `cd ../TaskB1 && python pipeline.py` (cleans them and creates `airquality.db`) → everything else. Run each program from inside its own folder. The data are generated (the case study gives no files).

| Task | Run | Result in one line |
|---|---|---|
| A1 Acquisition design | `inspect_source.py`, `compare_csv_vs_sql.py`; `schema.sql`, `design.md` | 8 kinds of problem found in 8,966 rows; SQL with an index answers in 0.19 ms at 1 million rows against 0.58 s for pandas |
| A2 Cleaning design | `normalisation_demo.py`, `compare_missing_strategies.py`; `design.md` | forward fill beats dropping when gaps are not random (bias −0.86 against −1.42) |
| A3 Analysis design | `summary_python_vs_sql.py`; `design.md` | SQL GROUP BY 4× faster and 19× less memory than Python loops |
| A4 Debugging/profiling | `buggy_cleaning.py`, `run_pdb_demo.py`, `print_vs_logging.py`; `design.md` | switched-on logging costs 9.8 µs per call, switched off 0.18 µs |
| A5 AI design | `chatbot.py`; `design.md` | rule-based chatbot with 9 limitations |
| B1 Cleaning pipeline | `test_small.py`, `pipeline.py`, `complete_code.py`, `complete_code_999.py`, `queries.py`, `charts.py`, `compare_pandas.py` | 8,966 rows → 8,912 clean rows in SQLite; 5 charts; pandas 4.6× faster at 1 million rows |
| B2 Adversarial data | `adversarial_files.py`, `sql_injection_demo.py`, `sentiment_adversarial.py`, `complete_code.py`, `compare_executemany.py` | bad files rejected; `?` placeholder stops injection; scorer wrong on 9 of 11 hard sentences |
| B3 Loops vs libraries vs SQL | `run_experiment.py`, `profile_python.py` | all three agree; `statistics.mean` is 42 % of the Python time |
| B4 Final decision | `complete_code.py`, `evaluate.py`, `index_test.py`, `naive_bayes_compare.py` | scorer agrees on 94 % (52 tuned) / 83 % (12 new); index makes the slowest query 2.8× faster |

Each folder contains `output_<program>.txt` (captured output) and a `screenshots/` folder (rendered images of the output; replace them with screenshots of your own runs).


---
**Note (file-count reduction):** to keep the submission under 100 files, the 372 raw CSV files in `data/raw/` and the `screenshots/` folders were removed. Re-create the raw files with `cd data && python generate_data.py` (seeded, gives identical files) and the screenshots with `python make_screenshots.py` (or take your own screenshots).
