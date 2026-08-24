def adjusted_business_farm(net_worth: float) -> int:
    n = max(0.0, net_worth)

    if n < 1:
        return 0
    if n <= 180000:
        return round(0.40 * n)
    if n <= 540000:
        return round(72000 + 0.50 * (n - 180000))
    if n <= 905000:
        return round(252000 + 0.60 * (n - 540000))
    return round(471000 + 1.00 * (n - 905000))

def asset_contribution(net_worth: float, rate: float, apa: float = 0.0) -> int:
    discretionary = net_worth - apa
    return max(0, round(discretionary * rate))
