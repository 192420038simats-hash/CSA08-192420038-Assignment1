"""Task 1.2 - repaired mess-bill totaliser: with statement, line-by-line reading, specific exceptions,
list of rejected lines, file name as a parameter, exact (Decimal) money."""
import sys
from decimal import Decimal, InvalidOperation


def parse_bill(line):
    """'192311001,Anitha K,1250.50' -> ('192311001', 'Anitha K', Decimal('1250.50')).
    Raises ValueError with a reason if the line is not valid."""
    try:
        register, rest = line.split(",", 1)        # register number is before the FIRST comma
        name, amount_text = rest.rsplit(",", 1)    # names may contain commas, the amount is after the LAST comma
    except ValueError:                             # unpacking fails when a comma is missing
        raise ValueError("expected register,name,amount") from None
    name = name.strip().strip('"')
    try:
        amount = Decimal(amount_text.strip())
    except InvalidOperation:
        raise ValueError(f"amount '{amount_text.strip()}' is not a number") from None
    if not amount.is_finite() or amount < 0:
        raise ValueError(f"amount {amount} must be zero or more")
    if not register.strip().isdigit():
        raise ValueError(f"register number '{register.strip()}' is not numeric")
    return register.strip(), name, amount


def total_mess_bills(path):
    """Return (report_lines, total, rejected). rejected = [(line_number, line_text, reason), ...].
    Blank lines are ignored (they are not data); every other bad line is recorded, never silently dropped."""
    report_lines, rejected, total = [], [], Decimal("0")
    with open(path, encoding="utf-8") as f:                    # closed automatically, even after an error
        for number, line in enumerate(f, start=1):             # one line in memory at a time
            line = line.rstrip("\r\n")
            if not line.strip():
                continue
            try:
                register, name, amount = parse_bill(line)
            except ValueError as e:                            # specific exception, not a bare except
                rejected.append((number, line, str(e)))
                continue
            total += amount
            report_lines.append(f"{register}  {name:<15}{amount:>10}")
    return report_lines, total, rejected


def main(path):
    try:
        report_lines, total, rejected = total_mess_bills(path)
    except FileNotFoundError:
        print(f"Cannot find '{path}'. Check the file name.")
        return 1
    except PermissionError:
        print(f"No permission to read '{path}'.")
        return 1
    except UnicodeDecodeError as e:
        print(f"'{path}' is not UTF-8 text: {e.reason} at byte {e.start}.")
        return 1
    print("\n".join(report_lines))                             # one join instead of repeated +
    print(f"Total {total}  ({len(report_lines)} bills accepted, {len(rejected)} lines rejected)")
    if rejected:
        print("\nRejected lines:")
        for number, text, reason in rejected:
            print(f"  line {number}: {text!r} -> {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "mess_oct.txt"))
