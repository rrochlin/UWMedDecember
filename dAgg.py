import pandas as pd
import numpy as np
from datetime import datetime as dt
import os
import glob
import json
import matplotlib.pyplot as plt

all_csv_files = glob.glob("./Data/*.txt")
print("--" + str(all_csv_files))
loops=len(all_csv_files)

data = {}
for idx,x in enumerate(all_csv_files):
    df = pd.read_csv(x,header=1,parse_dates=[[0,1]])
    df.columns = df.columns.str.replace(' ', '') 
    try:
        df.drop(df[df['Date_Time'] < pd.Timestamp('12/22/2020')].index, inplace = True)
    except TypeError:
        df.drop(df[df['Date_Time'] == '     0/0/0      0:0:0'].index, inplace = True)
        print(x)
        df['Date_Time'] = pd.to_datetime(df['Date_Time'])
        df.drop(df[df['Date_Time'] < pd.Timestamp('12/22/2020')].index, inplace = True)
    data[x[7:len(x)-4]] = df.reset_index(drop=True)
