"""Q7 - Merge phone contacts from several sources so that each person appears once.

Contact = {"name": str, "numbers": [str, ...], "emails": [str, ...]}  (any field may be missing)
Rule: two contacts are the same person if they share at least one normalised number or e-mail address
      (directly or through a chain of contacts). Names are NOT used to match (two people can share a name)."""

TITLES = {"dr", "mr", "mrs", "ms", "prof", "shri", "smt"}


def normalise_number(raw):
    """Return the 10-digit Indian number as text, or None if it cannot be a mobile/landline number.
    '+91 98400 12345', '9840012345', '098400 12345', '+91-98400-12345' -> '9840012345'."""
    digits = "".join(ch for ch in raw if ch.isdigit())
    if len(digits) > 10 and digits.startswith("91"):
        digits = digits[2:]
    if len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]
    return digits if len(digits) == 10 else None


def normalise_name(raw):
    """Lower case, no punctuation, no titles, single spaces: 'Dr. Ravi' -> 'ravi'."""
    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in raw)
    return " ".join(w for w in cleaned.split() if w not in TITLES)


def normalise_email(raw):
    return raw.strip().lower()


def merge_contacts(contacts):
    """Group contacts with a dictionary of identifiers (union-find over numbers and e-mails): O(n) on average.
    Returns a list of {"name", "names": set, "numbers": set, "emails": set}."""
    parent = {}

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:                      # path compression
            parent[x], x = root, parent[x]
        return root

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    keyed = []
    for c in contacts:
        nums = [n for n in (normalise_number(x) for x in c.get("numbers", [])) if n]
        mails = [normalise_email(e) for e in c.get("emails", []) if e.strip()]
        keys = [("n", n) for n in nums] + [("e", e) for e in mails]
        for k in keys:
            parent.setdefault(k, k)
        for k in keys[1:]:
            union(keys[0], k)
        keyed.append((c, nums, mails, keys))

    groups = {}
    for c, nums, mails, keys in keyed:
        name = c.get("name", "").strip()
        root = find(keys[0]) if keys else ("name", normalise_name(name) or id(c))   # no identifier: only identical names collapse
        rec = groups.setdefault(root, {"names": set(), "numbers": set(), "emails": set()})
        if name:
            rec["names"].add(name)
        rec["numbers"].update(nums)
        rec["emails"].update(mails)
    out = []
    for rec in groups.values():
        rec["name"] = max(rec["names"], key=lambda s: (len(normalise_name(s)), s)) if rec["names"] else "(no name)"
        out.append(rec)
    return sorted(out, key=lambda r: normalise_name(r["name"]))


def merge_pairwise(contacts):
    """Alternative: compare every pair of contacts. O(n^2) comparisons."""
    ids = []
    for c in contacts:
        nums = {normalise_number(x) for x in c.get("numbers", [])} - {None}
        mails = {normalise_email(e) for e in c.get("emails", []) if e.strip()}
        ids.append(nums | mails)
    n = len(contacts)
    group = list(range(n))

    def find(i):
        while group[i] != i:
            group[i] = group[group[i]]; i = group[i]
        return i

    for i in range(n):
        for j in range(i + 1, n):
            if ids[i] and not ids[i].isdisjoint(ids[j]):
                group[find(j)] = find(i)
    merged = {}
    for i, c in enumerate(contacts):
        merged.setdefault(find(i), []).append(i)
    return merged


def show(records):
    for r in records:
        print(f"  {r['name']:<14} names={sorted(r['names'])}  numbers={sorted(r['numbers'])}  emails={sorted(r['emails'])}")
