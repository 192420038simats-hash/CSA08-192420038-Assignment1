"""(b) main script that imports the module."""
from pathlib import Path
import attendance_lib as lib

DATA = Path(__file__).resolve().parents[2] / "data"
OUT = Path(__file__).resolve().parent / "out"

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    records, errors = lib.read_month(DATA)
    pcts = lib.attendance_percentages(records)
    lib.write_percentage_report(pcts, OUT / "percent.csv")
    lib.write_error_log(errors, OUT / "errors.log")
    print("below 75 %:", lib.below_limit(pcts))
    print("errors logged:", len(errors))
