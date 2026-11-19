"""Task 3.1 / 3.3 - provoke every failure and record the exception that Python raises."""
import os, subprocess, sys, tempfile
from pathlib import Path
from processor import process_file, parse_line, InvalidRecord, AttendanceFileError

tmp = Path(tempfile.mkdtemp())
good = tmp / "good.txt";   good.write_text("192311001,2026-10-08,P\n192311002,2026-10-08,A\n", encoding="utf-8")
empty = tmp / "empty.txt"; empty.write_text("", encoding="utf-8")
badenc = tmp / "latin1.txt"; badenc.write_bytes("192311001,2026-10-08,P\n192311002,2026-10-08,\xe9\n".encode("latin-1"))
damaged = tmp / "damaged.txt"; damaged.write_text("192311001,2026-10-08,P\n192311003,2026-10-08\n192311004,2026-13-45,P\n192311005,2026-10-08,L\n", encoding="utf-8")
locked = tmp / "locked.txt"; locked.write_text("192311001,2026-10-08,P\n"); os.chmod(locked, 0o000)
os.chmod(tmp, 0o755)

print(f"{'situation':<26}{'what Python raises':<44}{'result of process_file()'}")
def show(label, path):
    try:
        r = process_file(path)
        print(f"{label:<26}{'no exception':<44}{r}")
    except AttendanceFileError as e:
        print(f"{label:<26}{type(e.__cause__).__name__:<44}AttendanceFileError: {e}")

show("good file", good)
show("missing file", tmp / "nope.txt")
show("missing folder", tmp / "nofolder" / "a.txt")
show("path is a folder", tmp)
show("wrong encoding", badenc)
show("damaged lines", damaged)
show("empty file", empty)

# PermissionError: root ignores file permissions, so the check is made by an ordinary user (nobody)
code = f"import sys; sys.path.insert(0, {os.getcwd()!r}); from processor import process_file, AttendanceFileError\n" \
       f"try:\n    process_file({str(locked)!r})\nexcept AttendanceFileError as e:\n    print(f'{{type(e.__cause__).__name__:<44}}AttendanceFileError: {{e}}')\n"
try:
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, user=65534)
    print(f"{'permission denied':<26}{r.stdout.strip() or r.stderr.strip()[-120:]}")
except (PermissionError, OSError) as e:
    print(f"{'permission denied':<26}(could not switch user here: {e}; on your computer use a read-protected file)")

print("\nraise ... from ... keeps the cause:")
try:
    parse_line("192311004,2026-13-45,P")
except InvalidRecord as e:
    print("  InvalidRecord:", e, "| cause:", repr(e.__cause__))

print("\nunsafe index/convert (what the damaged lines would raise without InvalidRecord):")
for text, op in [("192311003,2026-10-08", lambda t: t.split(",")[2]), ("abc,2026-10-08,P", lambda t: int(t.split(",")[0]))]:
    try: op(text)
    except (IndexError, ValueError) as e: print(f"  {text!r:<26}-> {type(e).__name__}: {e}")
