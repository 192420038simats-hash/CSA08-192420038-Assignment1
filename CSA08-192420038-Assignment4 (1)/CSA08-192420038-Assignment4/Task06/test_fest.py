"""Task 6 Stage 5 - demonstration and tests: clean files, duplicate, invalid e-mail, damaged line, missing file."""
import tempfile, os
from pathlib import Path
from fest.validator import valid_email, validate_line, InvalidRegistration, clean_events
from fest.pipeline import process_files, run

print("1. e-mail validation with string methods")
cases = {"anitha@college.edu": True, "a.b-c@dept.college.ac.in": True, "chitra@college": False, "farook@@college.edu": False,
         "jayanth p@college.edu": False, "@college.edu": False, "x@.edu": False, "x@college.": False, "x@col..edu": False,
         "x@college.e": False, "x@college.123": False, "": False}
for e, expected in cases.items():
    got = valid_email(e)
    assert got == expected, e
    print(f"   {e!r:<28} -> {got}")

print("\n2. line validation")
assert validate_line("192311001,Anitha K,cse,Anitha@College.edu,quiz; DANCE ;quiz")["events"] == ["Dance", "Quiz"]
for bad, why in [("1,2,3", "5 fields"), ("19231100,A,CSE,a@b.co,Quiz", "register number"), ("192311001, ,CSE,a@b.co,Quiz", "name is empty"),
                 ("192311001,A,CSE,a@b.co,;;", "no event")]:
    try:
        validate_line(bad); raise SystemExit("should have failed: " + bad)
    except InvalidRegistration as e:
        assert why in str(e), (bad, str(e)); print(f"   {bad!r:<36} -> InvalidRegistration: {e}")

print("\n3. clean files (no errors at all)")
tmp = Path(tempfile.mkdtemp())
(tmp / "cse.txt").write_text("192311001,Anitha K,CSE,anitha@college.edu,Dance\n192311002,Bala M,CSE,bala@college.edu,Quiz;Dance\n")
(tmp / "ece.txt").write_text("192312001,Eswari M,ECE,eswari@college.edu,Music\n")
students, errors, c = process_files(tmp, ["cse", "ece"])
assert len(students) == 3 and errors == [] and c["lines rejected"] == 0
print("   students:", len(students), " errors:", errors)

print("\n4. the five sample files: duplicate, invalid e-mails, damaged line, bad register number, missing file")
students, errors, c = process_files("data", ["cse", "ece", "mech", "civil", "it"])
kinds = [e[2] for e in errors]
expected = {"students": 7, "REJECTED": 6, "DUPLICATE": 1, "MISSING FILE": 1}
assert len(students) == 7 and kinds.count("REJECTED") == 6 and kinds.count("DUPLICATE") == 1 and kinds.count("MISSING FILE") == 1
assert students["192311001"]["events"] == ["Dance", "Music", "Quiz"]          # events of the duplicate registration were merged
assert "192311003" not in students and "192312003" not in students            # invalid e-mail / damaged line are not in the master list
print("   accepted 7, rejected 6, duplicate merged 1, missing file 1 -> all as calculated by hand")

print("\n5. every file missing / wrong encoding / folder instead of file: the program still finishes")
students, errors, c = process_files(tmp / "nowhere", ["cse", "ece"])
print("   no data folder  ->", c["files missing/unreadable"], "files reported missing, students:", len(students))
(tmp / "bad.txt").write_bytes(b"192311001,Anitha K,CSE,anitha@college.edu,Dance\n\xff\xfe\n")
(tmp / "folder.txt").mkdir()
students, errors, c = process_files(tmp, ["bad", "folder"])
print("   wrong encoding / folder ->", [(e[0], e[2]) for e in errors], "| program finished, students:", len(students))
assert c["files missing/unreadable"] == 2

print("\n6. empty folder of outputs is created and written")
c, n, ev = run("data", tmp / "out", ["cse", "ece", "mech", "civil", "it"])
assert (tmp / "out" / "master_list.csv").exists() and (tmp / "out" / "events" / "Music.txt").exists()
print("   outputs:", sorted(p.name for p in (tmp / "out").iterdir()))
print("\nAll tests passed.")
