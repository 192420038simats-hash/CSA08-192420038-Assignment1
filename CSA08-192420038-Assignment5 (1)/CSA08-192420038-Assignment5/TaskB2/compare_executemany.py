"""B2 alternative: executemany() versus execute() in a loop - time for n rows, in memory and in a file database."""
import os, sqlite3, tempfile, time

rows = lambda n: [(f"S{i % 12:02d}", "2026-10-01", float(i % 200)) for i in range(n)]
tmp = tempfile.mkdtemp()


def new_db(where):
    path = ":memory:" if where == "memory" else os.path.join(tmp, "t.db")
    if where != "memory" and os.path.exists(path): os.remove(path)
    con = sqlite3.connect(path); con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)"); con.commit()
    return con


print(f"{'rows':>9} | {'database':<8}| {'executemany + 1 commit':>23} {'execute() loop + 1 commit':>26} {'execute() + commit each row':>29}")
for n in (1_000, 10_000, 100_000):
    data = rows(n)
    for where in ("memory", "file"):
        c = new_db(where); t0 = time.perf_counter(); c.executemany("INSERT INTO aq VALUES (?,?,?)", data); c.commit(); t_many = time.perf_counter() - t0; c.close()
        c = new_db(where); t0 = time.perf_counter()
        for r in data: c.execute("INSERT INTO aq VALUES (?,?,?)", r)
        c.commit(); t_loop = time.perf_counter() - t0; c.close()
        if n <= 10_000:
            c = new_db(where); t0 = time.perf_counter()
            for r in data: c.execute("INSERT INTO aq VALUES (?,?,?)", r); c.commit()
            t_each = f"{time.perf_counter() - t0:>27.3f} s"; c.close()
        else:
            t_each = f"{'(not run: too slow)':>29}"
        print(f"{n:>9,} | {where:<8}| {t_many:>21.4f} s {t_loop:>24.4f} s {t_each}")
