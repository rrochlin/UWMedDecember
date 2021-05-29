import pandas as pd


# cleanUp takes sensor data in .txt format and transfers it to .csv format whil removing null timestamps and
# correcting for user specified time errors in hours.
# cutoff: str, formatted according to pandas datetime standards. Will cutoff all data before this time
# timeRectifyingParams: dictionary, input dictionary with {condition1:hours to adjust} format in {str:int} datatype
# filePaths: iterable with the correct filepaths to look for

def autoFix(file,df,start = 0):
    indexErrors={}
    for idx,i in enumerate(df['Date_Time'][start:]):
        try:
            pd.Timestamp(i)
        except:
            print('Error encountered when parsing: ',file)
            print('first index',idx,'  ', 'time value \''+i+'\'')
            # print(len(df['Date_Time']))
            indexErrors[idx]=i
            df.drop(df[df['Date_Time'] == i].index, inplace = True)
            df.reset_index(drop=True)
            df = autoFix(file,df,idx)
            break
    return df




def cleanUp(cutoff,timeRectifyingParams,filePaths,columns,badTimes):

    fData = {}
    mod = {}
    cleaningCutOffTime = pd.Timestamp(cutoff)
    for idx,file in enumerate(filePaths):
        
        # Here we are reading in the data from the sensors. if 'all' was put into the columns variable we just
        # take everything.
        if 'all' in columns:
            df = pd.read_csv(
                file,
                header=1,
                parse_dates = [[0,1]]
                ).dropna(how='all')
        else:
            df = pd.read_csv(
                file,
                header=1,
                parse_dates = [[0,1]],
                usecols = columns
                ).dropna(how='all')
        
        # This takes annoying spaces out of the column names
        df.columns = df.columns.str.replace(' ', '') 

        # Here we assume the sensor path is in the from ./Data\\{sensorname}.txt and shorten it to just be {sensorname}
        name = file[7:len(file)-4]

        # Here we check to see if the date parse was successful. If not we filter out known buggy timestamps
        # if there is a new buggy timestamp that cannot be converted we end the function early and return the pertinent
        # info

        if type(df['Date_Time'][0]) == type('string'):
            for time in badTimes:
                df.drop(df[df['Date_Time'] == time].index, inplace = True)
            # df.drop(df[df['Date_Time'] == '     0/0/0      0:0:0'].index, inplace = True)
            # df.drop(df[df['Date_Time'] == '2165/165/165 165:165:85'].index, inplace = True)
            try:
                df['Date_Time'] = pd.to_datetime(df['Date_Time'])
            except:
                df = autoFix(file,df)
                df['Date_Time'] = pd.to_datetime(df['Date_Time'])
                
            # Here we need to set up our time changing parameters
            # For this instance we need to roll back all sensors by 1 hour
            # except the two BU sensors which needed to be rolled back by
            # 8 hours.
        try:
            offset = timeRectifyingParams[name]
            mod[name] = 'yes'
            # print(x,'yes')
            df['Date_Time'] = df['Date_Time']-pd.Timedelta(hours = offset)
        except KeyError:
            mod[name] = 'no'
            # print(x,'no')

        try:
            df.drop(df[df['Date_Time'] < cleaningCutOffTime].index, inplace = True)

        except TypeError:
            print('TypeError: ')
            return file,df
            # In the instance of a TypeError occuring, we are bascically dealing with
            # the 0 timestamps causing an error in the read_csv parser and not 
            # converting the Date_Time column to timestamp data type.

        fData[name] = df.reset_index(drop=True)

        # ends by printing out the new start and stop times of the data sets
    for label in fData:
        try:
            print(label,'   ',fData[label]['Date_Time'].iloc[0],'    ',fData[label]['Date_Time'].iloc[-1],'     ','mod:',mod[label])
        except:
            print(label,' NO DATA PRESENT    NO DATA PRESENT')
    return fData
