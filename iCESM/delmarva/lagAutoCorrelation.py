import numpy as np
import pyleoclim as pyleo
import matplotlib.pyplot as plt
import pandas as pd
from delmarvaPSMiCESM import data
from pyleoclim.utils.tsmodel import ar1_fit
from pyleoclim.utils.correlation import corr_isopersist

df = pd.DataFrame({'d18OAnoms': data['d18OAnoms'].values,'pseudocarbonate': data['pseudocarbonate'].values}).dropna()
observed = df['d18OAnoms']
pseudocarb = df['pseudocarbonate']

print(corr_isopersist(observed, pseudocarb))
