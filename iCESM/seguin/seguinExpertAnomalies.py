## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

def getExpertYear(time):
    return time.year - int(time.month < 10)

## calculating the temp and salt anomalies for each month
def calcSodaAnoms(iCESMTEMPFile, iCESMSALINEFile):

    ## loading in the combined .nc file
    print("Loading file...")
    dsTemp = xr.open_dataset(iCESMTEMPFile)
    dsSaline = xr.open_dataset(iCESMSALINEFile)
    
    ## getting just the month and year
    print("Extracting month and year...")
    dsTemp['month'] = dsTemp['time'].dt.month
    dsTemp['year'] = dsTemp['time'].dt.year

    dsSaline['month'] = dsSaline['time'].dt.month
    dsSaline['year'] = dsSaline['time'].dt.year

    expertTemp = xr.apply_ufunc(getExpertYear, dsTemp['time'], vectorize=True)
    expertSaline = xr.apply_ufunc(getExpertYear, dsSaline['time'], vectorize=True)

    dsTemp = dsTemp.assign_coords(year=expertTemp)
    dsSaline = dsSaline.assign_coords(year=expertSaline)

    dsTemp = dsTemp.assign_coords(month=dsTemp['time'].dt.month)
    dsSaline = dsSaline.assign_coords(month=dsSaline['time'].dt.month)

    print("Computing monthly mean temp and salinity...")
    iCESMAnomTemp = dsTemp['TEMP'].groupby(['year', 'month']).mean('time')
    iCESMAnomSaline = dsSaline['SALT'].groupby(['year', 'month']).mean('time')

    print("Computing monthly means...")
    monthlyMeansTemp =  dsTemp['TEMP'].groupby('month').mean('time')
    monthlyMeansSaline =  dsSaline['SALT'].groupby('month').mean('time')


    print("Calculating anomalies...")
    tempAnomalies = iCESMAnomTemp - monthlyMeansTemp
    saltAnomalies = iCESMAnomSaline - monthlyMeansSaline

    spatialMeanAnomsTemp = tempAnomalies.mean(dim=['nlat', 'nlon'])
    spatialMeanAnomsTemp = spatialMeanAnomsTemp.sel(z_t = 63, method = 'nearest')
    spatialMeanAnomsSaline = saltAnomalies.mean(dim=['nlat', 'nlon'])
    spatialMeanAnomsSaline = spatialMeanAnomsSaline.sel(z_t = 63, method = 'nearest')

    print("Computing annual anomalies...")
    annualTempAnoms = spatialMeanAnomsTemp.groupby('year').mean('month')
    annualSalineAnoms = spatialMeanAnomsSaline.groupby('year').mean('month')

    print("Combining the results...")
    resultAnomalies = xr.Dataset()
    resultAnomalies['temp'] = annualTempAnoms
    resultAnomalies['salt'] = annualSalineAnoms

    print("Returning results.")
    return resultAnomalies

iCESMExpertAnoms = calcSodaAnoms("./iCESM/selections/tempSEGUIN.nc", "./iCESM/selections/saltSEGUIN.nc")