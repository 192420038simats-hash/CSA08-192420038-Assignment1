"""Writing the four kinds of output."""
import csv
from pathlib import Path


def write_master(students, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["register", "name", "department", "email", "events"])
        for s in sorted(students.values(), key=lambda s: s["register"]):
            w.writerow([s["register"], s["name"], s["department"], s["email"], ";".join(s["events"])])


def write_event_files(students, folder):
    """One file per event: its participants sorted by register number. Returns {event: count}."""
    folder = Path(folder); folder.mkdir(parents=True, exist_ok=True)
    by_event = {}
    for s in sorted(students.values(), key=lambda s: s["register"]):
        for e in s["events"]:
            by_event.setdefault(e, []).append(s)
    for event, people in by_event.items():
        with open(folder / f"{event.replace(' ', '_')}.txt", "w", encoding="utf-8") as f:
            f.write(f"{event} - {len(people)} participants\n")
            for s in people:
                f.write(f"{s['register']}  {s['name']}  ({s['department']})\n")
    return {e: len(p) for e, p in sorted(by_event.items())}


def write_error_log(errors, path):
    with open(path, "w", encoding="utf-8") as f:
        for source, number, kind, message, text in errors:
            where = source if number == 0 else f"{source}:{number}"
            f.write(f"{where}: {kind}: {message}" + (f"  [{text}]" if text else "") + "\n")


def write_summary(stats, event_counts, dept_counts, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("FEST REGISTRATION SUMMARY\n=========================\n")
        for label, value in stats:
            f.write(f"{label:<34}{value:>5}\n")
        f.write("\nParticipants per event\n")
        for e, c in event_counts.items():
            f.write(f"  {e:<20}{c:>4}\n")
        f.write("\nStudents per department\n")
        for d, c in sorted(dept_counts.items()):
            f.write(f"  {d:<20}{c:>4}\n")
