import numpy as np


def pivotid(df1, l, n1, n2):
    if l - n1 < 0 or l + n2 >= len(df1):
        return 0

    pividlow = 1
    pividhigh = 1
    for i in range(l - n1, l + n2 + 1):
        if df1.Low[l] > df1.Low[i]:
            pividlow = 0
        if df1.High[l] < df1.High[i]:
            pividhigh = 0
    if pividlow and pividhigh:
        return 3
    elif pividlow:
        return 1
    elif pividhigh:
        return 2
    else:
        return 0


def pointpos(x):
    if x["Pivot"] == 1:
        return x["Low"] - 1e-3
    elif x["Pivot"] == 2:
        return x["High"] + 1e-3
    else:
        return np.nan
