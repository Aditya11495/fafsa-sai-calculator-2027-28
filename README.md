# https://fafsa-sai-calculator-2027-28-cr5dgkz4csa5zjufrd7i6a.streamlit.app/#formula-specific-inputs
# FAFSA 2027–28 SAI & Pell Grant Calculator

A rule-based financial aid calculation system designed to estimate a student's **Student Aid Index (SAI)** and determine potential **Federal Pell Grant eligibility and award amount** for the FAFSA 2027–28 award year.

The system collects FAFSA-style financial and household information, determines the applicable SAI calculation formula, calculates the SAI, and then evaluates Pell Grant eligibility based on the calculated SAI and applicable Pell Grant rules.

> **Development Status:** This project is currently under development and is intended for calculation, testing, and educational purposes. It should not be treated as an official FAFSA filing or federal financial-aid determination.

## 🚀 Project Overview

The application is designed as an end-to-end financial-aid decision engine:


User Information
       ↓
FAFSA-style Questionnaire
       ↓
Dependency / Student Classification
       ↓
SAI Formula Selection
       ↓
SAI Calculation
       ↓
Pell Grant Eligibility
       ↓
Maximum / Calculated / Minimum Pell Evaluation
       ↓
Final Estimated Pell Award
# # Project Architecture
fafsa_sai_2027_28/
│
├── app.py
│
├── engine/
│   ├── __init__.py
│   ├── models.py
│   ├── calculator.py
│   ├── dependency.py
│   ├── payroll.py
│   ├── assets.py
│   ├── rounding.py
│   └── tables.py
│
├── pell/
│   ├── __init__.py
│   ├── pell_engine.py
│   ├── maximum_pell.py
│   ├── calculated_pell.py
│   └── minimum_pell.py
│
├── tables/
│   ├── __init__.py
│   └── pell_parameters.py
│
├── tests/
│   ├── test_engine.py
│   └── test_pell.py
│
├── requirements.txt
└── README.md
