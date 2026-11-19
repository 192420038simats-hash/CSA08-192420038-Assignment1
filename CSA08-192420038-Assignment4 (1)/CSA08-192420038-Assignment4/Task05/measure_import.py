"""Task 5 alternative: one-time import cost, memory and the size of each organisation (after the change)."""
import subprocess, sys, statistics, time, importlib
from pathlib import Path

orgs = {
    "a single script": ("a_single_script", "import attendance_all"),
    "b one module": ("b_one_module", "import attendance_lib"),
    "c three modules": ("c_three_modules", "import reader, stats, report"),
    "d package": ("d_package", "import attendance.reader, attendance.stats, attendance.report"),
}
print(f"{'organisation':<18}{'files':>6}{'lines':>7}{'first import (fresh process)':>31}{'import again (cached)':>24}{'memory after import':>21}")
for name, (folder, stmt) in orgs.items():
    d = Path("after_change") / folder
    pyfiles = [p for p in d.rglob("*.py") if not p.name.startswith("main_")]
    lines = sum(len(p.read_text().splitlines()) for p in pyfiles)
    code = (f"import sys, time, tracemalloc, decimal, pathlib; sys.path.insert(0, {str(d)!r}); tracemalloc.start(); t=time.perf_counter(); {stmt}; "
            f"first=time.perf_counter()-t; t=time.perf_counter(); {stmt}; again=time.perf_counter()-t; "
            f"print(first*1e6, again*1e6, tracemalloc.get_traced_memory()[0])")
    firsts, agains, mems = [], [], []
    for _ in range(15):
        out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True).stdout.split()
        firsts.append(float(out[0])); agains.append(float(out[1])); mems.append(float(out[2]))
    print(f"{name:<18}{len(pyfiles):>6}{lines:>7}{statistics.median(firsts):>27.0f} us{statistics.median(agains):>20.2f} us{statistics.median(mems)/1024:>17.1f} KiB")
print("\n(decimal and pathlib are imported before the timing starts, so only the project's own modules are measured; median of 15 fresh runs; 'cached' = the second import statement in the same process: modules are found in sys.modules)")
