from app.selection import select_rows


def test_zero_limit_returns_no_rows():
    rows = ["A", "B", "C"]
    assert select_rows(rows, limit=0) == []
    assert rows == ["A", "B", "C"]
