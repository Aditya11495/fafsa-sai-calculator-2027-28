from .rounding import whole
from .payroll import payroll_tax_allowance
from .assets import adjusted_business_farm, asset_contribution
from .tables import parent_aai, formula_c_aai
from .models import FAFSAInput


# ============================================================
# 2027-28 PARAMETERS
# ============================================================

EEA_CAP = 5200

DEPENDENT_IPA = 12220

INDEPENDENT_UNMARRIED_IPA = 19000
INDEPENDENT_MARRIED_IPA = 30470


# ============================================================
# COMMON INCOME CALCULATION
# ============================================================

def common_income(x: FAFSAInput):
    """
    Total Income =
        Income Additions - Income Offsets

    Income additions:
        AGI
        + IRA/KEOGH
        + Tax-exempt interest
        + Untaxed IRA
        + Untaxed pensions
        + Foreign income exclusion

    Income offsets:
        Taxable grants/scholarships
        + Education credits
        + Federal Work-Study
    """

    additions = (
        x.agi
        + x.ira_keogh
        + x.tax_exempt_interest
        + x.untaxed_ira
        + x.untaxed_pensions
        + x.foreign_income_exclusion
    )

    offsets = (
        x.taxable_grants
        + x.education_credits
        + x.work_study
    )

    total_income = whole(additions - offsets)

    return (
        total_income,
        whole(additions),
        whole(offsets),
    )


# ============================================================
# FORMULA A
# DEPENDENT STUDENT
# ============================================================

def formula_a(x: FAFSAInput):

    # --------------------------------------------------------
    # 1. Parent income
    # --------------------------------------------------------

    parent_additions = (
        x.parent_agi
        + x.parent_ira_keogh
        + x.parent_tax_exempt_interest
        + max(0.0, x.parent_untaxed_ira)
        + max(0.0, x.parent_untaxed_pensions)
        + abs(x.parent_foreign_income_exclusion)
    )

    parent_offsets = (
        x.parent_taxable_grants
        + x.parent_education_credits
        + x.parent_work_study
    )

    parent_income = whole(
        parent_additions - parent_offsets
    )

    # --------------------------------------------------------
    # 2. Parent allowances
    # --------------------------------------------------------

    parent_payroll = payroll_tax_allowance(
        x.parent_earned_income,
        "MFJ" if x.married else "SINGLE"
    )

    parent_ipa = parent_ipa_value(
        x.family_size
    )

    parent_eea = min(
        0.35 * x.parent_earned_income,
        EEA_CAP
    )

    parent_available = whole(
        parent_income
        - x.parent_tax_paid
        - parent_payroll
        - parent_ipa
        - parent_eea
    )

    # --------------------------------------------------------
    # 3. Parent assets
    # --------------------------------------------------------

    parent_biz = adjusted_business_farm(
        x.parent_business_farm_net_worth
    )

    parent_assets = (
        x.parent_child_support
        + max(0.0, x.parent_cash)
        + max(0.0, x.parent_investments)
        + parent_biz
    )

    # 2027-28 Formula A parent asset rate = 12%
    parent_asset_contribution = asset_contribution(
        parent_assets,
        0.12
    )

    # --------------------------------------------------------
    # 4. Parent Adjusted Available Income
    # --------------------------------------------------------

    parent_paai = whole(
        parent_available
        + parent_asset_contribution
    )

    parents_contribution = parent_aai(
        parent_paai
    )

    # --------------------------------------------------------
    # 5. Student income
    # --------------------------------------------------------

    student_income, _, _ = common_income(x)

    student_payroll = payroll_tax_allowance(
        x.earned_income,
        "MFJ" if x.married else "SINGLE"
    )

    # IMPORTANT:
    # If Parent AAI/PAAI is negative, its absolute value
    # becomes an allowance against student income.
    parent_negative_paai_allowance = max(
        0,
        -parent_paai
    )

    student_available = whole(
        student_income
        - x.tax_paid
        - student_payroll
        - DEPENDENT_IPA
        - parent_negative_paai_allowance
    )

    # Student contribution from income = 50%
    student_income_contribution = max(
        0,
        whole(student_available * 0.50)
    )

    # --------------------------------------------------------
    # 6. Student assets
    # --------------------------------------------------------

    student_biz = adjusted_business_farm(
        x.business_farm_net_worth
    )

    student_assets = (
        max(0.0, x.cash)
        + max(0.0, x.investments)
        + student_biz
    )

    # Formula A student asset rate = 20%
    student_asset_contribution = asset_contribution(
        student_assets,
        0.20
    )

    # --------------------------------------------------------
    # 7. Final SAI
    # --------------------------------------------------------

    sai = (
        parents_contribution
        + student_income_contribution
        + student_asset_contribution
    )

    return {
        "formula": "A",

        "parent_income": parent_income,
        "parent_available_income": parent_available,

        "parent_asset_contribution":
            parent_asset_contribution,

        "parent_adjusted_available_income":
            parent_paai,

        "parent_negative_paai_allowance":
            parent_negative_paai_allowance,

        "parents_contribution":
            parents_contribution,

        "student_income_contribution":
            student_income_contribution,

        "student_asset_contribution":
            student_asset_contribution,

        "sai": bound_sai(sai),
    }


