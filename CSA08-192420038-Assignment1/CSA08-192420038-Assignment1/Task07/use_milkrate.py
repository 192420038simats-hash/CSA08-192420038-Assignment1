"""A separate script that imports the module - the test table is NOT printed (because __name__ == 'milkrate')."""
import milkrate
from milkrate import payout
import milkrate as mr
import sys, math

print("module name seen inside milkrate:", milkrate.__name__)
print("payout(8.5, 4.2, 8.7)               =", payout(8.5, 4.2, 8.7))
print("milkrate.rate_per_litre(3.1, 8.3)   =", milkrate.rate_per_litre(3.1, 8.3))
print("mr.BASE_RATE                        =", mr.BASE_RATE)
print("milkrate in sys.modules (loaded once):", "milkrate" in sys.modules)
print("first sys.path entry (script folder):", sys.path[0].split("/")[-1])
print("math.floor(-2.5) from standard module:", math.floor(-2.5))
