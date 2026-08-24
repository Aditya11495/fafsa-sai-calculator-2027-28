from pell.maximum_pell import check_maximum_pell
from pell.minimum_pell import check_minimum_pell
from pell.pell_engine import calculate_pell
from tables.pell_parameters import get_poverty_guideline


def test_poverty_guideline_family_4_other():
    assert get_poverty_guideline("Other", 4) == 32150


def test_maximum_pell_not_single_parent_175_percent():
    result = check_maximum_pell(
        dependency_status="dependent",
        single_parent=False,
        agi=50000,
        foreign_income_exclusion=0,
        poverty_guideline=32150,
        tax_filing_required=True,
    )
    assert result["eligible"] is True
    assert result["indicator"] == 3


def test_calculated_pell():
    result = calculate_pell(
        sai=2254,
        dependency_status="dependent",
        single_parent=False,
        is_parent=False,
        agi=60000,
        foreign_income_exclusion=0,
        poverty_guideline=32150,
        tax_filing_required=True,
        maximum_pell_award=7395,
        minimum_pell_award=740,
        cost_of_attendance=10000,
        enrollment_intensity=1.0,
    )
    assert result["pell_eligible"] is True
    assert result["pell_type"] == "Calculated Pell"
    assert result["scheduled_award"] == 5140


def test_minimum_pell_path():
    result = calculate_pell(
        sai=14000,
        dependency_status="dependent",
        single_parent=False,
        is_parent=False,
        agi=80000,
        foreign_income_exclusion=0,
        poverty_guideline=32150,
        tax_filing_required=True,
        maximum_pell_award=7395,
        minimum_pell_award=740,
        cost_of_attendance=10000,
        enrollment_intensity=1.0,
    )
    assert result["pell_eligible"] is True
    assert result["pell_type"] == "Minimum Pell"
    assert result["scheduled_award"] == 740
