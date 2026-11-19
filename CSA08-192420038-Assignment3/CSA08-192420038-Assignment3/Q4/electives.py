"""Q4 - Elective registration: duplicates, clash detection, reports, edge cases, hand-verified small case."""

def clean(register_numbers):
    """Remove duplicate registrations (a set keeps one copy of each)."""
    return set(register_numbers)

def report(a, b, everyone):
    return {
        "union (registered in at least one)": sorted(a | b),
        "intersection (clash)": sorted(a & b),
        "only first": sorted(a - b),
        "only second": sorted(b - a),
        "symmetric difference (exactly one)": sorted(a ^ b),
        "not registered": sorted(everyone - (a | b)),
    }

if __name__ == "__main__":
    # raw registrations with duplicates (a student pressed submit twice)
    ai_raw = ["S1", "S2", "S3", "S2", "S5", "S1"]
    iot_raw = ["S3", "S4", "S5", "S5", "S6"]
    everyone = {"S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"}
    ai, iot = clean(ai_raw), clean(iot_raw)
    print("duplicates removed:", len(ai_raw), "->", len(ai), "and", len(iot_raw), "->", len(iot))
    expected = {                                  # worked out by hand on paper
        "union (registered in at least one)": ["S1", "S2", "S3", "S4", "S5", "S6"],
        "intersection (clash)": ["S3", "S5"],
        "only first": ["S1", "S2"],
        "only second": ["S4", "S6"],
        "symmetric difference (exactly one)": ["S1", "S2", "S4", "S6"],
        "not registered": ["S7", "S8"],
    }
    got = report(ai, iot, everyone)
    print(f"\n{'result':<38}{'by hand':<30}{'program':<30}ok")
    for k in expected:
        print(f"{k:<38}{str(expected[k]):<30}{str(got[k]):<30}{expected[k] == got[k]}")
        assert expected[k] == got[k]

    print("\nEdge cases")
    print("  empty electives   :", report(set(), set(), everyone)["intersection (clash)"], report(set(), set(), everyone)["not registered"][:3], "...")
    same = {"S1", "S2", "S3"}
    r = report(same, same, everyone)
    print("  identical electives: clash", r["intersection (clash)"], " exactly one", r["symmetric difference (exactly one)"], " only first", r["only first"])
    print("  one empty          :", report({"S1"}, set(), everyone)["only first"], report({"S1"}, set(), everyone)["intersection (clash)"])
