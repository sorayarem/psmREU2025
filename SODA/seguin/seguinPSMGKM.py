## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from seguinOxyIso import d18OData
from pyleoclim.utils.tsmodel import ar1_fit
from pyleoclim.utils.correlation import corr_isopersist

## setting the seasonal preference (F:Annual; T:Expert)
season = True

## setting the model preference (1: Temperature; 2:Salinity, 3:Both)
model = 3

## method to establish an expert season (oct-sep)
def getExpertYear(time):
    return time.year + int(time.month >= 10)

## building the pseudocarbonate
def pseudocarbonate(SST, SSS):
    ## using the grossman and ku equation (specific to the gulf of maine)
    temp = SST
    sw = (0.5 * SSS -17.3)

    ## calculating pseudocarbonate value
    carbonate = ((20.6 - temp)/4.34) + (sw - 0.27) if model == 3 else (((20.6 - temp)/4.34) - 0.27) if model == 1 else ((20.6/4.34) + (sw - 0.27))
    return carbonate

## loading in the data
sodaRaw = pd.read_csv("./csv_clean/seguinCSV.csv")

## converting from string to date-time object and to expert season
print("Converting time column...")
sodaRaw['time'] = pd.to_datetime(sodaRaw['time'], format= 'mixed')
sodaRaw['expertYear'] = sodaRaw['time'].apply(getExpertYear)
sodaRaw['time'] = sodaRaw['time'].dt.to_period('M')

## getting just the month and year
print("Extracting month and year...")
sodaRaw['year'] = sodaRaw['time'].dt.year

## computing the mean for each overall year
print("Computing annual means...")
sodaRawAnnual = sodaRaw.groupby('year', as_index=False).agg({'temp': 'mean', 'salt': 'mean'})
sodaRawExpert = sodaRaw.groupby('expertYear', as_index=False).agg({'temp': 'mean', 'salt': 'mean'})

## removing the first and last years from the dataset
yearsValid = sodaRawExpert['expertYear'].iloc[1:-1]
sodaRawExpert = sodaRawExpert[sodaRawExpert['expertYear'].isin(yearsValid)]

## finding the years that are in both datasets
intersectAnnual = set(sodaRawAnnual['year']).intersection(set(d18OData['year']))
intersectExpert = set(sodaRawExpert['expertYear']).intersection(set(d18OData['year']))

## only keeping the overlapping years (annual)
sodaFilteredAnnual = sodaRawAnnual[sodaRawAnnual['year'].isin(intersectAnnual)]
d18OFilteredAnnual = d18OData[d18OData['year'].isin(intersectAnnual)]

## only keeping the overlapping years (expert)
sodaFilteredExpert = sodaRawExpert[sodaRawExpert['expertYear'].isin(intersectExpert)]
d18OFilteredExpert = d18OData[d18OData['year'].isin(intersectExpert)]

## merge on inner join (based on the year)
mergedAnnual = pd.merge(sodaFilteredAnnual, d18OFilteredAnnual, on='year', how='inner')
mergedExpert = pd.merge(sodaFilteredExpert, d18OFilteredExpert, left_on='expertYear', right_on='year', how='inner')

## setting the seasonal switch
merged = mergedExpert if season else mergedAnnual

## computing the pseudocarbonate for each year
if {'year', 'temp', 'salt'}.issubset(merged.columns):
    pseudocarbonateData = []
    for _, row in merged.iterrows():
        pseudoCarbonateValue = pseudocarbonate(
            SST=row['temp'],
            SSS=row['salt'])
        pseudocarbonateData.append(pseudoCarbonateValue)

    ## converting to a data frame
    merged['pseudocarbonate'] = pseudocarbonateData
    data = merged
else:
    print("Missing required columns in overlapping_df")

## plotting the results of the PSM
plt.figure(figsize=(12, 6))

## plotting the timeseries
plt.plot(data['year'], data['seguinIso'], label='shell record', linestyle='-', color='#008080')
plt.plot(data['year'], data['pseudocarbonate'], label='pseudocarbonate', linestyle='-', color='#D2691E')
plt.xlabel('Year')
plt.ylabel('Value')

## plotting the correlation
##plt.scatter(data['seguinIso'], data['pseudocarbonate'], label='d18OAnoms', color='#008080')

plt.suptitle('Seguin', fontsize = 16, fontweight = 'bold')
method = "Grossman and Ku Method (Expert Season)" if season else "Grossman and Ku Method (Annual Season)"
model = "Temperature + Salinity" if model == 3 else ("Temperature Only" if model == 1 else "Salinity Only")
plt.title(method + " | " + model)
plt.legend()
plt.grid(True)
plt.show()

# creating the merged data frame
df = pd.DataFrame({ 'year': data['year'], 'observed': data['seguinIso'], 'pseudocarb': data['pseudocarbonate']})

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
rmse = np.sqrt(((data['seguinIso'] - data['pseudocarbonate']) ** 2).mean())
print("RMSE:", rmse)

## finding null-model root mean squared error
nrmse = np.sqrt(((data['seguinIso'] - 0) ** 2).mean())
print("NRMSE:", nrmse)

## finding the effective degrees of freedom
rA = ar1_fit(observed, years)
rB = ar1_fit(pseudocarb, years)
dT = ((1+rA*rB)/(1-rA*rB))
nEff = (data['seguinIso'].shape)/dT
print("N-eff:", nEff)
print("df Used:", min(nEff, data['seguinIso'].shape[0] - 1))




