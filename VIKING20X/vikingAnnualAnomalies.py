## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

## calculating the temp and salt anomalies for each month
def calcSodaAnoms(vikingTEMPFile, vikingSALINEFile):

    ## loading in the combined .nc file
    print("Loading file...")
    dsTemp = xr.open_dataset(vikingTEMPFile)
    dsSaline = xr.open_dataset(vikingSALINEFile)
    
    ## getting just the month and year
    print("Extracting month and year...")
    dsTemp['month'] = dsTemp['time_counter'].dt.month
    dsTemp['year'] = dsTemp['time_counter'].dt.year

    dsSaline['month'] = dsSaline['time_counter'].dt.month
    dsSaline['year'] = dsSaline['time_counter'].dt.year

    dsTemp = dsTemp.assign_coords(year=dsTemp['time_counter'].dt.year,month=dsTemp['time_counter'].dt.month)
    dsSaline = dsSaline.assign_coords(year=dsSaline['time_counter'].dt.year,month=dsSaline['time_counter'].dt.month)

    print("Computing monthly mean temp and salinity...")
    vikingAnomTemp = dsTemp['votemper'].groupby(['year', 'month']).mean('time_counter')
    vikingAnomSaline = dsSaline['vosaline'].groupby(['year', 'month']).mean('time_counter')


    print("Computing monthly means...")
    monthlyMeansTemp =  dsTemp['votemper'].groupby('month').mean('time_counter')
    monthlyMeansSaline =  dsSaline['vosaline'].groupby('month').mean('time_counter')


    print("Calculating anomalies...")
    tempAnomalies = vikingAnomTemp - monthlyMeansTemp
    saltAnomalies = vikingAnomSaline - monthlyMeansSaline

    spatialMeanAnomsTemp = tempAnomalies.mean(dim=['deptht', 'y', 'x'])
    spatialMeanAnomsSaline = saltAnomalies.mean(dim=['deptht', 'y', 'x'])

    print("Computing annual anomalies...")
    annualTempAnoms = spatialMeanAnomsTemp.groupby('year').mean('month')
    annualSalineAnoms = spatialMeanAnomsSaline.groupby('year').mean('month')

    print("Combining the results...")
    resultAnomalies = annualTempAnoms
    resultAnomalies['salt'] = annualSalineAnoms

    print("Returning results.")
    return resultAnomalies

vikingAnnualAnoms = calcSodaAnoms("viking_ALLTEMP.nc", "viking_ALLSALINE.nc")
years = vikingAnnualAnoms['year'].values
temps = vikingAnnualAnoms.values
salts = vikingAnnualAnoms['salt'].values

plt.figure(figsize=(10, 5))
plt.plot(years, temps, label='Temp Anomalies', linestyle='-', color='#008080')  # Teal
plt.plot(years, salts, label='Salt Anomalies', linestyle='-', color='#D2691E')  # Dark Orange
plt.xlabel('Time')
plt.ylabel('Anomaly Value')
plt.title('Temperature and Salinity Anomalies Over Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()