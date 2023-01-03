import pytest

from nemdata.mmsdm import find_mmsdm_table


def test_find_mmsdm_table():
    table = find_mmsdm_table("trading-price")
    assert table.name == "trading-price"

    with pytest.raises(ValueError) as err:
        find_mmsdm_table("missing-table")
        assert "missing-table not found" in str(err)
