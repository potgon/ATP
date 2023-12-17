import datetime

def is_forex_day(date=None) -> bool:
    """
    Calculates current day (0->Monday | 6->Sunday) and returns a bool indicating whether Forex market is operating
    If no date is provided, today's date is used
    """
    if date:
        if date >= 5:
            return False
    else:
        if datetime.datetime.today().weekday() >= 5:
            return False
    return True
    