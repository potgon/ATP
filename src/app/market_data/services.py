import datetime

def is_forex_day(date=None) -> bool:
    """
    Determines whether Forex market is operating
    Currently accounting for: Closed from 10PM UTC Friday to 10PM UTC Sunday
    If no date is provided, today's date is used
    """
    if not date:
        date = datetime.datetime.utcnow()

    weekday = date.weekday
    time = date.time()

    if weekday == 4 and time >= datetime.time(22,0):
        return False
    elif weekday == 5:
        return False
    elif weekday == 6 and time < datetime.time(22,0):
        return False

    return True
