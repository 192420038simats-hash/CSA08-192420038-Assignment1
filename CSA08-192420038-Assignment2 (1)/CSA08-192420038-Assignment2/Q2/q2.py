"""Q2 - OTP attempt loops (K3 Apply)."""
CORRECT = "482913"


def verify_while(entries, security_ok=False):
    """while version. Blank entries are skipped (continue) and not counted.
    A correct security answer raises the limit from 3 to 5 (changed condition)."""
    entries = iter(entries)
    limit = 5 if security_ok else 3
    attempts = 0
    while attempts < limit:
        code = next(entries, None)
        if code is None:                   # keypad timed out: stop asking
            break
        code = code.strip()
        if code == "":
            continue                       # blank: NOT an attempt
        attempts += 1                      # counted only after the blank check
        if code == CORRECT:
            return f"VERIFIED on attempt {attempts}"
        print(f"   wrong OTP ({attempts}/{limit})")
    else:
        return "ACCOUNT LOCKED for 30 minutes"   # loop-else: ran out of attempts
    return "SESSION ENDED (no input)"


def verify_for(entries):
    """for range(3) version; blank entries need an inner while to be re-asked."""
    entries = iter(entries)
    for attempt in range(1, 4):
        code = ""
        while code == "":
            code = next(entries, "?").strip()
        if code == CORRECT:
            return f"VERIFIED on attempt {attempt}"
        if attempt == 3:
            pass                           # placeholder: SMS alert would be sent here
        print(f"   wrong OTP ({attempt}/3)")
    else:
        return "ACCOUNT LOCKED for 30 minutes"


def verify_recursive(entries, attempt=1, limit=3):
    """Recursive alternative: O(a) stack frames."""
    if attempt > limit:
        return "ACCOUNT LOCKED for 30 minutes"
    code = next(entries, "?").strip()
    if code == "":
        return verify_recursive(entries, attempt, limit)
    if code == CORRECT:
        return f"VERIFIED on attempt {attempt}"
    print(f"   wrong OTP ({attempt}/{limit})")
    return verify_recursive(entries, attempt + 1, limit)


def verify_counter_bug(entries):
    """Demonstrates the wrong counter placement: blanks consume attempts."""
    attempts = 0
    for code in entries:
        attempts += 1                      # BUG: incremented before blank check
        if code.strip() == "":
            continue
        if code.strip() == CORRECT:
            return f"VERIFIED on attempt {attempts}"
        if attempts == 3:
            break
    return f"LOCKED after {attempts} entries (blanks wrongly counted)"


if __name__ == "__main__":
    scenarios = {
        "correct on 2nd try": ["111111", CORRECT],
        "blank entries ignored": ["", "  ", "000000", CORRECT],
        "three wrong -> lock": ["1", "2", "3", CORRECT],
    }
    for name, data in scenarios.items():
        print(f"\nScenario: {name}")
        print("  while    :", verify_while(list(data)))
        print("  for      :", verify_for(list(data)))
        print("  recursive:", verify_recursive(iter(data)))

    print("\nChanged condition (security answer correct -> 5 attempts):")
    data = ["1", "2", "3", "4", CORRECT]
    print("  limit 3:", verify_while(list(data)))
    print("  limit 5:", verify_while(list(data), security_ok=True))

    print("\nWrong counter placement demo (blank, blank, wrong, correct):")
    print("  buggy  :", verify_counter_bug(["", "", "9", CORRECT]))
    print("  correct:", verify_while(["", "", "9", CORRECT]))
