"""Task 5 alternative: try/except versus string check - time and behaviour."""
import timeit
from input_reader import is_valid_number, parse_try_except
for text in ["8.5", "8,5", "eight"]:
    t1 = timeit.timeit(lambda: is_valid_number(text), number=500_000)
    t2 = timeit.timeit(lambda: parse_try_except(text), number=500_000)
    print(f"{text!r:8} string-check {t1:.3f} s   try/except {t2:.3f} s  (500,000 calls)")
