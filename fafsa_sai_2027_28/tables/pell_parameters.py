# 2027-28 Pell eligibility parameters.
#
# 2027-28 uses the 2025 HHS poverty guidelines for the applicable
# state category. The actual 2027-28 Maximum/Minimum Pell dollar
# amounts are award-year values and are kept as editable inputs in app.py
# until the Department publishes the final 2027-28 amounts.

POVERTY_GUIDELINES_2025 = {
    "Other": {
        1: 15650, 2: 21150, 3: 26650, 4: 32150,
        5: 37650, 6: 43150, 7: 48650, 8: 54150,
    },
    "Alaska": {
        1: 19550, 2: 26420, 3: 33290, 4: 40160,
        5: 47030, 6: 53900, 7: 60770, 8: 67640,
    },
    "Hawaii": {
        1: 17990, 2: 24220, 3: 30450, 4: 36680,
        5: 42910, 6: 49140, 7: 55370, 8: 61600,
    },
}

# Per-person increment for family size > 8.
ADDITIONAL_PERSON_2025 = {
    "Other": 5500,
    "Alaska": 6870,
    "Hawaii": 6230,
}

# Temporary test values only. Replace with official 2027-28 award-year
# amounts when published.
TEST_MAXIMUM_PELL_2026_27 = 7395
TEST_MINIMUM_PELL_2026_27 = 740


def get_poverty_guideline(state_category: str, family_size: int) -> int:
    if state_category not in POVERTY_GUIDELINES_2025:
        raise ValueError("state_category must be Other, Alaska, or Hawaii")
    if family_size < 1:
        raise ValueError("family_size must be at least 1")

    table = POVERTY_GUIDELINES_2025[state_category]
    if family_size <= 8:
        return table[family_size]

    return table[8] + (family_size - 8) * ADDITIONAL_PERSON_2025[state_category]
