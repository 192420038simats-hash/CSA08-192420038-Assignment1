"""Task 4 - expressions: steps, rate and amount, with surprising results explained."""
import math

# --- precedence and associativity ---
print("-2 ** 2        =", -2 ** 2, "   (** binds tighter than unary minus -> -(2**2))")
print("(-2) ** 2      =", (-2) ** 2)
print("2 ** 3 ** 2    =", 2 ** 3 ** 2, " (** is right-associative -> 2**(3**2))")
print("10 - 4 - 3     =", 10 - 4 - 3, "  (left-associative)")
print("30 + 7 * 0.4   =", 30 + 7 * 0.4, " (* before +)")

# --- surprise 1 ---
print("\nSurprise 1: (4.2 - 3.5) / 0.1 =", (4.2 - 3.5) / 0.1)
print("            round(...)         =", round((4.2 - 3.5) / 0.1))
# --- surprise 2 ---
print("Surprise 2: (3.1 - 3.5) / 0.1 =", (3.1 - 3.5) / 0.1, " int() ->", int((3.1 - 3.5) / 0.1), " round() ->", round((3.1 - 3.5) / 0.1))
# --- surprise 3 ---
print("Surprise 3: 0.4 * 7 =", 0.4 * 7, " ; 30 + 0.4*7 + 0.3*2 =", 30 + 0.4 * 7 + 0.3 * 2)
# --- surprise 4: banker's rounding / representation ---
print("Surprise 4: round(2.5) =", round(2.5), ", round(3.5) =", round(3.5), ", round(0.285, 2) =", round(0.285, 2))

# --- int / floor / round for negative values ---
print("\nvalue      int  floor  round")
for v in (2.7, -2.7, 2.5, -2.5, -0.4):
    print(f"{v:6}  {int(v):5} {math.floor(v):5} {round(v):6}")

# --- comparison chaining and Boolean operators ---
fat = 4.2
print("\n2.0 <= fat <= 7.0 :", 2.0 <= fat <= 7.0)
print("same, long form    :", 2.0 <= fat and fat <= 7.0)
print("not (fat < 2.0 or fat > 7.0):", not (fat < 2.0 or fat > 7.0))

# --- the actual expressions of the calculator ---
BASE_RATE, FAT_VAL, SNF_VAL = 30.00, 0.40, 0.30
litres, fat, snf = 8.5, 4.2, 8.7
fat_steps = round((fat - 3.5) / 0.1)
snf_steps = round((snf - 8.5) / 0.1)
rate = round(BASE_RATE + fat_steps * FAT_VAL + snf_steps * SNF_VAL, 2)
amount = round(litres * rate, 2)
print(f"\nfat_steps={fat_steps} snf_steps={snf_steps} rate={rate} amount={amount}")
