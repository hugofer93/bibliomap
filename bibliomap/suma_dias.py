from datetime import timedelta

(MON, TUE, WED, THU, FRI, SAT, SUN) = range(7)

def addworkdays(start, days, holidays=(), workdays=(MON,TUE,WED,THU,FRI)):
    weeks, days = divmod(days, len(workdays))
    result = start + timedelta(weeks=weeks)
    lo, hi = min(start, result), max(start, result)
    count = len([h for h in holidays if h >= lo and h <= hi])
    days += count * (-1 if days < 0 else 1)
    for _ in range(days):
        result += timedelta(days=1)
        while result in holidays or result.weekday() not in workdays:
            result += timedelta(days=1)
    return result