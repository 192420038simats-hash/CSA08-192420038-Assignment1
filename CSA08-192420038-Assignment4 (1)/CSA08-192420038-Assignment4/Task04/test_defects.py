"""Task 4.2 - evidence: run process() for three days and print the log; show the file left open by a failed write()."""
import os, tempfile
from library_original import process, save_returns

work = tempfile.mkdtemp(); os.chdir(work)
days = {"day1.txt": ["Python Basics", "Data Structures"], "day2.txt": ["Operating Systems", "Networks"], "day3.txt": ["Algorithms", "Databases"]}
for name, books in days.items():
    with open(name, "w") as f:
        f.write("\n".join(books) + "\n")

print("Defect 1 and 2: three days processed one after the other")
for name in days:
    process(name)
    print(f"  after {name}: returns.log = {open('returns.log').read()!r}")
print("  -> the log holds ONLY day 3 (mode 'w' empties the file each time) and the titles are run together (no newline).")

print("\nDefect 3: a write() that fails leaves the file open and its buffered data unsaved")
def open_files():
    return len(os.listdir("/proc/self/fd"))
open("returns.log", "w").close()
before = open_files()
held = None
try:
    save_returns(["Chemistry", None, "Physics"])       # None cannot be written -> TypeError
except TypeError as e:
    held = e                                          # an error reporter / debugger / test runner keeps the exception
print(f"  TypeError raised by write(); open file descriptors before {before}, after {open_files()}  (one file left open)")
print(f"  content of returns.log on disk while the file is still open: {open('returns.log').read()!r}  ('Chemistry' was lost)")
print("  process() catches only FileNotFoundError, so this TypeError stops the program and no message is written anywhere.")
del held

print("\nDefect 4: process() opens the day file and never closes it explicitly")
before = open_files()
keep = [open("day1.txt") for _ in range(3)]            # same effect as open(day_file).read() when the frame/object is kept alive
print(f"  3 files opened without close(): descriptors {before} -> {open_files()}")
for k in keep: k.close()
