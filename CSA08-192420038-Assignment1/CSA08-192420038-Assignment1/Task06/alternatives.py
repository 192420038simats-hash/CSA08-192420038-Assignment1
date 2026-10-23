"""Task 6 alternative: one long script (repeated code) and lambda expressions; function-call overhead timing."""
import time
from functions import payout, rate_per_litre

N = 500_000
entries = [(8.5, 4.2, 8.7)] * N

# (a) functions
t0 = time.perf_counter(); tot = 0.0
for l, f, s in entries: tot += payout(l, f, s)
t_func = time.perf_counter() - t0

# (b) one long script - everything inlined (this block would be pasted for every report that needs it)
t0 = time.perf_counter(); tot2 = 0.0
for l, f, s in entries:
    rate = round(30.00 + round((f - 3.5) / 0.1) * 0.40 + round((s - 8.5) / 0.1) * 0.30, 2)
    tot2 += round(l * rate, 2)
t_inline = time.perf_counter() - t0

# (c) lambdas
rate_l = lambda f, s: round(30.00 + round((f - 3.5) / 0.1) * 0.40 + round((s - 8.5) / 0.1) * 0.30, 2)
pay_l = lambda l, f, s: round(l * rate_l(f, s), 2)
t0 = time.perf_counter(); tot3 = 0.0
for l, f, s in entries: tot3 += pay_l(l, f, s)
t_lambda = time.perf_counter() - t0

print(f"functions : {t_func:.3f} s   inline script: {t_inline:.3f} s   lambda: {t_lambda:.3f} s   (n = {N:,})")
print("totals    :", round(tot, 2), round(tot2, 2), round(tot3, 2))
print(f"overhead per entry (functions vs inline): {(t_func - t_inline) / N * 1e6:.2f} microseconds")
