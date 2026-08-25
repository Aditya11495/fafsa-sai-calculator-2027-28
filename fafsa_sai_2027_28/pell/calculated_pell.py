def calculate_calculated_pell(
    sai: int,
    maximum_pell_award: float,
    minimum_pell_award: float,
) -> dict:

    raw = maximum_pell_award - sai

    eligible = sai <= (
        maximum_pell_award - minimum_pell_award
    )

    return {
        "eligible": eligible,
        "raw_amount": max(0.0, raw) if eligible else 0.0,
    }


def round_pell_award(amount: float) -> int:

    # Pell award rounding is to the nearest $5.
    return int(round(amount / 5) * 5)