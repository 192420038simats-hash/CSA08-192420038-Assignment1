"""The processing flow:  department files -> read -> validate -> remove duplicates -> write outputs."""
from pathlib import Path

from .reader import read_lines
from .validator import validate_line, InvalidRegistration
from .writer import write_master, write_event_files, write_error_log, write_summary


def process_files(data_dir, departments):
    """Read and validate every department file. Never stops because of a bad line or a missing file.
    Returns (students, errors, counters)."""
    students, errors, seen = {}, [], set()               # seen = set of register numbers already accepted
    c = {"files expected": len(departments), "files read": 0, "files missing/unreadable": 0, "lines read": 0,
         "registrations accepted": 0, "duplicates merged": 0, "lines rejected": 0}
    for dept in departments:
        path = Path(data_dir) / f"{dept}.txt"
        try:
            for number, line in read_lines(path):
                c["lines read"] += 1
                try:
                    rec = validate_line(line)                                      # InvalidRegistration if bad
                except InvalidRegistration as e:
                    c["lines rejected"] += 1
                    errors.append((path.name, number, "REJECTED", str(e), line))
                    continue
                if rec["register"] in seen:                                        # O(1) average set look-up
                    old = students[rec["register"]]
                    old["events"] = sorted(set(old["events"]) | set(rec["events"]))
                    c["duplicates merged"] += 1
                    errors.append((path.name, number, "DUPLICATE", f"{rec['register']} already registered; events merged", ""))
                else:
                    seen.add(rec["register"]); students[rec["register"]] = rec
                    c["registrations accepted"] += 1
        except FileNotFoundError:
            c["files missing/unreadable"] += 1
            errors.append((path.name, 0, "MISSING FILE", f"{path} does not exist", ""))
        except (PermissionError, IsADirectoryError):
            c["files missing/unreadable"] += 1
            errors.append((path.name, 0, "UNREADABLE", "no permission or not a file", ""))
        except UnicodeDecodeError as e:
            c["files missing/unreadable"] += 1
            errors.append((path.name, 0, "BAD ENCODING", f"not UTF-8 text (undecodable byte at position {e.start}); file skipped from that point", ""))
        else:
            c["files read"] += 1
    return students, errors, c


def run(data_dir, out_dir, departments):
    """Process the files and write all outputs; returns the counters."""
    students, errors, c = process_files(data_dir, departments)
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    write_master(students, out / "master_list.csv")
    event_counts = write_event_files(students, out / "events")
    dept_counts = {}
    for s in students.values():
        dept_counts[s["department"]] = dept_counts.get(s["department"], 0) + 1
    write_error_log(errors, out / "error_log.txt")
    stats = [(k.capitalize(), v) for k, v in c.items()] + [("Students in master list", len(students))]
    write_summary(stats, event_counts, dept_counts, out / "summary_report.txt")
    return c, len(students), event_counts
