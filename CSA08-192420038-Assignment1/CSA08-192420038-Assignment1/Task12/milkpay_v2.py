"""Task 12 - adapted design (MODIFY, not redesign): same Decimal core, rate card selected by month,
two-decimal analyser readings give fractional steps, separate bonus function for the ten-day total."""
import json, os
from decimal import Decimal, ROUND_HALF_UP

PAISE = Decimal("0.01")
CARD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rate_cards.json")


def load_cards(path=CARD_FILE):
    """Return (cards, summer_months). Cards map season name -> dict of Decimal values."""
    with open(path) as fh:
        raw = json.load(fh)
    months = raw.pop("summer_months")
    return {name: {k: Decimal(v) for k, v in card.items()} for name, card in raw.items()}, months


def select_card(month, cards, summer_months):
    """Return the rate card in force for a month number 1-12."""
    return cards["summer"] if month in summer_months else cards["standard"]


def money(x):
    """Round to whole paise, halves up."""
    return x.quantize(PAISE, rounding=ROUND_HALF_UP)


def steps(value, standard, step):
    """Number of 0.1 % steps (may be fractional with two-decimal readings, exact in Decimal)."""
    return (value - standard) / step


def rate_per_litre(fat, snf, card):
    """Rate per litre rounded to the paisa; fat/snf are Decimals with up to two decimals."""
    r = (card["base_rate"]
         + steps(fat, card["std_fat"], card["step"]) * card["fat_step_value"]
         + steps(snf, card["std_snf"], card["step"]) * card["snf_step_value"])
    return money(r)


def payout(litres, fat, snf, card):
    """Amount for one delivery (no bonus)."""
    return money(litres * rate_per_litre(fat, snf, card))


def bonus(total_litres, card):
    """Bonus for the ten days: Rs 0.50 on EVERY litre when total litres are MORE than 500 (assumption: all litres)."""
    if total_litres > card["bonus_threshold_litres"]:
        return money(total_litres * card["bonus_per_litre"])
    return Decimal("0.00")


def ten_day_total(entries, card):
    """entries: list of (litres, fat, snf) text triples. Returns (milk_amount, bonus_amount, grand_total, total_litres)."""
    amount, litres_sum = Decimal("0.00"), Decimal("0")
    for l, f, s in entries:
        l, f, s = Decimal(l), Decimal(f), Decimal(s)
        amount += payout(l, f, s, card)
        litres_sum += l
    b = bonus(litres_sum, card)
    return amount, b, amount + b, litres_sum


if __name__ == "__main__":
    cards, months = load_cards()
    print("April card :", {k: str(v) for k, v in select_card(4, cards, months).items() if k in ("base_rate", "fat_step_value")})
    print("October card:", {k: str(v) for k, v in select_card(10, cards, months).items() if k in ("base_rate", "fat_step_value")})
