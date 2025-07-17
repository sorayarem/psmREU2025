import pandas as pd
import numpy as np
from bivalvePSMSODA import data
from oxyIsoAnomalies import d18OData

print(d18OData)
print(data[['year', 'pseudocarbonate']])

matrix = np.corrcoef(d18OData['delmarvaIso'], data[['year', 'pseudocarbonate']])
pearson = matrix[0, 1]

print(f"Pearson Correlation Coefficient: {pearson}")