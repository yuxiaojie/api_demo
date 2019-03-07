from datetime import datetime


def timestamp_to_datetime(timestamp):

    if not timestamp:
        return None
    return datetime.fromtimestamp(int(timestamp) / 1000)


def month_delta(date, delta):
    m, y = (date.month+delta) % 12, date.year + (date.month + delta - 1) // 12
    if not m:
        m = 12
    d = min(date.day, [31, 29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m-1])
    return date.replace(day=d, month=m, year=y)

