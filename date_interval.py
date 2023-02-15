from datetime import datetime, timedelta


def get_interval(days_ago: int):
    today = datetime.today()
    start = datetime.today() - timedelta(days=10)

    interval = f'{start.day}%2F{start.month}%2F{start.year}%20-%20{today.day}%2F{today.month}%2F{today.year}'
    return interval
