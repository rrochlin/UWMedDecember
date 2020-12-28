import pandas as pd
import numpy as np


def fillDf(df, freq, start, end, cutoff):
    if start:
        startTime = pd.Timestamp(start)
    else:
        startTime = df.values[0][0]

    if end:
        endTime = pd.Timestamp(end)
    else:
        endTime = df.values[-1][0] + pd.Timedelta(seconds=10)

    volatility = 0
    padding = 0
    nochange = 0

    threshold = pd.Timedelta(seconds=cutoff)

    index = pd.date_range(startTime, endTime, freq=freq)
    columns = df.columns

    count = 0

    overall = []

    for idx, i in enumerate(df.values):
        oldCount = count

        try:
            while i[0] >= index[count]:
                count += 1
        except IndexError:
            continue

        val = count - oldCount

        # if sensor measurements are more frequent than the sampling rate we just skip them
        if not val:
            continue

        if threshold < (index[count] - index[oldCount]):
            if not idx:
                temp = df.values[0][1:]
            else:
                temp = df.values[idx - 1][1:]

            # if the time gap is over the threshold entries are 0 padded instead of interpolated
            for step, ovrwrt in enumerate(range(oldCount, count)):
                padding += 1
                tempdata = np.concatenate(
                    (np.array([index[ovrwrt]]),
                     np.floor(np.array(temp * 0))), 0
                )
                overall.append(tempdata)
            val = 0

        # might error on first value

        if val and val - 1:

            # time gaps < threshold will be linearly interpolated

            if not idx:
                temp = df.values[0][1:]
            else:
                temp = df.values[idx - 1][1:]
            inc = (i[1:] - temp) / val

            for step, ovrwrt in enumerate(range(oldCount, count)):
                volatility += 1
                tempdata = np.concatenate(
                    (np.array([index[ovrwrt]]), np.floor(
                        np.array(temp + inc * step))),
                    0,
                )
                overall.append(tempdata)

        elif val:
            nochange += 1
            temp = i[1:]
            tempdata = np.concatenate(
                (np.array([index[oldCount]]), np.floor(np.array(temp))), 0
            )
            overall.append(tempdata)


    total = len(overall)

    if total:
        accuracy = ["% of values from interpolation : " + str(np.round(volatility/total*100, 3)),
                    "% of values from 0-padding : " +
                    str(np.round(padding/total*100, 3)),
                    "% of values not changed : " + str(np.round(nochange/total*100, 3))]
    else:
        accuracy = 'NO DATA'

    newDF = pd.DataFrame(overall, columns=columns)

    return newDF, accuracy
