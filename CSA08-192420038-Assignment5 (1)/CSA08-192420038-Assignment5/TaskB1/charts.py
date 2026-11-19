"""B1.4 - the five charts designed in A3.1, drawn from airquality.db. Prints the numbers used in the interpretation."""
import sqlite3, statistics
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
con = sqlite3.connect(HERE / "airquality.db")
names = dict(con.execute("SELECT station_id, name FROM stations"))
daily = con.execute("SELECT station_id, day, AVG(pm25), AVG(temp_c) FROM readings GROUP BY station_id, day ORDER BY day").fetchall()
PM_LIMIT = 60                                     # 24-hour PM2.5 standard (ug/m3)

# 1 line: trend of daily mean PM2.5 over the month
fig, ax = plt.subplots(figsize=(8, 4))
for sid in ("ADY", "GND", "MAN"):
    pts = [(d[1], d[2]) for d in daily if d[0] == sid and d[2] is not None]
    ax.plot([int(p[0][-2:]) for p in pts], [p[1] for p in pts], marker="o", ms=3, label=names[sid])
net = {}
for sid, day, pm, t in daily:
    if pm is not None: net.setdefault(day, []).append(pm)
ax.plot([int(d[-2:]) for d in sorted(net)], [statistics.fmean(net[d]) for d in sorted(net)], "k--", lw=2, label="Network mean")
ax.axhline(PM_LIMIT, color="red", lw=1, ls=":", label="24-h standard (60)")
ax.set_xlabel("Day of October 2026"); ax.set_ylabel("Daily mean PM2.5 (ug/m3)"); ax.set_title("Chart 1 - Trend of daily mean PM2.5, October 2026")
ax.legend(fontsize=8, ncol=2); ax.grid(alpha=.3); fig.tight_layout(); fig.savefig(HERE / "chart1_trend.png", dpi=110); plt.close(fig)
t = [statistics.fmean(net[d]) for d in sorted(net)]
print(f"chart1: network mean ranges {min(t):.1f} to {max(t):.1f} ug/m3; days above 60: {sum(v > 60 for v in t)} of {len(t)}")

# 2 bar: monthly mean per station, sorted
means = sorted(con.execute("SELECT s.name, AVG(r.pm25) FROM readings r JOIN stations s USING (station_id) GROUP BY s.name").fetchall(), key=lambda x: x[1])
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh([m[0] for m in means], [m[1] for m in means], color=["#c0392b" if m[1] > PM_LIMIT else "#2e86c1" for m in means])
ax.axvline(PM_LIMIT, color="k", ls="--", lw=1); ax.set_xlabel("Monthly mean PM2.5 (ug/m3)"); ax.set_title("Chart 2 - Station comparison (red = above 60)")
fig.tight_layout(); fig.savefig(HERE / "chart2_stations.png", dpi=110); plt.close(fig)
print("chart2: highest", means[-1][0], round(means[-1][1], 1), "| lowest", means[0][0], round(means[0][1], 1), "| stations above 60:", sum(m[1] > 60 for m in means))

# 3 scatter: daily mean temperature against daily mean PM2.5
pts = [(d[3], d[2]) for d in daily if d[2] is not None and d[3] is not None]
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=8, alpha=.5)
r = statistics.correlation([p[0] for p in pts], [p[1] for p in pts])
ax.set_xlabel("Daily mean temperature (C)"); ax.set_ylabel("Daily mean PM2.5 (ug/m3)"); ax.set_title(f"Chart 3 - Temperature vs PM2.5 (r = {r:.2f})")
ax.grid(alpha=.3); fig.tight_layout(); fig.savefig(HERE / "chart3_scatter.png", dpi=110); plt.close(fig)
print(f"chart3: {len(pts)} station-days, correlation r = {r:.3f}")

# 4 bar: mean PM2.5 by hour of day (all stations)
hours = con.execute("SELECT hour, AVG(pm25) FROM readings GROUP BY hour ORDER BY hour").fetchall()
worst = sorted(hours, key=lambda h: -h[1])[:3]
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar([h[0] for h in hours], [h[1] for h in hours], color=["#c0392b" if h in worst else "#2e86c1" for h in hours])
ax.set_xlabel("Hour of day"); ax.set_ylabel("Mean PM2.5 (ug/m3)"); ax.set_xticks(range(0, 24, 2)); ax.set_title("Chart 4 - Hours with the worst air (all stations)")
fig.tight_layout(); fig.savefig(HERE / "chart4_hours.png", dpi=110); plt.close(fig)
print("chart4: worst hours", [(h[0], round(h[1], 1)) for h in worst], "| best hour", min(hours, key=lambda h: h[1])[0], round(min(h[1] for h in hours), 1))

# 5 box plot: distribution of hourly PM2.5 per station
data = {names[sid]: [v for (v,) in con.execute("SELECT pm25 FROM readings WHERE station_id = ? AND pm25 IS NOT NULL", (sid,))] for sid in names}
order = sorted(data, key=lambda n: statistics.median(data[n]))
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.boxplot([data[n] for n in order], orientation="vertical", showfliers=True, flierprops={"markersize": 2})
ax.set_xticks(range(1, len(order) + 1)); ax.set_xticklabels(order, rotation=45, ha="right", fontsize=8)
ax.set_ylabel("Hourly PM2.5 (ug/m3)"); ax.set_title("Chart 5 - Spread of hourly PM2.5 by station"); fig.tight_layout(); fig.savefig(HERE / "chart5_boxplot.png", dpi=110); plt.close(fig)
iqr = {n: statistics.quantiles(data[n], n=4)[2] - statistics.quantiles(data[n], n=4)[0] for n in order}
print("chart5: median highest", order[-1], round(statistics.median(data[order[-1]]), 1), "| widest IQR", max(iqr, key=iqr.get), round(max(iqr.values()), 1))
con.close()
