import datetime

def checkTime(d1,d2):
    t = d2-d1
    t_val = int(t.total_seconds())
    if t_val > 10:
        return False
    return True

