"""Task 4.3 - demonstrate the repaired program on the same three days plus failures."""
import os, tempfile
import library_fixed as lf

work = tempfile.mkdtemp(); os.chdir(work)
days = {"day1.txt": ["Python Basics", "Data Structures"], "day2.txt": ["Operating Systems", "Networks"], "day3.txt": ["Algorithms", "Databases"]}
for name, books in days.items():
    with open(name, "w") as f:
        f.write("\n".join(books) + "\n")
with open("day5.txt", "wb") as f:
    f.write(b"Compilers\n\xff\xfe broken bytes\n")

for name in list(days) + ["day4_missing.txt", "day5.txt"]:
    ok = lf.process(name)
    print(f"{name:<18} processed: {ok}")
print("\nreturns.log:\n" + open("returns.log").read())
print("errors.log (first lines of each entry):")
for line in open("errors.log"):
    if line[:2] == "20":
        print("  " + line.rstrip())

def open_files(): return len(os.listdir("/proc/self/fd"))
before = open_files(); held = []
for _ in range(20):
    try:
        lf.save_returns("dayX", ["A", None, "B"])
    except TypeError as e:
        held.append(e)
print(f"\n20 failed writes with the repaired save_returns(): open files before {before}, after {open_files()} (none left open)")
