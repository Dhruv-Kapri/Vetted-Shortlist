from scripts.dld_check import SQFT_PER_SQM, area_match


def test_area_match_converts_sqft_and_applies_relative_tolerance() -> None:
    assert area_match(1076.39, 100.0)  # 1076.39 sqft is 100 sqm
    assert area_match(100 * SQFT_PER_SQM * 1.049, 100.0)  # just inside +5%
    assert not area_match(100 * SQFT_PER_SQM * 1.051, 100.0)  # just outside
    assert area_match(100 * SQFT_PER_SQM * 0.951, 100.0)  # just inside -5%
    assert not area_match(100 * SQFT_PER_SQM * 0.949, 100.0)  # just outside -5%
    assert not area_match(1000.0, 0.0)  # missing DLD area never matches
