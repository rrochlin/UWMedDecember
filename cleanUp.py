import pandas as pd
import os
import glob


# cleanUp takes sensor data in .txt format and transfers it to .csv format whil removing null timestamps and
# correcting for user specified time errors in hours.
# cutoff: str, formatted according to pandas datetime standards. Will cutoff all data before this time
# timeRectifyingParams: dictionary, input dictionary with {condition1:hours to adjust} format in {str:int} datatype
# filePaths: iterable with the correct filepaths to look for

def cleanUp(cutoff,timeRectifyingParams,filePaths,columns):

    fData = {}
    cleaningCutOffTime = pd.Timestamp(cutoff)
    for idx,x in enumerate(filePaths):
        if 'all' in columns:
            df = pd.read_csv(
                x,
                header=1,
                parse_dates = [[0,1]]
                ).dropna(how='all')
        else:
            df = pd.read_csv(
                x,
                header=1,
                parse_dates = [[0,1]],
                usecols = columns
                ).dropna(how='all')

        df.columns = df.columns.str.replace(' ', '') 

            # Here we need to set up our time changing parameters
            # For this instance we need to roll back all sensors by 1 hour
            # except the two BU sensors which needed to be rolled back by
            # 8 hours.
        for rule in timeRectifyingParams:
            if rule in x:
                try:
                    df['Date_Time'] = df['Date_Time']-pd.Timedelta(hours = timeRectifyingParams[rule])
                except TypeError:
                    df.drop(df[df['Date_Time'] == '     0/0/0      0:0:0'].index, inplace = True)
                    df['Date_Time'] = pd.to_datetime(df['Date_Time'])
                    df['Date_Time'] = df['Date_Time']-pd.Timedelta(hours = timeRectifyingParams[rule])
                break

        df.drop(df[df['Date_Time'] < cleaningCutOffTime].index, inplace = True)
            # In the instance of a TypeError occuring, we are bascically dealing with
            # the 0 timestamps causing an error in the read_csv parser and not 
            # converting the Date_Time column to timestamp data type.

        fData[x[7:len(x)-4]] = df.reset_index(drop=True)

        # ends by printing out the new start and stop times of the data sets
    for x in fData:
        try:
            print(x,'   ',fData[x]['Date_Time'].iloc[0],'    ',fData[x]['Date_Time'].iloc[-1])
        except:
            print(x,' NO DATA PRESENT    NO DATA PRESENT')
    return fData
