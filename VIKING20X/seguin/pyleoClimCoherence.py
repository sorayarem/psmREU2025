import numpy as np
import pandas as pd
import pyleoclim as pyleo
import matplotlib.pyplot as plt
from scipy.stats import chi2
from seguinPSMWEA import merged
from pyleoclim.utils.spectral import mtm

# creating the merged data frame
df = pd.DataFrame({ 'year': merged['year'], 'observed': merged['d18OAnoms'], 'pseudocarb': merged['pseudocarbonate']})

# dropping rows where either observed or pseudocarb is n/a
filter = df.dropna(subset=['observed', 'pseudocarb'])
observed = filter['observed']
pseudocarb = filter['pseudocarb']
years = filter['year']

observedMTM = mtm(observed, years)
pseudocarbMTM = mtm(pseudocarb, years)

f1 = observedMTM['freq']
psdObserved = observedMTM['psd']

f2 = pseudocarbMTM['freq']
psdPseudo = pseudocarbMTM['psd']

## computing 95% significance threshold
alpha = 0.05
sigObserved = 16 * psdObserved / chi2.ppf(alpha / 2, 16)
sigPseudo = 16 * psdPseudo / chi2.ppf(alpha / 2, 16)

plt.figure(figsize=(10, 6))
plt.semilogy(f1, psdObserved, label='Observed', color='blue')
plt.semilogy(f2, psdPseudo, label='Pseudocarbonate', color='green')
plt.semilogy(f1, sigObserved, '--', color='blue', label='95% Significance Level')
plt.semilogy(f2, sigPseudo, '--', color='green', label='95% Significance Level')
plt.xlabel('Frequency (1/year)')
plt.ylabel('Power Spectral Density')
plt.title('MTM Power Spectral Density')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

