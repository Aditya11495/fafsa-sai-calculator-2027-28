from .rounding import whole

def payroll_tax_allowance(earned_income: float, filing_status: str) -> int:
    earned_income = max(0.0, earned_income)

    if filing_status == "MFJ":
        hi_threshold = 250000
        oasdi_base = 352200
    elif filing_status == "MFS":
        hi_threshold = 125000
        oasdi_base = 176100
    else:
        hi_threshold = 200000
        oasdi_base = 176100

    hi = min(earned_income, hi_threshold) * 0.0145
    if earned_income > hi_threshold:
        hi += (earned_income - hi_threshold) * 0.0235

    oasdi = min(earned_income, oasdi_base) * 0.062

    return whole(round(hi, 3) + round(oasdi, 3))