# ============================================================
# FORMULA B
# INDEPENDENT STUDENT WITHOUT DEPENDENTS
# ============================================================

def formula_b(x: FAFSAInput):

    income, _, _ = common_income(x)

    payroll = payroll_tax_allowance(
        x.earned_income,
        "MFJ" if x.married else "SINGLE"
    )

    ipa = (
        INDEPENDENT_MARRIED_IPA
        if x.married
        else INDEPENDENT_UNMARRIED_IPA
    )

    eea = (
        min(0.35 * x.earned_income, EEA_CAP)
        if x.married
        else 0
    )

    available = whole(
        income
        - x.tax_paid
        - payroll
        - ipa
        - eea
    )

    biz = adjusted_business_farm(
        x.business_farm_net_worth
    )

    net_worth = (
        x.child_support
        + max(0.0, x.cash)
        + max(0.0, x.investments)
        + biz
    )

    asset = asset_contribution(
        net_worth,
        0.20
    )

    income_contribution = whole(
        available * 0.50
    )

    sai = income_contribution + asset

    return {
        "formula": "B",
        "available_income": available,
        "income_contribution": income_contribution,
        "asset_contribution": asset,
        "sai": bound_sai(sai),
    }


# ============================================================
# FORMULA C
# INDEPENDENT STUDENT WITH DEPENDENTS
# ============================================================

def formula_c(x: FAFSAInput):

    income, _, _ = common_income(x)

    payroll = payroll_tax_allowance(
        x.earned_income,
        "MFJ" if x.married else "SINGLE"
    )

    ipa = formula_c_ipa(
        x.family_size,
        x.married
    )

    eea = min(
        0.35 * x.earned_income,
        EEA_CAP
    )

    available = whole(
        income
        - x.tax_paid
        - payroll
        - ipa
        - eea
    )

    biz = adjusted_business_farm(
        x.business_farm_net_worth
    )

    net_worth = (
        x.child_support
        + max(0.0, x.cash)
        + max(0.0, x.investments)
        + biz
    )

    # Formula C asset rate = 7%
    asset = asset_contribution(
        net_worth,
        0.07
    )

    adjusted_available_income = whole(
        available + asset
    )

    sai = formula_c_aai(
        adjusted_available_income
    )

    return {
        "formula": "C",
        "available_income": available,
        "asset_contribution": asset,
        "adjusted_available_income":
            adjusted_available_income,
        "sai": bound_sai(sai),
    }


# ============================================================
# MAIN SAI CALCULATOR
# ============================================================

def calculate_sai(x: FAFSAInput):

    if x.formula == "A":
        return formula_a(x)

    if x.formula == "B":
        return formula_b(x)

    if x.formula == "C":
        return formula_c(x)

    raise ValueError(
        "Formula must be A, B, or C."
    )


# ============================================================
# FORMULA A - PARENT IPA
# ============================================================

def parent_ipa_value(family_size: int):

    table = {
        2: 30300,
        3: 37720,
        4: 46590,
        5: 54970,
        6: 64290,
    }

    if family_size in table:
        return table[family_size]

    if family_size > 6:
        return (
            table[6]
            + (family_size - 6) * 7260
        )

    return 0


# ============================================================
# FORMULA C - IPA
# ============================================================

def formula_c_ipa(
    family_size: int,
    married: bool
):

    if married:

        table = {
            3: 59930,
            4: 74000,
            5: 87320,
            6: 102120,
        }

        increment = 11530

        if family_size in table:
            return table[family_size]

        if family_size > 6:
            return (
                table[6]
                + (family_size - 6) * increment
            )

    else:

        table = {
            2: 57050,
            3: 71040,
            4: 87700,
            5: 103500,
            6: 121030,
        }

        increment = 13680

        if family_size in table:
            return table[family_size]

        if family_size > 6:
            return (
                table[6]
                + (family_size - 6) * increment
            )

    return 0


# ============================================================
# SAI BOUNDS
# ============================================================

def bound_sai(value: int):

    return max(
        -1500,
        min(999999, value)
    )