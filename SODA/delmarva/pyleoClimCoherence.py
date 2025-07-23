import numpy as np
import pyleoclim as pyleo
import matplotlib.pyplot as plt
import pandas as pd
from delmarvaPSMSODA import data
from pyleoclim.utils.spectral import mtm


observed = data['d18OAnoms']
pseudocarb = data['pseudocarbonate']
years = data['year']

observedMTM = mtm(observed, years)
pseudocarbMTM = mtm(pseudocarb, years)

f1 = observedMTM['freq']
psdObserved = observedMTM['psd']

f2 = pseudocarbMTM['freq']
psdPseudo = pseudocarbMTM['psd']

'''
coherence = observed.wavelet_coherence(pseudocarb)
coh_sig = coherence.signif_test(number=10)
coh_sig.dashboard()
'''

plt.figure(figsize=(10, 6))
plt.plot(f1, psdObserved, label='Observed', color='blue')
plt.plot(f2, psdPseudo, label='Pseudocarbonate', color='green')

plt.xlabel('Frequency (1/year)')
plt.ylabel('Power Spectral Density')
plt.title('MTM Power Spectral Density')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
