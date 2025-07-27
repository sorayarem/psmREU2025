## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import numpy as np
from isleOxyIso import d18OData

def pseudocarbonate(SST, SSS, species="default", data_to_use=2, verbose=False):
    ## define a1 and a2 based on the region (north atlantic)
    temp = SST
    sw = (0.5 * SSS -17.3)

    ## calculating pseudocarbonate value
    carbonate = ((20.6 - temp)/4.34) + (sw - 0.27)

    return carbonate

sodaRaw = pd.read_csv("./csv_clean/isleAuHautCSV.csv")

## converting from string to date-time object
print("Converting time column...")
sodaRaw['time'] = pd.to_datetime(sodaRaw['time'], format= 'mixed')
sodaRaw['time'] = sodaRaw['time'].dt.to_period('M')

## getting just the month and year
print("Extracting month and year...")
sodaRaw['year'] = sodaRaw['time'].dt.year

print("Computing annual means...")
sodaRaw = sodaRaw.groupby('year', as_index=False).agg({'temp': 'mean', 'salt': 'mean'})

## finding the years that are in both datasets
intersect = set(sodaRaw['year']).intersection(set(sodaRaw['year']))

## only keeping the overlapping years
sodaFiltered = sodaRaw[sodaRaw['year'].isin(intersect)]
d18OFiltered = d18OData[d18OData['year'].isin(intersect)]

## merge on inner join (based on the year)
merged = pd.merge(sodaFiltered, d18OFiltered, on='year', how='inner')
print(merged)

if {'year', 'temp', 'salt'}.issubset(merged.columns):
    ## computing the pseudocarbonate for each year
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

import pandas as pd
import matplotlib.pyplot as plt


plt.figure(figsize=(12, 6))
##plt.plot(data['year'], data['isleAuHautIso'], label='jonesportIso', linestyle='-', color='#008080')
##plt.plot(data['year'], data['pseudocarbonate'], label='pseudocarbonate', linestyle='-', color='#D2691E')
plt.scatter(data['isleAuHautIso'], data['pseudocarbonate'], label='d18OAnoms', color='#008080')
plt.xlabel('Time')
plt.ylabel('Anomaly Value')
plt.title('Isle Au Haut - d18O-carb and d18O-pseudo Over Time')
plt.legend()
plt.grid(True)

plt.show()

