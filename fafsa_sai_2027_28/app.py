import streamlit as st
from engine.models import FAFSAInput
from engine.dependency import select_formula
from engine.calculator import calculate_sai
from pell.pell_engine import calculate_pell
from tables.pell_parameters import get_poverty_guideline, TEST_MAXIMUM_PELL_2026_27, TEST_MINIMUM_PELL_2026_27

st.set_page_config(page_title="FAFSA 2027–28 SAI & Pell Calculator", page_icon="🎓", layout="wide")

st.title("FAFSA 2027–28 → SAI Calculator")
st.caption("Development build — Formula A/B/C calculation engine")

st.warning(
    "This is the first development build. The calculation engine is separated from the questionnaire. "
    "The complete FAFSA 2027–28 question bank and dependency decision tree will be added before this is treated "
    "as a final eligibility calculator."
)

with st.sidebar:
    st.header("Student classification")
    dependent = st.radio("Dependency status", ["Dependent", "Independent"])
    married = st.checkbox("Student is married")
    has_dependents = st.checkbox("Student has dependents other than spouse")

formula = select_formula(
    dependency_status=dependent.lower(),
    has_dependents=has_dependents
)

st.info(f"Selected SAI formula: **Formula {formula}**")

st.header("Financial inputs")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Income")
    agi = st.number_input("AGI ($)", min_value=0.0, value=0.0, step=100.0)
    ira_keogh = st.number_input("Deductible IRA/KEOGH ($)", min_value=0.0, value=0.0, step=100.0)
    tax_exempt_interest = st.number_input("Tax-exempt interest ($)", min_value=0.0, value=0.0, step=100.0)
    untaxed_ira = st.number_input("Untaxed IRA distributions ($)", min_value=0.0, value=0.0, step=100.0)
    untaxed_pensions = st.number_input("Untaxed pensions ($)", min_value=0.0, value=0.0, step=100.0)
    foreign_income = st.number_input("Foreign income exclusion ($)", min_value=0.0, value=0.0, step=100.0)
    tax_paid = st.number_input("Federal income tax paid ($)", min_value=0.0, value=0.0, step=100.0)
    earned_income = st.number_input("Earned income ($)", min_value=0.0, value=0.0, step=100.0)

with c2:
    st.subheader("Offsets")
    taxable_grants = st.number_input("Taxable grants/scholarships ($)", min_value=0.0, value=0.0, step=100.0)
    education_credits = st.number_input("Education credits ($)", min_value=0.0, value=0.0, step=100.0)
    work_study = st.number_input("Federal Work-Study ($)", min_value=0.0, value=0.0, step=100.0)

    st.subheader("Assets")
    child_support = st.number_input("Child support received ($)", min_value=0.0, value=0.0, step=100.0)
    cash = st.number_input("Cash / savings / checking ($)", min_value=0.0, value=0.0, step=100.0)
    investments = st.number_input("Investments ($)", min_value=0.0, value=0.0, step=100.0)
    business_farm = st.number_input("Business/farm net worth ($)", min_value=0.0, value=0.0, step=100.0)

st.header("Formula-specific inputs")

family_size = st.number_input("Family size", min_value=1, value=2, step=1)

if formula == "A":
    parent_agi = st.number_input("Parent AGI ($)", min_value=0.0, value=0.0, step=100.0)
    parent_tax_paid = st.number_input("Parent federal income tax paid ($)", min_value=0.0, value=0.0, step=100.0)
    parent_earned_income = st.number_input("Parent combined earned income ($)", min_value=0.0, value=0.0, step=100.0)
    parent_child_support = st.number_input("Parent child support received ($)", min_value=0.0, value=0.0, step=100.0)
    parent_cash = st.number_input("Parent cash/savings/checking ($)", min_value=0.0, value=0.0, step=100.0)
    parent_investments = st.number_input("Parent investments ($)", min_value=0.0, value=0.0, step=100.0)
    parent_business_farm = st.number_input("Parent business/farm net worth ($)", min_value=0.0, value=0.0, step=100.0)
else:
    parent_agi = parent_tax_paid = parent_earned_income = 0.0
    parent_child_support = parent_cash = parent_investments = parent_business_farm = 0.0


st.header("Pell Grant inputs")

st.info(
    "Pell eligibility is evaluated after SAI. The 2027–28 eligibility rules use "
    "the applicable 2025 HHS poverty guideline. The 2027–28 dollar award amounts "
    "are kept editable until officially published."
)

p1, p2 = st.columns(2)

