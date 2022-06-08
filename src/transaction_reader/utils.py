from datetime import datetime


def parse_date(value, *, fmt="%m/%d"):
    """Parsers the value in the corresponding format.
    Args:
        value: An string with date information. For example: 6/6
        fmt: An string with time format to be parser.
    Returns:
        A datetime object.
    """
    return datetime.strptime(value, fmt)


def group_by_month(item):
    """Returns the transaction month key."""
    return item.Date.month


def group_by_kind(item):
    """Returns the transaction kind key."""
    return item.Transaction.kind
