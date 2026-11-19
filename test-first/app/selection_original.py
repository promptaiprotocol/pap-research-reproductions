def select_rows(rows, *, limit):
    if type(limit) is not int:
        raise TypeError("limit must be an integer")
    if limit < 0 or limit > 100:
        raise ValueError("limit out of range")
    return rows[:limit or 100]
