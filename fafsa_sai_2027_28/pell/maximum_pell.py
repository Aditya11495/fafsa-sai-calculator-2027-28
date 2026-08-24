def check_maximum_pell(
    dependency_status: str,
    single_parent: bool,
    agi: float,
    foreign_income_exclusion: float,
    poverty_guideline: float,
    tax_filing_required: bool,
) -> dict:
    """Return the 2027-28 Maximum Pell indicator test result."""
    income_measure = max(0.0, agi) + max(0.0, foreign_income_exclusion)
    dependency_status = dependency_status.lower()

    if not tax_filing_required:
        return {
            "eligible": True,
            "indicator": 1,
            "reason": "Student/parent (and spouse if applicable) is not required to file a federal income tax return.",
            "income_measure": income_measure,
            "threshold_percent": None,
            "threshold_amount": None,
        }

    threshold_percent = 225 if single_parent else 175
    threshold_amount = poverty_guideline * threshold_percent / 100

    # The 2027-28 guide requires the AGI + FEIE amount to be > 0
    # for the poverty-guideline Max Pell indicators.
    eligible = 0 < income_measure <= threshold_amount

    indicator = None
    if eligible:
        indicator = 2 if single_parent else 3

    return {
        "eligible": eligible,
        "indicator": indicator,
        "reason": (
            f"AGI + foreign income exclusion <= {threshold_percent}% "
            "of the applicable poverty guideline."
            if eligible else
            "Maximum Pell poverty-guideline test not satisfied."
        ),
        "income_measure": income_measure,
        "threshold_percent": threshold_percent,
        "threshold_amount": threshold_amount,
    }
