from dataclasses import dataclass

@dataclass
class FAFSAInput:
    formula: str
    married: bool
    family_size: int

    agi: float
    ira_keogh: float
    tax_exempt_interest: float
    untaxed_ira: float
    untaxed_pensions: float
    foreign_income_exclusion: float
    tax_paid: float
    earned_income: float

    taxable_grants: float
    education_credits: float
    work_study: float

    child_support: float
    cash: float
    investments: float
    business_farm_net_worth: float

    parent_agi: float = 0.0
    parent_tax_paid: float = 0.0
    parent_earned_income: float = 0.0
    parent_child_support: float = 0.0
    parent_cash: float = 0.0
    parent_investments: float = 0.0
    parent_business_farm_net_worth: float = 0.0
