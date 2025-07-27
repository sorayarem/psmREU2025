## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from seguinOxyIso import d18OAnoms
from seguinAnnualAnomalies import sodaAnnualAnoms
from seguinExpertAnomalies import sodaExpertAnoms
from pyleoclim.utils.tsmodel import ar1_fit
from pyleoclim.utils.correlation import corr_isopersist

## setting the seasonal preference (F:Annual; T:Expert)
season = True

## setting the model preference (1: Temperature; 2:Salinity, 3:Both)
model = 3

## building the pseudocarbonate
def pseudocarbonate(SST, SSS):
    ## define a1 and a2 based on the region (north atlantic)
    a1 = 0.22
    a2 = 0.97002 * 0.55

    ## calculating pseudocarbonate value
    carbonate = a1 * SST + a2 * SSS if model == 3 else (a1 * SST if model == 1 else a2 * SSS)
    return carbonate

## finding the years that are in both datasets
intersect = set(sodaExpertAnoms['year']).intersection(set(d18OAnoms['year'])) if season else set(sodaAnnualAnoms['year']).intersection(set(d18OAnoms['year']))

## only keeping the overlapping years
sodaFiltered = sodaExpertAnoms[sodaExpertAnoms['year'].isin(intersect)] if season else sodaAnnualAnoms[sodaAnnualAnoms['year'].isin(intersect)]
d18OFiltered = d18OAnoms[d18OAnoms['year'].isin(intersect)]

## merge on inner join (based on the year)
merged = pd.merge(sodaFiltered, d18OFiltered, on='year', how='inner')

## computing the pseudocarbonate for each year
if {'year', 'tempAnoms', 'saltAnoms'}.issubset(merged.columns):
    pseudocarbonateData = []
    for _, row in merged.iterrows():
        pseudoCarbonateValue = pseudocarbonate(
            SST=row['tempAnoms'],
            SSS=row['saltAnoms'])
        pseudocarbonateData.append(pseudoCarbonateValue)

    ## converting to a data frame
    merged['pseudocarbonate'] = pseudocarbonateData
    data = merged
else:
    print("Missing required columns in overlapping_df")

## plotting the results of the PSM
plt.figure(figsize=(12, 6))

## plotting the timeseries
plt.plot(data['year'], data['d18OAnoms'], label='shell record', linestyle='-', color='#008080')
plt.plot(data['year'], data['pseudocarbonate'], label='pseudocarbonate', linestyle='-', color='#D2691E')
plt.xlabel('Year')
plt.ylabel('Anomaly Value')

## plotting the correlation
##plt.scatter(data['d18OAnoms'], data['pseudocarbonate'], label='d18OAnoms', color='#008080')

plt.suptitle('Seguin', fontsize = 16, fontweight = 'bold')
method = "Williams et al. Method (Expert Season)" if season else "Williams et al. Method (Annual Season)"
model = "Temperature + Salinity" if model == 3 else ("Temperature Only" if model == 1 else "Salinity Only")
plt.title(method + " | " + model)
plt.legend()
plt.grid(True)
plt.show()

# creating the merged data frame
df = pd.DataFrame({ 'year': data['year'], 'observed': data['d18OAnoms'], 'pseudocarb': data['pseudocarbonate']})

# dropping rows where either observed or pseudocarb is n/a
filter = df.dropna(subset=['observed', 'pseudocarb'])
observed = filter['observed']
pseudocarb = filter['pseudocarb']
years = filter['year']

## finding correlation coefficient (r) and the p-value
r, sig, pValue = corr_isopersist(observed, pseudocarb)
print("Correlation:", r)
print("p-value:", pValue)

## finding root mean squared error
rmse = np.sqrt(((filter['observed'] - filter['pseudocarb']) ** 2).mean())
print("RMSE:", rmse.item())

## finding null-model root mean squared error
nrmse = np.sqrt(((0 - filter['pseudocarb']) ** 2).mean())
print("NRMSE:", nrmse.item())







