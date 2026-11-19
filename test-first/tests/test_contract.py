import pytest
from app.selection import select_rows


@pytest.mark.parametrize("limit,expected", [
    (0, []),
    (1, ["B"]),
    (2, ["B", "A"]),
    (4, ["B", "A", "A"]),
    (100, ["B", "A", "A"]),
])
def test_selection_contract(limit, expected):
    rows = ["B", "A", "A"]
    assert select_rows(rows, limit=limit) == expected
    assert rows == ["B", "A", "A"]


@pytest.mark.parametrize("limit", [-1, 101])
def test_rejects_out_of_range(limit):
    with pytest.raises(ValueError):
        select_rows(["A"], limit=limit)


@pytest.mark.parametrize("limit", [None, "2", True])
def test_rejects_non_integer(limit):
    with pytest.raises(TypeError):
        select_rows(["A"], limit=limit)
