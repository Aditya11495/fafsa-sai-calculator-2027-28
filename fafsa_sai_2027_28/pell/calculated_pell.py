def calculate_calculated_pell(sai: int, maximum_pell_award: float) -> dict:
    raw = maximum_pell_award - sai
    return {
        "eligible": raw > 0,
        "raw_amount": max(0.0, raw),
    }


def round_pell_award(amount: float) -> int:
    # Pell award rounding is to the nearest $5 for this calculation path.
    return int(round(amount / 5) * 5)
