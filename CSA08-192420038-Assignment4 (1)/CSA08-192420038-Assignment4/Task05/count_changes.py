"""Task 5.2 - how many files had to change for the new report (absent 3 consecutive days) in each organisation?"""
import difflib
from pathlib import Path

before, after = Path("before_change"), Path("after_change")
print(f"{'organisation':<18}{'files':>6}{'files changed':>15}{'lines added':>13}{'lines removed':>15}   changed files")
for org in sorted(p.name for p in after.iterdir() if p.is_dir()):
    files = sorted(p for p in (after / org).rglob("*.py"))
    changed, added, removed, names = 0, 0, 0, []
    for new in files:
        old = before / new.relative_to(after)
        a, b = old.read_text().splitlines(), new.read_text().splitlines()
        diff = [d for d in difflib.unified_diff(a, b, lineterm="", n=0) if d[:1] in "+-" and d[:3] not in ("+++", "---")]
        if diff:
            changed += 1; names.append(new.name)
            added += sum(d[0] == "+" for d in diff); removed += sum(d[0] == "-" for d in diff)
    print(f"{org:<18}{len(files):>6}{changed:>15}{added:>13}{removed:>15}   {', '.join(names)}")
