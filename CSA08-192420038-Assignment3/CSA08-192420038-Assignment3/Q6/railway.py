"""Q6 - Railway timetable as nested data.
timetable[train_no] = {"name": str, "stops": [(station, arrival, departure), ...], "days": {"Mon", ...}}
Times are "HH:MM" strings (24 h), which sort correctly as text."""

DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
ALL = set(DAYS)

timetable = {
    "12624": {"name": "Chennai Mail", "stops": [("Chennai Central", "--", "20:15"), ("Katpadi", "22:05", "22:10"), ("Bengaluru", "01:30", "01:40"), ("Mysuru", "05:00", "--")], "days": set(ALL)},
    "12007": {"name": "Shatabdi Express", "stops": [("Chennai Central", "--", "06:00"), ("Katpadi", "07:35", "07:37"), ("Bengaluru", "11:00", "11:10"), ("Mysuru", "12:30", "--")], "days": ALL - {"Tue"}},
    "16021": {"name": "Kaveri Express", "stops": [("Mysuru", "--", "13:15"), ("Bengaluru", "15:45", "15:55"), ("Katpadi", "19:10", "19:15"), ("Chennai Central", "21:30", "--")], "days": {"Mon", "Wed", "Fri", "Sun"}},
    "12639": {"name": "Brindavan Express", "stops": [("Chennai Central", "--", "07:40"), ("Katpadi", "09:20", "09:22"), ("Bengaluru", "12:40", "--")], "days": ALL},
    "12608": {"name": "Lalbagh Express", "stops": [("Chennai Central", "--", "15:30"), ("Katpadi", "17:12", "17:14"), ("Bengaluru", "21:05", "--")], "days": {"Mon", "Tue", "Thu", "Sat"}},
}


def trains_at(station, day, tt):
    """Train numbers that stop at `station` on `day` (scans every train and every stop)."""
    return [no for no, t in tt.items() if day in t["days"] and any(s[0] == station for s in t["stops"])]


def departure_at(train_no, station, tt):
    """Departure time from `station` for the train, or None."""
    for s in tt[train_no]["stops"]:
        if s[0] == station:
            return s[2]
    return None


def sorted_by_departure(station, day, tt):
    """Trains at station on day sorted by departure time; arrival-only stops ('--') sort last."""
    nos = trains_at(station, day, tt)
    key = lambda no: (departure_at(no, station, tt) in (None, "--"), departure_at(no, station, tt) or "99:99")
    return sorted(nos, key=key)


def print_timetable(tt):
    print(f"{'Train':<7}{'Name':<20}{'Station':<18}{'Arr':>6}{'Dep':>7}   Days")
    for no, t in tt.items():
        days = ",".join(d for d in DAYS if d in t["days"])
        for i, (st, arr, dep) in enumerate(t["stops"]):
            print(f"{no if i == 0 else '':<7}{t['name'] if i == 0 else '':<20}{st:<18}{arr:>6}{dep:>7}   {days if i == 0 else ''}")
        print()


def build_index(tt):
    """station -> list of train numbers that stop there (built once)."""
    index = {}
    for no, t in tt.items():
        for st, _, _ in t["stops"]:
            index.setdefault(st, []).append(no)
    return index


def trains_at_indexed(station, day, tt, index):
    """Only the trains in index[station] are examined."""
    return [no for no in index.get(station, []) if day in tt[no]["days"]]


if __name__ == "__main__":
    print_timetable(timetable)
    print("Departure time of the third station of train 12624 :", timetable["12624"]["stops"][2][2],
          " (expression: timetable['12624']['stops'][2][2])")
    print("\nTrains stopping at Katpadi on Tue (scan):", trains_at("Katpadi", "Tue", timetable))
    print("Sorted by departure from Katpadi on Tue :", sorted_by_departure("Katpadi", "Tue", timetable))
    for no in sorted_by_departure("Katpadi", "Tue", timetable):
        print(f"   {departure_at(no, 'Katpadi', timetable)}  {no}  {timetable[no]['name']}")
    index = build_index(timetable)
    print("\nindex:", index)
    print("with index, Katpadi on Tue:", trains_at_indexed("Katpadi", "Tue", timetable, index))
    print("\nEdge cases")
    print("  unknown station         :", trains_at("Atlantis", "Mon", timetable), trains_at_indexed("Atlantis", "Mon", timetable, index))
    print("  train not running on day:", "12007" in trains_at("Katpadi", "Tue", timetable), "(12007 does not run on Tue)")
    print("  Mysuru on Mon sorted    :", sorted_by_departure("Mysuru", "Mon", timetable), "(16021 departs 13:15; 12624 and 12007 only arrive)")
