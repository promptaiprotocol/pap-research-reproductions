import pytest
from app.selection import select_rows


@pytest.mark.parametrize("limit", [0, 2])
def test_empty_input(limit):
    assert select_rows([], limit=limit) == []


def test_upper_limit_preserves_first_100_rows():
    rows = [f"row-{i}" for i in range(101)]
    expected = [f"row-{i}" for i in range(100)]
    assert select_rows(rows, limit=100) == expected
    assert rows == [*expected, "row-100"]
