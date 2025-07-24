## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

## calculating the temp and salt anomalies for each month
def calcSodaAnoms(iCESMTEMPFile, iCESMISOFile):

    ## loading in the combined .nc file
    print("Loading file...")
    dsTemp = xr.open_dataset(iCESMTEMPFile)
    dsIso = xr.open_dataset(iCESMISOFile)
    
    ## getting just the month and year
    print("Extracting month and year...")
    dsTemp['month'] = dsTemp['time'].dt.month
    dsTemp['year'] = dsTemp['time'].dt.year

    dsIso['month'] = dsIso['time'].dt.month
    dsIso['year'] = dsIso['time'].dt.year

    dsTemp = dsTemp.assign_coords(year=dsTemp['time'].dt.year,month=dsTemp['time'].dt.month)
    dsIso = dsIso.assign_coords(year=dsIso['time'].dt.year,month=dsIso['time'].dt.month)

    print("Computing monthly mean temp and salinity...")
    iCESMAnomTemp = dsTemp['TEMP'].groupby(['year', 'month']).mean('time')
    iCESMAnomIso = dsIso['R18O'].groupby(['year', 'month']).mean('time')

    print("Computing monthly means...")
    monthlyMeansTemp =  dsTemp['TEMP'].groupby('month').mean('time')
    monthlyMeansIso =  dsIso['R18O'].groupby('month').mean('time')

    print("Calculating anomalies...")
    tempAnomalies = iCESMAnomTemp - monthlyMeansTemp
    saltAnomalies = iCESMAnomIso - monthlyMeansIso

    spatialMeanAnomsTemp = tempAnomalies.mean(dim=['nlat', 'nlon'])
    spatialMeanAnomsTemp = spatialMeanAnomsTemp.sel(z_t = 80, method = 'nearest')
    spatialMeanAnomsIso = saltAnomalies.mean(dim=['nlat', 'nlon'])
    spatialMeanAnomsIso = spatialMeanAnomsIso.sel(z_t = 80, method = 'nearest')

    print("Computing annual anomalies...")
    annualTempAnoms = spatialMeanAnomsTemp.groupby('year').mean('month')
    annualIsoAnoms = spatialMeanAnomsIso.groupby('year').mean('month')

    print("Combining the results...")
    resultAnomalies = xr.Dataset()
    resultAnomalies['temp'] = annualTempAnoms
    resultAnomalies['iso'] = annualIsoAnoms

    print("Returning results.")
    return resultAnomalies

iCESMAnnualAnoms = calcSodaAnoms("./iCESM/selections/tempJONESPORT.nc", "./iCESM/selections/isoJONESPORT.nc")