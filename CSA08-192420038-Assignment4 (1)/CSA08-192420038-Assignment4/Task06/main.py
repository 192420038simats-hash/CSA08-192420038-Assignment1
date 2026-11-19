"""Run the fest registration desk:  python main.py  [data_folder] [output_folder]"""
import sys
from fest.pipeline import run

DEPARTMENTS = ["cse", "ece", "mech", "civil", "it"]          # the five departments (it.txt is missing on purpose)

if __name__ == "__main__":
    data = sys.argv[1] if len(sys.argv) > 1 else "data"
    out = sys.argv[2] if len(sys.argv) > 2 else "out"
    try:
        counters, n, events = run(data, out, DEPARTMENTS)
    except OSError as e:                                      # the output folder itself cannot be written
        sys.exit(f"Cannot write the outputs: {e}")
    for k, v in counters.items():
        print(f"{k:<28}{v:>4}")
    print(f"{'students in master list':<28}{n:>4}")
    print("participants per event:", events)
    print(f"outputs written to '{out}/': master_list.csv, events/, summary_report.txt, error_log.txt")
