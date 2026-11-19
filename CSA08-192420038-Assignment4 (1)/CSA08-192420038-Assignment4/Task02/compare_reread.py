"""Task 2 alternative: re-read all daily files for each student (O(s*f*l)) versus one pass with a dictionary (O(f*l))."""
import tempfile, time, os, random
from pathlib import Path
from attendance_monthly import process_month, parse_line

random.seed(2)
F = 20
print(f"{'students s':>10} {'files f':>8} {'lines/file l':>13} {'line reads (re-read)':>21} {'line reads (one pass)':>22} {'time re-read s':>15} {'time one pass s':>16}  same")
for s in (50, 100, 200, 400):
    with tempfile.TemporaryDirectory() as tmp:
        regs = [f"19231{i:04d}" for i in range(s)]
        for d in range(F):
            with open(Path(tmp) / f"attendance_2026-10-{d+1:02d}.txt", "w") as fh:
                for r in regs:
                    fh.write(f"{r},2026-10-{d+1:02d},{random.choice('PPPA')}\n")
        files = sorted(Path(tmp).glob("attendance_*.txt"))
        t0 = time.perf_counter(); counts, damaged, _ = process_month(tmp); t_one = time.perf_counter() - t0
        t0 = time.perf_counter(); reads = 0; res = {}
        for r in regs:                                   # for EACH student open and scan EVERY file again
            p = t = 0
            for path in files:
                with open(path) as fh:
                    for line in fh:
                        reads += 1
                        reg, day, st = parse_line(line)
                        if reg == r:
                            t += 1; p += (st == "P")
            res[r] = [p, t]
        t_re = time.perf_counter() - t0
        print(f"{s:>10} {F:>8} {s:>13} {reads:>21,} {F*s:>22,} {t_re:>15.3f} {t_one:>16.4f}  {res == counts}")
