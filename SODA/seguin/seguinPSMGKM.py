## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from seguinOxyIso import d18OData
from pyleoclim.utils.tsmodel import ar1_fit
from pyleoclim.utils.correlation import corr_isopersist

## setting up the model arugments
parser = argparse.ArgumentParser(description='Running PSM...')
parser.add_argument('--season', type=int, choices=[0, 1], default=0, help='Seasonal preference (0 = Annual, 1 = Expert)')
parser.add_argument('--model', type=int, choices=[1, 2, 3], default=1, help='Model preference (1=Temp, 2=Salinity, 3=Both)')
args = parser.parse_args()

## setting the seasonal preference (F:Annual; T:Expert)
season = args.season

## setting the model preference (1: Temperature; 2:Salinity, 3:Both)
model = args.model

## method to establish an expert season (oct-sep)
def getExpertYear(time):
    return time.year + int(time.month >= 10)

## building the pseudocarbonate
def pseudocarbonate(SST, SSS, avgTemp, avgSalt):
    ## using the grossman and ku equation (specific to the gulf of maine)
    temp = avgTemp if model == 2 else SST
    sw = (0.5 * avgSalt -17.3) if model == 1 else (0.5 * SSS -17.3)

    ## calculating pseudocarbonate value
    carbonate = ((20.6 - temp)/4.34) + (sw - 0.27)
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

sodaRawAnnual['avgTemp'] = sodaRawAnnual['temp'].mean()
sodaRawExpert['avgTemp'] = sodaRawExpert['temp'].mean()

sodaRawAnnual['avgSalt'] = sodaRawAnnual['salt'].mean()
sodaRawExpert['avgSalt'] = sodaRawExpert['salt'].mean()

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
if {'year', 'temp', 'salt', 'avgTemp', 'avgSalt'}.issubset(merged.columns):
    pseudocarbonateData = []

    for _, row in merged.iterrows():
        pseudoCarbonateValue = pseudocarbonate(
            SST=row['temp'],
            SSS=row['salt'],
            avgTemp=row['avgTemp'],
            avgSalt=row['avgSalt'])
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

filepath = "./figures/soda"
figname = "seguin_SODA_GKM_M" + str(model) + "_" + ("EXP" if season else "ANN") + ".png"
filename = os.path.join(filepath, figname)

plt.suptitle('Seguin', fontsize = 16, fontweight = 'bold')
method = "Grossman and Ku Method (Expert Season)" if season else "Grossman and Ku Method (Annual Season)"
modelType = "Temperature + Salinity" if model == 3 else ("Temperature Only" if model == 1 else "Salinity Only")
plt.title(method + " | " + modelType)
plt.legend()
plt.grid(True)
plt.savefig(filename)

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
rmse = np.sqrt(((filter['observed'] - filter['pseudocarb']) ** 2).mean())
print("RMSE:", rmse.item())

## finding null-model root mean squared error
nrmse = np.sqrt(((0 - filter['observed']) ** 2).mean())
print("NRMSE:", nrmse.item())

## saving the results to an excel file
file = "psmREUStats.xlsx"
site = "Seguin"
equation = "GKM"
data = "SODA"
season = "Expert" if season else "Annual"
method = "Both" if model == 3 else ("Temperature" if model == 1 else "Salinity")

modelResults = {'Site': site, 'Data': data,'Season': season, 'Method': method, 'Equation': equation}

modelResults['r'] = r
modelResults['p-value'] = pValue
modelResults['RMSE'] = rmse.item()
modelResults['NRMSE'] = nrmse.item()

rowToAdd = pd.DataFrame([modelResults])

if os.path.exists(file):
    ## loading the excel file
    previousDF = pd.read_excel(file)

    ## checking if the same row already exists
    match = ((previousDF['Site'] == site) & (previousDF['Data'] == data) & (previousDF['Season'] == season) & 
                (previousDF['Method'] == method) & (previousDF['Equation'] == equation))

    if match.any():
        ## replacing the existing row
        previousDF.loc[match, :] = rowToAdd.values[0]
        print("Row already exists, overwriting file...")
    else:
        ## adding the new row
        previousDF = pd.concat([previousDF, rowToAdd], ignore_index=True)
        print("Row doesn't exist, adding...")

    ## saving the changes to excel
    with pd.ExcelWriter(file, engine='openpyxl', mode='w') as writer:
        previousDF.to_excel(writer, index=False)
else:
    ## creating a new file
    rowToAdd.to_excel(file, index=False, engine='openpyxl')

print("Row added!")





