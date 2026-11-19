"""Q7 - tests: formats, duplicates, missing fields, transitive links, same name different people, hand-merged case."""
from contacts import *

phone1 = [{"name": "Dr. Ravi", "numbers": ["+91 98400 12345"], "emails": ["Ravi@x.com"]},
          {"name": "Meena", "numbers": ["98410 55555"]}]
phone2 = [{"name": "ravi kumar", "numbers": ["9840012345", "9444411111"]}]
sim = [{"name": "RAVI K", "numbers": ["098400 12345", "044-2345 6789"]},
       {"name": "R Kumar", "numbers": ["+91 94444 11111"]},
       {"name": "Meena S", "numbers": ["+91-98410-55555"], "emails": ["meena@y.com"]},
       {"name": "Arun", "numbers": ["98765 43210"]},
       {"name": "Arun", "numbers": ["9123456789"]},
       {"name": "Kumar Stores", "emails": ["shop@z.com"]},
       {"name": "NoInfo"}]
allc = phone1 + phone2 + sim
print("number formats ->", [normalise_number(x) for x in ["+91 98400 12345", "9840012345", "098400 12345", "+91-98400-12345", "044-2345 6789", "12345", "abc"]])
print("name formats   ->", [normalise_name(x) for x in ["Dr. Ravi", "ravi kumar", "  RAVI   K. ", "Mrs. S. Meena"]])

merged = merge_contacts(allc)
print(f"\n{len(allc)} contacts in -> {len(merged)} people out")
show(merged)

# worked out by hand on paper
expected = {
    "Ravi": ({"Dr. Ravi", "ravi kumar", "RAVI K", "R Kumar"}, {"9840012345", "9444411111", "4423456789"}, {"ravi@x.com"}),
    "Meena": ({"Meena", "Meena S"}, {"9841055555"}, {"meena@y.com"}),
}
by_first = {}
for r in merged:
    by_first.setdefault(normalise_name(r["name"]).split()[0] if normalise_name(r["name"]) else "", []).append(r)
ravi = [r for r in merged if "9840012345" in r["numbers"]][0]
meena = [r for r in merged if "9841055555" in r["numbers"]][0]
assert ravi["names"] == expected["Ravi"][0] and ravi["numbers"] == expected["Ravi"][1] and ravi["emails"] == expected["Ravi"][2]
assert meena["names"] == expected["Meena"][0] and meena["numbers"] == expected["Meena"][1] and meena["emails"] == expected["Meena"][2]
arun = [r for r in merged if r["name"] == "Arun"]
assert len(arun) == 2, "two different people named Arun must stay separate"
assert any(r["emails"] == {"shop@z.com"} and not r["numbers"] for r in merged)       # e-mail only contact
assert any(r["name"] == "NoInfo" and not r["numbers"] and not r["emails"] for r in merged)   # name only contact
assert len(merged) == 6
print("\nhand-merged expectation (6 people) matches: True")

# the pairwise method must find the same number of people, with the same group sizes
pw = merge_pairwise(allc)
assert len(pw) == len(merged) == 6
assert sorted(len(v) for v in pw.values()) == [1, 1, 1, 1, 2, 4] or sorted(len(v) for v in pw.values()) == [1, 1, 1, 1, 2, 4]
print("pairwise method finds the same 6 groups, sizes", sorted(len(v) for v in pw.values()))

print("\nEdge cases")
print("  empty list          ->", merge_contacts([]))
print("  duplicate contacts  ->", len(merge_contacts([{"name": "A", "numbers": ["9876543210"]}] * 5)), "person")
print("  invalid number only ->", len(merge_contacts([{"name": "B", "numbers": ["12345"]}, {"name": "C", "numbers": ["12345"]}])), "people (invalid numbers are not used to match)")
print("  same name no id     ->", len(merge_contacts([{"name": "Dr. Ravi"}, {"name": "ravi"}])), "person (identical normalised names collapse)")
print("  shared family phone ->", len(merge_contacts([{"name": "Ravi", "numbers": ["9840012345"]}, {"name": "Latha", "numbers": ["9840012345"]}])), "person  <- limitation: shared number merges two people")
