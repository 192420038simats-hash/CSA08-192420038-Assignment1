"""Task 11 - recommended design: Decimal values, ROUND_HALF_UP to the paisa on every payment,
rates read from rate_card.json at start-up (a rate revision = edit one file, no code change)."""
import json, os
from decimal import Decimal, ROUND_HALF_UP

PAISE = Decimal("0.01")
CARD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rate_card.json")


def load_rate_card(path=CARD_FILE):
    """Read the rate card; every value is parsed from text into Decimal (never through float)."""
    with open(path) as fh:
        raw = json.load(fh)
    return {k: Decimal(v) for k, v in raw.items()}


def money(x):
    """Round to whole paise, halves up."""
    return x.quantize(PAISE, rounding=ROUND_HALF_UP)


def rate_per_litre(fat, snf, card):
    """Rate per litre (paise precision) for Decimal fat and snf."""
    f = (fat - card["std_fat"]) / card["step"]
    s = (snf - card["std_snf"]) / card["step"]
    return money(card["base_rate"] + f * card["fat_step_value"] + s * card["snf_step_value"])


def payout(litres, fat, snf, card):
    """Amount payable, rounded per payment."""
    return money(litres * rate_per_litre(fat, snf, card))


def ten_day_total(entries, card):
    """Total of the per-payment amounts (what the bank pays)."""
    total = Decimal("0.00")
    for litres, fat, snf in entries:
        total += payout(Decimal(litres), Decimal(fat), Decimal(snf), card)
    return total


if __name__ == "__main__":
    import time
    t0 = time.perf_counter(); card = load_rate_card(); t1 = time.perf_counter()
    print(f"card loaded in {(t1-t0)*1e6:.0f} microseconds:", {k: str(v) for k, v in card.items()})
    sample = [("10", "3.5", "8.5"), ("8.5", "4.2", "8.7"), ("12", "3.1", "8.3")]
    print("total:", ten_day_total(sample, card))
    # rate revision: change only the JSON text (simulated here with a copy) - same code, new rates
    revised = dict(card, base_rate=Decimal("31.00"))
    print("total after base_rate revised to 31.00:", ten_day_total(sample, revised))
