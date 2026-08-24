# FAFSA 2027–28 SAI Calculator — Development Build

This project is the first coding stage of the FAFSA → Formula A/B/C → SAI → Pell system.

## Current scope

- Formula A/B/C selection engine
- Common income additions/offsets
- Payroll tax allowance
- 2027–28 business/farm adjustment
- Formula A parent contribution structure
- Formula B calculation structure
- Formula C calculation structure
- 2027–28 AAI tables represented in code
- Central SAI bounds
- Streamlit test interface
- Unit tests

## Important

This is NOT yet the final FAFSA eligibility product.

The complete 2027–28 FAFSA question bank, dependency-status decision tree, all conditional questions, Maximum Pell Indicator logic, Minimum Pell Indicator logic, Pell flag logic, poverty-guideline tables, and final award calculation still need to be mapped from the official 2027–28 FAFSA Specifications/SAI materials before production use.

The architecture intentionally separates:

1. questionnaire
2. dependency/formula decision
3. mathematical engine
4. Pell eligibility engine
5. year-specific parameter tables

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Run tests:

```bash
pytest
```


## Pell Grant section (V0.2)

Pell eligibility is now evaluated after SAI. The app includes Maximum Pell, Calculated Pell, and Minimum Pell paths, plus poverty-guideline lookup, COA, and enrollment-intensity inputs. The 2027–28 award-year dollar amounts are intentionally editable because final amounts must be loaded when officially published. A temporary 2026–27 test mode is provided for development/testing only.
