from .rounding import whole
from .payroll import payroll_tax_allowance
from .assets import adjusted_business_farm, asset_contribution
from .tables import parent_aai, formula_c_aai
from .models import FAFSAInput

EEA_CAP = 5200
DEPENDENT_IPA = 12220
INDEPENDENT_UNMARRIED_IPA = 19000
INDEPENDENT_MARRIED_IPA = 30470

def common_income(x: FAFSAInput):
    additions = (
        x.agi + x.ira_keogh + x.tax_exempt_interest +
        x.untaxed_ira + x.untaxed_pensions + x.foreign_income_exclusion
    )
    offsets = x.taxable_grants + x.education_credits + x.work_study
    return whole(additions - offsets), whole(additions), whole(offsets)

def formula_a(x: FAFSAInput):
    p_income, _, _ = common_income(
        FAFSAInput(
            formula="A", married=x.married, family_size=x.family_size,
            agi=x.parent_agi, ira_keogh=0, tax_exempt_interest=0,
            untaxed_ira=0, untaxed_pensions=0,
            foreign_income_exclusion=0, tax_paid=x.parent_tax_paid,
            earned_income=x.parent_earned_income, taxable_grants=0,
            education_credits=0, work_study=0, child_support=0, cash=0,
            investments=0, business_farm_net_worth=0
        )
    )
    parent_payroll = payroll_tax_allowance(x.parent_earned_income, "MFJ" if x.married else "SINGLE")
    parent_ipa = parent_ipa_value(x.family_size)
    parent_eea = min(0.35 * x.parent_earned_income, EEA_CAP)

    parent_available = whole(p_income - x.parent_tax_paid - parent_payroll - parent_ipa - parent_eea)

    parent_biz = adjusted_business_farm(x.parent_business_farm_net_worth)
    parent_assets = x.parent_child_support + x.parent_cash + x.parent_investments + parent_biz
    pca = asset_contribution(parent_assets, 0.12)
    paaI = whole(parent_available + pca)
    parents_contribution = parent_aai(paaI)

    student_income, _, _ = common_income(x)
    student_payroll = payroll_tax_allowance(x.earned_income, "MFJ" if x.married else "SINGLE")
    student_available = whole(student_income - x.tax_paid - student_payroll - DEPENDENT_IPA)
    student_income_contribution = max(0, whole(student_available * 0.50))

    student_biz = adjusted_business_farm(x.business_farm_net_worth)
    student_assets = x.cash + x.investments + student_biz
    student_asset_contribution = asset_contribution(student_assets, 0.20)

    sai = parents_contribution + student_income_contribution + student_asset_contribution
    return {
        "formula": "A",
        "parent_available_income": parent_available,
        "parent_asset_contribution": pca,
        "parents_contribution": parents_contribution,
        "student_income_contribution": student_income_contribution,
        "student_asset_contribution": student_asset_contribution,
        "sai": bound_sai(sai),
    }

def formula_b(x: FAFSAInput):
    income, _, _ = common_income(x)
    payroll = payroll_tax_allowance(x.earned_income, "MFJ" if x.married else "SINGLE")
    ipa = INDEPENDENT_MARRIED_IPA if x.married else INDEPENDENT_UNMARRIED_IPA
    eea = min(0.35 * x.earned_income, EEA_CAP) if x.married else 0
    available = whole(income - x.tax_paid - payroll - ipa - eea)

    biz = adjusted_business_farm(x.business_farm_net_worth)
    net_worth = x.child_support + x.cash + x.investments + biz
    asset = asset_contribution(net_worth, 0.20)

    sai = whole(available * 0.50) + asset
    return {
        "formula": "B",
        "available_income": available,
        "income_contribution": whole(available * 0.50),
        "asset_contribution": asset,
        "sai": bound_sai(sai),
    }

def formula_c(x: FAFSAInput):
    income, _, _ = common_income(x)
    payroll = payroll_tax_allowance(x.earned_income, "MFJ" if x.married else "SINGLE")
    ipa = formula_c_ipa(x.family_size, x.married)
    eea = min(0.35 * x.earned_income, EEA_CAP)
    available = whole(income - x.tax_paid - payroll - ipa - eea)

    biz = adjusted_business_farm(x.business_farm_net_worth)
    net_worth = x.child_support + x.cash + x.investments + biz
    asset = asset_contribution(net_worth, 0.07)
    aai = whole(available + asset)

    sai = formula_c_aai(aai)
    return {
        "formula": "C",
        "available_income": available,
        "asset_contribution": asset,
        "adjusted_available_income": aai,
        "sai": bound_sai(sai),
    }

def calculate_sai(x: FAFSAInput):
    if x.formula == "A":
        return formula_a(x)
    if x.formula == "B":
        return formula_b(x)
    if x.formula == "C":
        return formula_c(x)
    raise ValueError("Formula must be A, B, or C.")

def parent_ipa_value(family_size: int):
    table = {2: 30300, 3: 37720, 4: 46590, 5: 54970, 6: 64290}
    if family_size in table:
        return table[family_size]
    if family_size > 6:
        return table[6] + (family_size - 6) * 7260
    return 0

def formula_c_ipa(family_size: int, married: bool):
    if married:
        table = {3: 59930, 4: 74000, 5: 87320, 6: 102120}
        increment = 11530
        if family_size in table:
            return table[family_size]
        if family_size > 6:
            return table[6] + (family_size - 6) * increment
    else:
        table = {2: 57050, 3: 71040, 4: 87700, 5: 103500, 6: 121030}
        increment = 13680
        if family_size in table:
            return table[family_size]
        if family_size > 6:
            return table[6] + (family_size - 6) * increment
    return 0

def bound_sai(value: int):
    return max(-1500, min(999999, value))
