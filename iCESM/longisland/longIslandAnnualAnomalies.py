## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

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

    ## assigning the new columns the appropriate coordinates
    dsTemp = dsTemp.assign_coords(year=dsTemp['time'].dt.year,month=dsTemp['time'].dt.month)
    dsSaline = dsSaline.assign_coords(year=dsSaline['time'].dt.year,month=dsSaline['time'].dt.month)

    ## getting the monthly means for each specific month (i.e. January 1980)
    print("Computing monthly mean temp and salinity...")
    iCESMAnomTemp = dsTemp['TEMP'].groupby(['year', 'month']).mean('time')
    iCESMAnomSaline = dsSaline['SALT'].groupby(['year', 'month']).mean('time')

    ## getting the means for each month overall (i.e. January)
    print("Computing monthly means...")
    monthlyMeansTemp =  dsTemp['TEMP'].groupby('month').mean('time')
    monthlyMeansSaline =  dsSaline['SALT'].groupby('month').mean('time')

    ## subtracting the monthly mean from each specific month
    print("Calculating anomalies...")
    tempAnomalies = iCESMAnomTemp - monthlyMeansTemp
    saltAnomalies = iCESMAnomSaline - monthlyMeansSaline

    ## averaging over space and selecting a specific depth
    spatialMeanAnomsTemp = tempAnomalies.mean(dim=['nlat', 'nlon'])
    spatialMeanAnomsTemp = spatialMeanAnomsTemp.sel(z_t = 0, method = 'nearest')
    spatialMeanAnomsSaline = saltAnomalies.mean(dim=['nlat', 'nlon'])
    spatialMeanAnomsSaline = spatialMeanAnomsSaline.sel(z_t = 0, method = 'nearest')

    ## getting the mean for each overall year
    print("Computing annual anomalies...")
    annualTempAnoms = spatialMeanAnomsTemp.groupby('year').mean('month')
    annualSalineAnoms = spatialMeanAnomsSaline.groupby('year').mean('month')

    ## combining the temperature and salinity results
    print("Combining the results...")
    resultAnomalies = xr.Dataset()
    resultAnomalies['temp'] = annualTempAnoms
    resultAnomalies['salt'] = annualSalineAnoms

    ## returning the overall annual anomalies
    print("Returning results.")
    return resultAnomalies

iCESMAnnualAnoms = calcSodaAnoms("./iCESM/selections/tempLONGISLAND.nc", "./iCESM/selections/saltLONGISLAND.nc")