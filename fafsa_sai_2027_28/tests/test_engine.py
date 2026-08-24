from engine.dependency import select_formula
from engine.assets import adjusted_business_farm, asset_contribution
from engine.tables import parent_aai

def test_formula_selection():
    assert select_formula("dependent", False) == "A"
    assert select_formula("independent", False) == "B"
    assert select_formula("independent", True) == "C"

def test_business_farm_example():
    assert adjusted_business_farm(200000) == 82000

def test_asset_example():
    assert asset_contribution(65000, 0.12) == 7800

def test_aai_table():
    assert parent_aai(22600) == 4972
    assert parent_aai(45600) == 12336
