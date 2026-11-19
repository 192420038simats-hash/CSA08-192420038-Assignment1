"""(d) main script using the package."""
from pathlib import Path
from attendance import reader, stats, report

DATA = Path(__file__).resolve().parents[2] / "data"
OUT = Path(__file__).resolve().parent / "out"

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    records, errors = reader.read_month(DATA)
    pcts = stats.attendance_percentages(records)
    report.write_percentage_report(pcts, OUT / "percent.csv")
    report.write_error_log(errors, OUT / "errors.log")
    print("below 75 %:", stats.below_limit(pcts))
    print("errors logged:", len(errors))
    absent = stats.consecutive_absences(records)
    report.write_absent_report(absent, OUT / "absent_3_days.txt")
    print("absent 3 or more consecutive days:", absent)
