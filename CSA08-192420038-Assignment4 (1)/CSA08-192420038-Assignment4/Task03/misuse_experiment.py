"""Task 3.4 - what happens when specific except clauses are replaced by 'except Exception: pass'."""
import tempfile, os
from processor import parse_line, InvalidRecord

data = "192311001,2026-10-08,P\n192311002,2026-10-08,A\n192311003,2026-10-08,P\n"
with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as t:
    t.write(data)
path = t.name


def summarise_specific(path):
    present = absent = 0
    errors = []
    try:
        with open(path, encoding="utf-8") as f:
            for number, line in enumerate(f, start=1):
                try:
                    _, _, status = parse_line(line)
                except InvalidRecord as e:
                    errors.append((number, str(e)))
                else:
                    if status == "P":
                        present += 1          # correct spelling
                    else:
                        absent += 1
    except FileNotFoundError:
        errors.append((0, "file not found"))
    return present, absent, errors


def summarise_misused(path):
    present = absent = 0
    errors = []
    try:
        with open(path, encoding="utf-8") as f:
            for number, line in enumerate(f, start=1):
                _, _, status = parse_line(line)
                if status == "P":
                    presnt += 1               # <-- typing error in the variable name
                else:
                    absent += 1
    except Exception:
        pass                                  # <-- hides EVERY error
    return present, absent, errors


print("correct data, misused version :", summarise_misused(path), " <- the right answer is (2, 1, [])")

# the same typing error in the version with specific except clauses
def summarise_typo_specific(path):
    present = absent = 0
    errors = []
    try:
        with open(path, encoding="utf-8") as f:
            for number, line in enumerate(f, start=1):
                try:
                    _, _, status = parse_line(line)
                except InvalidRecord as e:
                    errors.append((number, str(e)))
                else:
                    if status == "P":
                        presnt += 1           # same typing error
                    else:
                        absent += 1
    except FileNotFoundError:
        errors.append((0, "file not found"))
    return present, absent, errors

try:
    summarise_typo_specific(path)
except Exception as e:
    print("specific excepts, same typo    :", type(e).__name__ + ":", e, " <- the error is visible and points to the line")
print("specific excepts, no typo      :", summarise_specific(path))
os.remove(path)
