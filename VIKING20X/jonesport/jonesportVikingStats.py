import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from gkExperiment import data

df = pd.DataFrame({'d18OData': data['d18OData'].values,'pseudocarbonate': data['pseudocarbonate'].values}).dropna()
r, pValue = pearsonr(df['d18OData'], df['pseudocarbonate'])
print(f"Correlation: {r}, p-value: {pValue}")

rmse = np.sqrt(((data['d18OData'] - data['pseudocarbonate']) ** 2).mean())
print("RMSE:", rmse.item())

nrmse = np.sqrt(((0 - data['pseudocarbonate']) ** 2).mean())
print("NRMSE:", nrmse.item())