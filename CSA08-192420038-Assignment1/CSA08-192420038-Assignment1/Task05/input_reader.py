"""Task 5 - reading the clerk's entries, validating before converting, and formatted output."""

def is_valid_number(text):
    """True if text is a plain non-negative decimal number such as '8.5' or '12' (after stripping spaces)."""
    t = text.strip()
    return t.replace(".", "", 1).isdigit()          # exactly one optional '.', rest digits

def read_number(prompt, source=input):
    """Keep asking until the clerk types a valid number; return it as float."""
    while True:
        text = source(prompt)
        if is_valid_number(text):
            return float(text)
        print(f"  '{text}' is not a valid number - use digits and a decimal point, e.g. 8.5")

def parse_try_except(text):
    """Alternative: let float() decide; return None if it cannot convert."""
    try:
        return float(text)
    except ValueError:
        return None

if __name__ == "__main__":
    print("input() always returns str, e.g. type of what the clerk types:", type("8.5"))
    for sample in ["8.5", " 8.5 ", "8,5", "eight", "-3", "", "1e3", "nan", "8.5.1"]:
        a = is_valid_number(sample)
        b = parse_try_except(sample)
        print(f"{sample!r:9} string-check={a!s:5}  try/except -> {b!r}")

    # scripted clerk so the program is repeatable; with the keyboard just use read_number("Litres: ")
    answers = iter(["8,5", "eight", " 8.5 "])
    litres = read_number("Litres: ", source=lambda p: next(answers))
    print("accepted litres =", litres)

    # aligned output with f-string width and precision
    print(f"\n{'ID':<6}{'Litres':>8}{'Fat':>6}{'SNF':>6}{'Rate':>9}{'Amount':>10}")
    for fid, l, f, s, r in [("F001", 10, 3.5, 8.5, 30.0), ("F002", 8.5, 4.2, 8.7, 33.4), ("F003", 12, 3.1, 8.3, 27.8)]:
        print(f"{fid:<6}{l:8.1f}{f:6.1f}{s:6.1f}{r:9.2f}{l*r:10.2f}")