with p1:
    pell_state = st.selectbox(
        "State category for poverty guideline",
        ["Other", "Alaska", "Hawaii"],
        index=0,
        help="Use 'Other' for the 48 contiguous states and DC."
    )

    single_parent = st.checkbox(
        "Student/parent is a single parent"
    )

    is_parent = st.checkbox(
        "Student is a parent"
    )

    tax_filing_required = st.checkbox(
        "Required to file a federal income tax return",
        value=True,
        help="For Formula A this represents the parent(s); for B/C it represents the student/spouse."
    )

with p2:
    use_test_awards = st.checkbox(
        "Use 2026–27 Pell amounts for testing",
        value=True,
        help="Temporary testing only. Replace these with official 2027–28 award-year amounts when published."
    )

    if use_test_awards:
        max_pell_award = st.number_input(
            "Maximum Pell award used for test ($)",
            min_value=1.0,
            value=float(TEST_MAXIMUM_PELL_2026_27),
            step=5.0,
        )
        min_pell_award = st.number_input(
            "Minimum Pell award used for test ($)",
            min_value=1.0,
            value=float(TEST_MINIMUM_PELL_2026_27),
            step=5.0,
        )
    else:
        max_pell_award = st.number_input(
            "Official Maximum Pell award ($)",
            min_value=1.0,
            value=1.0,
            step=5.0,
        )
        min_pell_award = st.number_input(
            "Official Minimum Pell award ($)",
            min_value=1.0,
            value=1.0,
            step=5.0,
        )

    cost_of_attendance = st.number_input(
        "Cost of Attendance ($)",
        min_value=0.0,
        value=10000.0,
        step=100.0,
    )

    enrollment_intensity_pct = st.number_input(
        "Enrollment intensity (%)",
        min_value=1.0,
        max_value=100.0,
        value=100.0,
        step=5.0,
    )

poverty_guideline = get_poverty_guideline(
    pell_state,
    int(family_size)
)

st.caption(
    f"Applicable 2025 poverty guideline used by the Pell test: "
    f"${poverty_guideline:,}"
)

st.header("Calculate")

if st.button("Calculate SAI", type="primary"):
    data = FAFSAInput(
        formula=formula,
        married=married,
        family_size=family_size,
        agi=agi,
        ira_keogh=ira_keogh,
        tax_exempt_interest=tax_exempt_interest,
        untaxed_ira=untaxed_ira,
        untaxed_pensions=untaxed_pensions,
        foreign_income_exclusion=foreign_income,
        tax_paid=tax_paid,
        earned_income=earned_income,
        taxable_grants=taxable_grants,
        education_credits=education_credits,
        work_study=work_study,
        child_support=child_support,
        cash=cash,
        investments=investments,
        business_farm_net_worth=business_farm,
        parent_agi=parent_agi,
        parent_tax_paid=parent_tax_paid,
        parent_earned_income=parent_earned_income,
        parent_child_support=parent_child_support,
        parent_cash=parent_cash,
        parent_investments=parent_investments,
        parent_business_farm_net_worth=parent_business_farm,
    )

    result = calculate_sai(data)

    pell_result = calculate_pell(
        sai=result["sai"],
        dependency_status=dependent.lower(),
        single_parent=single_parent,
        is_parent=is_parent,
        agi=parent_agi if formula == "A" else agi,
        foreign_income_exclusion=foreign_income,
        poverty_guideline=poverty_guideline,
        tax_filing_required=tax_filing_required,
        maximum_pell_award=max_pell_award,
        minimum_pell_award=min_pell_award,
        cost_of_attendance=cost_of_attendance,
        enrollment_intensity=enrollment_intensity_pct / 100,
    )

    st.subheader("SAI Result")
    a, b, c = st.columns(3)
    a.metric("Formula", result["formula"])
    b.metric("Calculated SAI", f'{result["sai"]:,}')
    c.metric("Status", "Development calculation")

    st.json(result)

    st.subheader("Pell Grant Result")

    p1, p2, p3 = st.columns(3)
    p1.metric(
        "Pell Eligibility",
        "YES" if pell_result["pell_eligible"] else "NO"
    )
    p2.metric(
        "Pell Type",
        pell_result["pell_type"] or "Not eligible"
    )
    p3.metric(
        "Scheduled Pell Award",
        f'${pell_result["scheduled_award"]:,}'
    )

    if pell_result["pell_eligible"]:
        st.success(
            f"Estimated scheduled Pell Grant: "
            f"${pell_result["scheduled_award"]:,}"
        )
    else:
        st.error("Student does not qualify under the tested Pell paths.")

    with st.expander("Pell calculation details"):
        st.json(pell_result)
