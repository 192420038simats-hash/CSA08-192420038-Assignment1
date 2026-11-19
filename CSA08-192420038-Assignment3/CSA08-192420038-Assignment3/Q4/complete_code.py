"""Q4 - Complete the Code (TODO 1 done with set operators only) and the same with set methods."""
ai_elective = {"192311001", "192311004", "192311007", "192311009"}
iot_elective = {"192311002", "192311004", "192311009", "192311010"}
all_students = {f"1923110{i:02d}" for i in range(1, 11)}

# TODO 1 done: set operators only
both = ai_elective & iot_elective
exactly_one = ai_elective ^ iot_elective
neither = all_students - (ai_elective | iot_elective)

print("clash      :", sorted(both))
print("exactly one:", sorted(exactly_one))
print("neither    :", sorted(neither))

# Same with set methods - results must be identical
both2 = ai_elective.intersection(iot_elective)
exactly_one2 = ai_elective.symmetric_difference(iot_elective)
neither2 = all_students.difference(ai_elective.union(iot_elective))
print("\nset methods give the same results:", both == both2, exactly_one == exactly_one2, neither == neither2)

# Sets cannot hold lists, but can hold tuples
try:
    {["192311001", "A"]}
except TypeError as e:
    print("set of a list  -> TypeError:", e)
print("set of a tuple ->", {("192311001", "A")})
