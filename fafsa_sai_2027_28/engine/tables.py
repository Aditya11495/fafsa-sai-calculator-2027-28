def parent_aai(aai: float) -> int:
    # 2027–28 Table A5
    if aai < -8900:
        return -1958
    if aai <= 22600:
        return round(aai * 0.22)
    if aai <= 28300:
        return round(4972 + 0.25 * (aai - 22600))
    if aai <= 34000:
        return round(6397 + 0.29 * (aai - 28300))
    if aai <= 39900:
        return round(8050 + 0.34 * (aai - 34000))
    if aai <= 45600:
        return round(10056 + 0.40 * (aai - 39900))
    return round(12336 + 0.47 * (aai - 45600))

def formula_c_aai(aai: float) -> int:
    # 2027–28 Table C6
    return parent_aai(aai)
