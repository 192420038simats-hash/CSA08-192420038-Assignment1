"""The hostel office's ORIGINAL script, unchanged except that the Windows path is replaced by the sample file
so that it can run here. Everything else is exactly as given."""
f = open("mess_oct.txt")
data = f.read()
total = 0
report = ""
for line in data.split("\n"):
    try:
        parts = line.split(",")
        total = total + int(parts[2])
        report = report + parts[1] + " " + parts[2] + "\n"
    except:
        pass
print(report)
print("Total", total)
