def select_formula(dependency_status: str, has_dependents: bool) -> str:
    """
    2027–28 mathematical guide:
      Dependent -> A
      Independent + no dependents other than spouse -> B
      Independent + one or more dependents other than spouse -> C
    """
    if dependency_status == "dependent":
        return "A"

    if dependency_status == "independent" and has_dependents:
        return "C"

    return "B"
