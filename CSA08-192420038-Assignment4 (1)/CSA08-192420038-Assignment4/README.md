# CSA0806 – Python Programming | Assignment 4 (CO4)
## Robust data processing with files, exceptions, modules and packages

- Name: Dhatri
- Register number: 192420038
- Course: CSA0806 – Python Programming
- Python version: 3.12
- Libraries: standard library only (see `requirements.txt`)
- GitHub repository name: `CSA08-192420038-Assignment4`

Run every program from inside its own task folder (`cd Task03`, then the command shown).

| Task | Run | Result in one line |
|---|---|---|
| 1 Repair the mess-bill script | `python original_script.py`, `python mess_total.py [file]`, `python compare_read_methods.py` | original reports Total 2425 and silently drops 5 lines; repaired version: 6251.50 with 3 rejected lines listed |
| 2 Biometric attendance | `python attendance_monthly.py`, `python trace_demo.py`, `python compare_reread.py` | 5 students' percentages, 2 below 75 %, 4 log entries; re-reading per student is 400× more line reads at 400 students |
| 3 Error handling | `python complete_code.py` (TODO 1, 2), `python failures.py`, `python misuse_experiment.py`, `python compare_eafp_lbyl.py` | expected tuple printed; `except Exception: pass` returns (0, 0, []) silently |
| 4 File forensics | `python test_defects.py`, `python test_fixed.py`, `python compare_with_vs_finally.py` | 4 defects shown; repaired log keeps all days; 100 failed calls leave 100 files open in the original, 0 with `with` |
| 5 Four organisations | `python count_changes.py`, `python measure_import.py`, `python naming_demo.py`; each `main_*.py` / `attendance_all.py` inside `after_change/<organisation>/` | new report needs 1 / 2 / 3 / 3 changed files for (a) / (b) / (c) / (d) |
| 6 Fest registration package | `python main.py`, `python test_fest.py`, `python compare_duplicate_detection.py` | 14 lines → 7 students, 6 rejected, 1 duplicate merged, 1 missing file; list search 570× slower than a set at 40,000 |

Each folder contains `output_<program>.txt` (captured output), sample input files, diagrams (`Task06/flow_diagram.png`, `Task06/package_structure.png`) and a `screenshots/` folder (rendered images of the program output; replace them with screenshots of your own runs).


---
**Note (file-count reduction):** to keep the submission under 100 files, the `screenshots/` folders and the regenerable `out/`/`out_oct/` result folders were removed. Re-create the outputs by running the programs again and the screenshots with `python make_screenshots.py` (or take your own screenshots).
