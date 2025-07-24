import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from longIslandPSMSODA import data

df = pd.DataFrame({'d18OAnoms': data['d18OAnoms'], 'pseudocarbonate': data['pseudocarbonate']}).dropna()

r, pValue = pearsonr(df['d18OAnoms'], df['pseudocarbonate'])
print(f"Correlation: {r}, p-value: {pValue}")

rmse = np.sqrt(((data['d18OAnoms'] - data['pseudocarbonate']) ** 2).mean())
print("RMSE:", rmse)

nrmse = np.sqrt(((0 - data['pseudocarbonate']) ** 2).mean())
print("NRMSE:", nrmse)