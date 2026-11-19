"""A4 - a cleaning function with a deliberate precedence bug, used to demonstrate print / assert / logging / pdb."""
import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(funcName)s: %(message)s")
log = logging.getLogger(__name__)


def f_to_c(f):
    c = f - 32 * 5 / 9              # BUG: should be (f - 32) * 5 / 9
    log.debug("f_to_c(%s) = %s", f, c)
    assert -10 <= c <= 55, f"temperature {c:.1f} C is impossible for input {f} F"
    return round(c, 1)


def main():
    for f in (75.2, 86.0, 95.0):
        print(f"{f} F ->", f_to_c(f), "C")


if __name__ == "__main__":
    main()
