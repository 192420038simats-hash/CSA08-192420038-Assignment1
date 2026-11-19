"""Task 5.3 - the three import forms, and a naming conflict. Run from the Task05 folder."""
import sys
sys.path.insert(0, "after_change/d_package")      # so that the package 'attendance' can be found
import attendance.stats                         # form 1: whole sub-module, used with the full dotted name
from attendance import stats                    # form 2: the sub-module under its short name
from attendance.stats import percentage        # form 3: one function, used with no prefix

print("1 import attendance.stats       ->", attendance.stats.percentage(3, 4))
print("2 from attendance import stats  ->", stats.percentage(3, 4))
print("3 from attendance.stats import percentage ->", percentage(3, 4))
print("all three refer to the same function object:", attendance.stats.percentage is stats.percentage is percentage)

# Naming conflict: a name imported with 'from ... import' is silently replaced by a later assignment or import
percentage = 99                                  # my own variable has the same name -> the function is lost
try:
    percentage(3, 4)
except TypeError as e:
    print("conflict with form 3:", e)
print("forms 1 and 2 are still safe:", attendance.stats.percentage(3, 4))

# A second module with the same function name
import math
from math import floor
floor = lambda x: "my own floor"                 # shadows math.floor
print("shadowed floor:", floor(2.5), "| math.floor still works:", math.floor(2.5))
