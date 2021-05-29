import pandas as pd
from datetime import datetime as dt
import re

def fixYearStamp(filePath,incorrectString,date,charTimeStart,charTimeEnd,offset):

    fin = open(filePath,'rt')
    content = fin.readlines()
    fin.close()
    fout = open(filePath,'wt')
    for idx,i in enumerate(content):
        if re.search(incorrectString,i):
            line = (pd.Timestamp(date+i[charTimeStart:charTimeEnd])-pd.Timedelta(hours=offset)).strftime(' %Y/%m/%d, %H:%M:%S') + i[charTimeEnd:]
        else:
            line = i
        fout.write(line)
    fout.close()
    return

### This function will take in a file, the incorrect date string, the date for it in any format, the pivots for the time char array, and the
### hour offset as an integer to correct the function by