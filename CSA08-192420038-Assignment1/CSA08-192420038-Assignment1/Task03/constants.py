"""Task 3 - single, well-named set of constants (Python has no true constants: UPPER_CASE is a convention)."""
from decimal import Decimal

BASE_RATE = Decimal("30.00")        # Rs/litre at standard quality
FAT_STEP_VALUE = Decimal("0.40")    # Rs/litre per 0.1 % fat
SNF_STEP_VALUE = Decimal("0.30")    # Rs/litre per 0.1 % SNF
STD_FAT = Decimal("3.5")            # standard fat %
STD_SNF = Decimal("8.5")            # standard SNF %
STEP = Decimal("0.1")               # size of one step in %
FAT_MIN, FAT_MAX = Decimal("2.0"), Decimal("7.0")   # valid fat range
SNF_MIN, SNF_MAX = Decimal("7.0"), Decimal("10.0")  # assumed valid SNF range
PAISE = Decimal("0.01")

if __name__ == "__main__":
    # Dynamic typing: the same name can hold an int and later a str
    x = 10
    print(type(x), x)
    x = "ten"
    print(type(x), x)
    # x + 1 would now raise TypeError - the type belongs to the value, not the name

    # Constants are only a convention: Python lets you rebind them (a code-review problem, not a syntax error)
    BASE_RATE = Decimal("99")
    print("Rebinding is allowed:", BASE_RATE)

    # Multiple assignment and swapping
    a, b = 3.5, 8.5
    a, b = b, a
    print("after swap a, b =", a, b)
    litres, fat, snf = 8.5, 4.2, 8.7        # tuple unpacking
    print(litres, fat, snf)
    # Naming: snake_case for variables, UPPER_CASE constants; no spaces, cannot start with digit, not a keyword
