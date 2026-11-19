"""A5.2 - rule-based chatbot for citizens. Keywords decide the intent, the database gives the answer (parameterised queries only).
'today' means the latest day stored in the database."""
import difflib, sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "TaskB1" / "airquality.db"
con = sqlite3.connect(DB)
STATIONS = {name.lower(): (sid, name) for sid, name in con.execute("SELECT station_id, name FROM stations")}
LATEST = con.execute("SELECT MAX(day) FROM readings").fetchone()[0]
LEVELS = [(30, "good"), (60, "satisfactory"), (90, "moderate"), (120, "poor"), (250, "very poor"), (1e9, "severe")]   # PM2.5 24-hour bands (ug/m3)


def level(v):
    return next(name for limit, name in LEVELS if v <= limit)


def find_stations(text):
    """Stations named in the text: exact name, otherwise the closest spelling (difflib) of each word pair."""
    t, found = text.lower(), []
    for name, (sid, official) in STATIONS.items():
        if name in t:
            found.append((sid, official))
    if not found:
        words = t.replace("?", " ").replace(",", " ").split()
        grams = words + [" ".join(p) for p in zip(words, words[1:])]
        for g in grams:
            m = difflib.get_close_matches(g, STATIONS, n=1, cutoff=0.8)
            if m and STATIONS[m[0]] not in found:
                found.append(STATIONS[m[0]])
    return found


def latest_mean(sid):
    return con.execute("SELECT AVG(pm25) FROM readings WHERE station_id = ? AND day = ?", (sid, LATEST)).fetchone()[0]


def reply(text):
    t = text.lower()
    st = find_stations(t)
    has = lambda *ws: any(w in t for w in ws)
    if has("help", "what can you"):
        return "I can tell you the PM2.5 of a station today, its monthly average, the most or least polluted station, or list the stations."
    if has("list", "which stations", "all stations"):
        return "Stations: " + ", ".join(sorted(n for _, n in STATIONS.values()))
    if has("worst", "most polluted", "highest", "dirtiest"):
        row = con.execute("SELECT s.name, AVG(r.pm25) m FROM readings r JOIN stations s USING (station_id) WHERE r.day = ? GROUP BY s.name ORDER BY m DESC LIMIT 1", (LATEST,)).fetchone()
        return f"The most polluted station on {LATEST} is {row[0]} with a mean PM2.5 of {row[1]:.1f} ug/m3 ({level(row[1])})."
    if has("best", "cleanest", "lowest", "least polluted"):
        row = con.execute("SELECT s.name, AVG(r.pm25) m FROM readings r JOIN stations s USING (station_id) WHERE r.day = ? GROUP BY s.name ORDER BY m ASC LIMIT 1", (LATEST,)).fetchone()
        return f"The cleanest station on {LATEST} is {row[0]} with a mean PM2.5 of {row[1]:.1f} ug/m3 ({level(row[1])})."
    if has("compare") and len(st) >= 2:
        parts = [f"{n}: {latest_mean(sid):.1f}" for sid, n in st[:2]]
        return f"Mean PM2.5 on {LATEST} (ug/m3) - " + ", ".join(parts) + "."
    if has("pm2.5", "pm25", "pollution", "air", "aqi", "reading"):
        if not st:
            return "Which station do you mean? Try: 'What is the PM2.5 in Adyar today?'"
        sid, name = st[0]
        if has("average", "mean", "month", "october"):
            v = con.execute("SELECT AVG(pm25) FROM readings WHERE station_id = ?", (sid,)).fetchone()[0]
            return f"The average PM2.5 at {name} over the stored month is {v:.1f} ug/m3 ({level(v)})."
        v = latest_mean(sid)
        return f"The mean PM2.5 at {name} on {LATEST} is {v:.1f} ug/m3 - {level(v)}."
    return "Sorry, I did not understand. Type 'help' to see what I can answer."


if __name__ == "__main__":
    questions = [
        "What is the PM2.5 in Adyar today?",
        "pm25 in guindy",
        "What is the average PM2.5 at Manali this month?",
        "How is the air in Adyr?",                                   # spelling mistake
        "Which is the most polluted station today?",
        "compare Adyar and Manali pm2.5",
        "What is the PM2.5 in Mumbai today?",                        # station not in the network
        "Is the air clean in Adyar or not?",                         # keywords found, meaning of the question not understood
        "Will it rain tomorrow?",                                    # outside the topic
        "PM2.5 in Adyar DROP TABLE readings; --",                    # hostile text: handled as plain text
        "help",
    ]
    print(f"(database: latest day = {LATEST})")
    for q in questions:
        print(f"\nuser : {q}\nbot  : {reply(q)}")
    print("\nreadings table still has", con.execute("SELECT COUNT(*) FROM readings").fetchone()[0], "rows")
