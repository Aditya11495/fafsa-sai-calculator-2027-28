from .maximum_pell import check_maximum_pell
from .minimum_pell import check_minimum_pell
from .calculated_pell import calculate_calculated_pell, round_pell_award


def calculate_pell(
    *,
    sai: int,
    dependency_status: str,
    single_parent: bool,
    is_parent: bool,
    agi: float,
    foreign_income_exclusion: float,
    poverty_guideline: float,
    tax_filing_required: bool,
    maximum_pell_award: float,
    minimum_pell_award: float,
    cost_of_attendance: float,
    enrollment_intensity: float,
) -> dict:
    """Run Maximum Pell -> Calculated Pell -> Minimum Pell logic."""

    if maximum_pell_award <= 0 or minimum_pell_award <= 0:
        raise ValueError("Pell award amounts must be greater than zero.")
    if cost_of_attendance < 0:
        raise ValueError("Cost of attendance cannot be negative.")
    if not 0 < enrollment_intensity <= 1:
        raise ValueError("Enrollment intensity must be between 0 and 1.")

    max_result = check_maximum_pell(
        dependency_status=dependency_status,
        single_parent=single_parent,
        agi=agi,
        foreign_income_exclusion=foreign_income_exclusion,
        poverty_guideline=poverty_guideline,
        tax_filing_required=tax_filing_required,
    )

    # Maximum Pell eligibility receives the full annual maximum,
    # subject to COA/enrollment intensity for this calculator.
    if max_result["eligible"]:
        annual_award = maximum_pell_award
        scheduled = min(annual_award * enrollment_intensity, cost_of_attendance)
        return {
            "pell_eligible": True,
            "pell_type": "Maximum Pell",
            "pell_indicator": max_result["indicator"],
            "annual_award_before_enrollment": annual_award,
            "scheduled_award": round_pell_award(scheduled),
            "maximum_pell": max_result,
            "calculated_pell": None,
            "minimum_pell": None,
        }

    calculated = calculate_calculated_pell(
        sai=sai,
        maximum_pell_award=maximum_pell_award
    )

    calculated_rounded = round_pell_award(calculated["raw_amount"])

    # Calculated Pell is available when Max Pell is not awarded and
    # the calculated amount is at least the applicable Minimum Pell.
    if calculated_rounded >= minimum_pell_award:
        scheduled = min(
            calculated_rounded * enrollment_intensity,
            cost_of_attendance
        )
        return {
            "pell_eligible": True,
            "pell_type": "Calculated Pell",
            "pell_indicator": None,
            "annual_award_before_enrollment": calculated_rounded,
            "scheduled_award": round_pell_award(scheduled),
            "maximum_pell": max_result,
            "calculated_pell": {
                **calculated,
                "rounded_amount": calculated_rounded,
            },
            "minimum_pell": None,
        }

    minimum = check_minimum_pell(
        dependency_status=dependency_status,
        single_parent=single_parent,
        is_parent=is_parent,
        agi=agi,
        foreign_income_exclusion=foreign_income_exclusion,
        poverty_guideline=poverty_guideline,
        sai=sai,
        maximum_pell_award=maximum_pell_award,
    )

    if minimum["eligible"]:
        scheduled = min(
            minimum_pell_award * enrollment_intensity,
            cost_of_attendance
        )
        return {
            "pell_eligible": True,
            "pell_type": "Minimum Pell",
            "pell_indicator": minimum["indicator"],
            "annual_award_before_enrollment": minimum_pell_award,
            "scheduled_award": round_pell_award(scheduled),
            "maximum_pell": max_result,
            "calculated_pell": {
                **calculated,
                "rounded_amount": calculated_rounded,
            },
            "minimum_pell": minimum,
        }

    return {
        "pell_eligible": False,
        "pell_type": None,
        "pell_indicator": None,
        "annual_award_before_enrollment": 0,
        "scheduled_award": 0,
        "maximum_pell": max_result,
        "calculated_pell": {
            **calculated,
            "rounded_amount": calculated_rounded,
        },
        "minimum_pell": minimum,
    }
