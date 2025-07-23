import pandas as pd
import numpy as np
from jonesportPSMiCESM import data

observed = data['d18OAnoms'].to_pandas()
pseudocarb = data['pseudocarbonate'].to_pandas()
obs, pseu = observed.align(pseudocarb, join='inner')
corr = obs.corr(pseu)
print("Correlation:", corr)

rmse = np.sqrt(((data['d18OAnoms'] - data['pseudocarbonate']) ** 2).mean())
print("RMSE:", rmse)
