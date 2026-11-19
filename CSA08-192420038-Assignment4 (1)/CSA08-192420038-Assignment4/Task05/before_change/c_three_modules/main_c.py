"""(c) main script."""
from pathlib import Path
from reader import read_month
from stats import attendance_percentages, below_limit
from report import write_percentage_report, write_error_log

DATA = Path(__file__).resolve().parents[2] / "data"
OUT = Path(__file__).resolve().parent / "out"

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    records, errors = read_month(DATA)
    pcts = attendance_percentages(records)
    write_percentage_report(pcts, OUT / "percent.csv")
    write_error_log(errors, OUT / "errors.log")
    print("below 75 %:", below_limit(pcts))
    print("errors logged:", len(errors))
