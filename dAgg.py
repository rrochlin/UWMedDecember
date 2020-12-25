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
    data[x[7:len(x)-4]] = pd.read_csv(x,header=1)