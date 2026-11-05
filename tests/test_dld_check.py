from scripts.dld_check import SQFT_PER_SQM, area_match, clean_sales


def test_area_match_converts_sqft_and_applies_relative_tolerance() -> None:
    assert area_match(1076.39, 100.0)  # 1076.39 sqft is 100 sqm
    assert area_match(100 * SQFT_PER_SQM * 1.049, 100.0)  # just inside +5%
    assert not area_match(100 * SQFT_PER_SQM * 1.051, 100.0)  # just outside
    assert area_match(100 * SQFT_PER_SQM * 0.951, 100.0)  # just inside -5%
    assert not area_match(100 * SQFT_PER_SQM * 0.949, 100.0)  # just outside -5%
    assert not area_match(1000.0, 0.0)  # missing DLD area never matches


def _sale(tid: str, value: str, proc: str = "100", actual: str = "100", sub: str = "Flat", plan: str = "Ready") -> dict[str, str]:
    return {"TRANSACTION_NUMBER": tid, "TRANS_VALUE": value, "PROCEDURE_AREA": proc, "ACTUAL_AREA": actual,
            "PROP_SB_TYPE_EN": sub, "IS_OFFPLAN_EN": plan}


def test_clean_sales_drops_partial_shares_odd_values_duplicates_and_non_ready() -> None:
    rows = [_sale("ok", "1500000"), _sale("ok", "1500000"),  # duplicate id
            _sale("half", "1250000", proc="60.41", actual="120.82"),  # half-share transfer
            _sale("tiny", "40505"), _sale("shop", "2000000", sub="Shop"), _sale("plan", "2000000", plan="Off-Plan"),
            _sale("edge", "1500000", proc="100.9")]  # within 1%: kept
    kept, dropped = clean_sales(rows)
    assert [r["TRANSACTION_NUMBER"] for r in kept] == ["ok", "edge"]
    assert sum(dropped.values()) == 5
    assert dropped["partial share (areas differ >1%)"] == 1
