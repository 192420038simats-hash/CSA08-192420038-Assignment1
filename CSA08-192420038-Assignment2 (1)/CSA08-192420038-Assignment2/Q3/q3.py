"""Q3 - Vehicle registration number validator (K4 Analyse). No regular expressions."""


def normalise(text):
    """'tn 09 ab 1234' -> 'TN09AB1234' (spaces and hyphens removed, upper case)."""
    return text.replace(" ", "").replace("-", "").upper()


def is_valid(reg):
    """Valid form: 2 letters, 2 digits, 1 or 2 letters, 4 digits (e.g. TN09AB1234)."""
    if len(reg) not in (9, 10):
        return False
    series_len = len(reg) - 8                      # 1 or 2 letters
    state = reg[:2]
    district = reg[2:4]
    series = reg[4:4 + series_len]
    number = reg[-4:]
    return (state.isalpha() and district.isdigit()
            and series.isalpha() and number.isdigit())


def format_reg(reg):
    """Receipt format, e.g. 'TN 09 AB 1234' (valid numbers only)."""
    return " ".join([reg[:2], reg[2:4], reg[4:-4], reg[-4:]])


if __name__ == "__main__":
    print("--- Assignment program ---")
    for raw in ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]:
        reg = normalise(raw)
        print(f"{raw:15} -> {reg:11} {'valid' if is_valid(reg) else 'INVALID'}")

    print("\n--- Six designed inputs: prediction vs observed + receipt format ---")
    tests = [("tn 09 ab 1234", True), ("KA-01-M-0007", True), ("Tn09Ab1234", True),
             ("TN9AB1234", False), ("TN 22 1234 AB", False), ("TN-09-ABC-1234", False)]
    for raw, expected in tests:
        reg = normalise(raw)
        got = is_valid(reg)
        receipt = format_reg(reg) if got else "-"
        print(f"{raw:16} -> {reg:12} predicted={str(expected):5} observed={str(got):5} "
              f"{'PASS' if got == expected else 'FAIL'}  receipt: {receipt}")

    print("\n--- Slicing inquiry ---")
    for s in ("TN09A1234", "TN09AB1234"):
        print(f"len={len(s):2} s={s}  s[-4:]={s[-4:]!r}  s[4:-4]={s[4:-4]!r}")

    print("\n--- Immutability ---")
    text = "tn 09"
    result = text.upper()
    print(f"text={text!r}  text.upper()={result!r}  text after call={text!r}")
    try:
        text[0] = "T"
    except TypeError as e:
        print("text[0] = 'T' ->", type(e).__name__ + ":", e)

    print("\n--- Alternative: regular expression ---")
    import re
    pattern = r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}"
    agree = all((re.fullmatch(pattern, normalise(r)) is not None) == is_valid(normalise(r))
                for r, _ in tests)
    print("regex and slicing agree on all six inputs:", agree)
