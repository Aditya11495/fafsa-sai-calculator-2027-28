from .maximum_pell import check_maximum_pell
from .minimum_pell import check_minimum_pell
from .calculated_pell import (
    calculate_calculated_pell,
    round_pell_award,
)


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
    """
    2027-28 Pell workflow:

    Step 1:
        Determine Maximum Pell eligibility.

    Step 2:
        Calculate Pell from SAI.

    Step 3:
        Determine Minimum Pell eligibility.
    """

    # --------------------------------------------------------
    # INPUT VALIDATION
    # --------------------------------------------------------

    if maximum_pell_award <= 0:
        raise ValueError(
            "Maximum Pell award must be greater than zero."
        )

    if minimum_pell_award <= 0:
        raise ValueError(
            "Minimum Pell award must be greater than zero."
        )

    if cost_of_attendance < 0:
        raise ValueError(
            "Cost of attendance cannot be negative."
        )

    if not 0 < enrollment_intensity <= 1:
        raise ValueError(
            "Enrollment intensity must be between 0 and 1."
        )

    # --------------------------------------------------------
    # STEP 1
    # MAXIMUM PELL TEST
    # --------------------------------------------------------

    max_result = check_maximum_pell(
        dependency_status=dependency_status,
        single_parent=single_parent,
        agi=agi,
        foreign_income_exclusion=foreign_income_exclusion,
        poverty_guideline=poverty_guideline,
        tax_filing_required=tax_filing_required,
    )

    max_indicator = max_result["indicator"]

    # --------------------------------------------------------
    # MAXIMUM PELL INDICATOR 1
    #
    # Non-filer:
    # SAI = -1500
    # No further calculation.
    # --------------------------------------------------------

    if max_result["eligible"] and max_indicator == 1:

        annual_award = maximum_pell_award

        scheduled = min(
            annual_award * enrollment_intensity,
            cost_of_attendance,
        )

        return {
            "pell_eligible": True,
            "pell_type": "Maximum Pell",
            "pell_indicator": 1,
            "annual_award_before_enrollment": annual_award,
            "scheduled_award": round_pell_award(scheduled),
            "maximum_pell": max_result,
            "calculated_pell": None,
            "minimum_pell": None,
        }

    # --------------------------------------------------------
    # STEP 2
    #
    # All other applicants, including Maximum Pell
    # Indicators 2 and 3, go through SAI calculation.
    # --------------------------------------------------------

    calculated = calculate_calculated_pell(
        sai=sai,
        maximum_pell_award=maximum_pell_award,
        minimum_pell_award=minimum_pell_award,
    )

    calculated_rounded = round_pell_award(
        calculated["raw_amount"]
    )

    # --------------------------------------------------------
    # SAI <= 0
    #
    # Maximum Pell
    # --------------------------------------------------------

    if sai <= 0:

        annual_award = maximum_pell_award

        scheduled = min(
            annual_award * enrollment_intensity,
            cost_of_attendance,
        )

        return {
            "pell_eligible": True,
            "pell_type": "Maximum Pell",
            "pell_indicator": max_indicator,
            "annual_award_before_enrollment": annual_award,
            "scheduled_award": round_pell_award(scheduled),
            "maximum_pell": max_result,
            "calculated_pell": {
                **calculated,
                "rounded_amount": calculated_rounded,
            },
            "minimum_pell": None,
        }

    # --------------------------------------------------------
    # CALCULATED PELL
    #
    # SAI <= Maximum Pell - Minimum Pell
    # --------------------------------------------------------

    calculated_threshold = (
        maximum_pell_award
        - minimum_pell_award
    )

    if sai <= calculated_threshold:

        scheduled = min(
            calculated_rounded * enrollment_intensity,
            cost_of_attendance,
        )

        return {
            "pell_eligible": True,
            "pell_type": "Calculated Pell",
            "pell_indicator": (
                max_indicator
                if max_result["eligible"]
                else None
            ),
            "annual_award_before_enrollment": calculated_rounded,
            "scheduled_award": round_pell_award(scheduled),
            "maximum_pell": max_result,
            "calculated_pell": {
                **calculated,
                "rounded_amount": calculated_rounded,
            },
            "minimum_pell": None,
        }

    # --------------------------------------------------------
    # STEP 3
    # MINIMUM PELL
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # MINIMUM PELL ELIGIBLE
    # --------------------------------------------------------

    if minimum["eligible"]:

        scheduled = min(
            minimum_pell_award * enrollment_intensity,
            cost_of_attendance,
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

    # --------------------------------------------------------
    # NO PELL
    # --------------------------------------------------------

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