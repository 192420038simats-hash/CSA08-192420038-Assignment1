"""Task 6 - the calculation divided into small functions (rates are module-level constants, only READ inside)."""
BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30
STD_FAT, STD_SNF, STEP = 3.5, 8.5, 0.1


def steps(value, standard):
    """Return the whole number of 0.1 % steps of value above (+) or below (-) standard."""
    return round((value - standard) / STEP)


def rate_per_litre(fat, snf):
    """Return the price per litre (Rs, 2 decimals) for the given fat % and SNF %."""
    return round(BASE_RATE + steps(fat, STD_FAT) * FAT_STEP_VALUE + steps(snf, STD_SNF) * SNF_STEP_VALUE, 2)


def payout(litres, fat, snf):
    """Return the amount payable (Rs, 2 decimals) for one entry. Returns, does not print."""
    return round(litres * rate_per_litre(fat, snf), 2)


def ten_day_total(entries):
    """Return the total payable for a list of (litres, fat, snf) tuples."""
    total = 0.0
    for litres, fat, snf in entries:
        total += payout(litres, fat, snf)
    return round(total, 2)


def show_entry(litres, fat, snf):
    """Print one entry (prints, returns None) - shows the difference between print and return."""
    print(f"{litres:6.1f} L  fat {fat}  snf {snf}  -> Rs {payout(litres, fat, snf):8.2f}")


if __name__ == "__main__":
    entries = [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]
    for e in entries:
        show_entry(*e)
    print("ten-day total:", ten_day_total(entries))

    # return vs print
    r = show_entry(1, 3.5, 8.5)
    print("value returned by show_entry:", r)           # None

    # local vs global
    def wrong():
        BASE_RATE = 99                                   # creates a LOCAL name, global is untouched
        return BASE_RATE
    print("local BASE_RATE:", wrong(), "global BASE_RATE:", BASE_RATE)
    def reads_only():
        return BASE_RATE * 2                             # reading a global is fine
    print("reading global:", reads_only())
    def bad():
        try:
            BASE_RATE += 1                               # assignment makes it local -> UnboundLocalError
        except UnboundLocalError as e:
            return "UnboundLocalError: " + str(e)
    print(bad())
