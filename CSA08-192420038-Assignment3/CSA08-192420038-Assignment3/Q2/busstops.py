"""Q2 - City bus-stop map: tuples as keys, zone grid, aliasing, shallow and deep copy, unpacking."""
import copy

stops = {
    (13.0827, 80.2707): "Chennai Central",
    (13.0418, 80.2341): "T. Nagar",
    (13.0674, 80.2376): "Anna Nagar",
}
print("lookup by tuple key:", stops[(13.0674, 80.2376)])

print("\nUnpacking tuples in a for loop")
for (lat, lon), name in stops.items():
    print(f"  {name:<16} lat {lat:.4f}  lon {lon:.4f}")

# ----- grid bug and fix -----
rows, cols = 3, 3
bad = [[0] * cols] * rows
good = [[0] * cols for _ in range(rows)]
bad[1][2] += 5
good[1][2] += 5
print("\nbad grid after bad[1][2] += 5 :", bad)
print("good grid after good[1][2] += 5:", good)
print("rows of bad  share one object? ", bad[0] is bad[1] is bad[2], " ids:", [id(r) % 100000 for r in bad])
print("rows of good share one object? ", good[0] is good[1], " ids:", [id(r) % 100000 for r in good])

# ----- aliasing, shallow, deep -----
original = [[1, 2], [3, 4]]
alias = original
shallow1 = original[:]
shallow2 = copy.copy(original)
deep = copy.deepcopy(original)
original[0][0] = 99            # change an INNER list
original.append([5, 6])        # change the OUTER list
print("\noriginal :", original)
print("alias    :", alias,    " same object:", alias is original)
print("slice [:]:", shallow1, " outer new:", shallow1 is not original, " inner shared:", shallow1[0] is original[0])
print("copy.copy:", shallow2, " inner shared:", shallow2[0] is original[0])
print("deepcopy :", deep,     " inner shared:", deep[0] is original[0])

# ----- function that changes its list argument -----
def add_stop(route, stop):
    route.append(stop)                 # mutates the caller's list

def add_stop_safe(route, stop):
    return route + [stop]              # builds a new list

route = ["A", "B"]
add_stop(route, "C");       print("\nafter add_stop      :", route)
new = add_stop_safe(route, "D"); print("after add_stop_safe :", route, "-> new list", new)

# ----- list inside a tuple -----
t = ([1, 2], 3)
try:
    t[0] = [9]
except TypeError as e:
    print("\nreplace item of tuple  ->", "TypeError:", e)
t[0].append(99)
print("append to list inside tuple -> allowed:", t, "(the tuple still holds the same list object)")
try:
    hash(t)
except TypeError as e:
    print("hash(tuple containing a list) ->", "TypeError:", e)
print("hash((1, 2)) works:", hash((1, 2)) is not None)
