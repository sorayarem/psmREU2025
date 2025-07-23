import pandas as pd
import numpy as np
from georgesPSMSODA import data

## calculating correlation coefficient
corr = data['d18OAnoms'].corr(data['pseudocarbonate'])
print("Correlation coefficient:", corr)

rmse = np.sqrt(((data['d18OAnoms'] - data['pseudocarbonate']) ** 2).mean())
print("RMSE:", rmse)
