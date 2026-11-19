"""B2 - a station name containing a quote, and an injection attempt: SQL built with + / f-string versus a ? placeholder."""
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
con.executemany("INSERT INTO aq VALUES (?,?,?)", [("Adyar", "2026-10-01", 48.0), ("Guindy", "2026-10-01", 95.0), ("O'Brien Road", "2026-10-01", 70.0), ("Manali", "2026-10-01", 120.0)])


def by_concatenation(name):
    return con.execute("SELECT station, pm25 FROM aq WHERE station = '" + name + "'").fetchall()


def by_fstring(name):
    return con.execute(f"SELECT station, pm25 FROM aq WHERE station = '{name}'").fetchall()


def by_placeholder(name):
    return con.execute("SELECT station, pm25 FROM aq WHERE station = ?", (name,)).fetchall()


tests = [("normal name", "Adyar"), ("name with a quote", "O'Brien Road"), ("injection", "Adyar' OR '1'='1"), ("injection with UNION", "x' UNION SELECT name, 0 FROM sqlite_master --")]
print(f"{'input':<22}{'string joined with +':<62}{'? placeholder'}")
for label, name in tests:
    try:
        a = by_concatenation(name)
    except sqlite3.Error as e:
        a = f"{type(e).__name__}: {e}"
    b = by_placeholder(name)
    print(f"{label:<22}{str(a)[:60]:<62}{b}")
try:
    by_fstring("Adyar' OR '1'='1")
    print("\nf-string version with the injection returns every row (same as +)")
except sqlite3.Error as e:
    print(e)
print("\nA statement that DELETES data (sqlite3 refuses to run two statements in execute(), but older drivers do not):")
try:
    con.execute("SELECT * FROM aq WHERE station = '" + "x'; DROP TABLE aq; --" + "'")
except sqlite3.Error as e:
    print("  ", type(e).__name__ + ":", e)
print("table still exists:", con.execute("SELECT COUNT(*) FROM aq").fetchone()[0], "rows")
