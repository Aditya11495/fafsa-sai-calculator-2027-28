def check_minimum_pell(
    dependency_status: str,
    single_parent: bool,
    is_parent: bool,
    agi: float,
    foreign_income_exclusion: float,
    poverty_guideline: float,
    sai: int,
    maximum_pell_award: float,
) -> dict:
    """Return the 2027-28 Minimum Pell indicator test result."""
    dependency_status = dependency_status.lower()
    income_measure = max(0.0, agi) + max(0.0, foreign_income_exclusion)

    if dependency_status == "dependent":
        threshold_percent = 325 if single_parent else 275
        indicator = 1 if single_parent else 2
    else:
        if single_parent:
            threshold_percent = 400
            indicator = 3
        elif is_parent:
            threshold_percent = 350
            indicator = 4
        else:
            threshold_percent = 275
            indicator = 5

    threshold_amount = poverty_guideline * threshold_percent / 100
    poverty_test = income_measure <= threshold_amount

    # 2027-28 additional condition.
    sai_test = sai < (2 * maximum_pell_award)

    eligible = poverty_test and sai_test

    return {
        "eligible": eligible,
        "indicator": indicator if eligible else None,
        "threshold_percent": threshold_percent,
        "threshold_amount": threshold_amount,
        "income_measure": income_measure,
        "poverty_test": poverty_test,
        "sai_test": sai_test,
        "sai_limit": 2 * maximum_pell_award,
    }
