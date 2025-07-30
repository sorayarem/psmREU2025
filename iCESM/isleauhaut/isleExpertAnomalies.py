## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

## method to establish an expert season (oct-sep)
def getExpertYear(time):
    return time.year + int(time.month >= 10)

## calculating the temp and salt anomalies for each month
def calcSodaAnoms(iCESMTEMPFile, iCESMSALINEFile, iCESMISOFile):

    ## loading in the combined .nc file
    print("Loading file...")
    dsTemp = xr.open_dataset(iCESMTEMPFile)
    dsSaline = xr.open_dataset(iCESMSALINEFile)
    dsIso = xr.open_dataset(iCESMISOFile)

    ## fixing the n/a values with forward fill
    dsTemp = dsTemp.where(dsTemp['TEMP'] != 0.0)
    dsTemp['TEMP'] = dsTemp['TEMP'].ffill('z_t', limit=None)
    dsSaline = dsSaline.where(dsSaline['SALT'] != 0.0)
    dsSaline['SALT'] = dsSaline['SALT'].ffill('z_t', limit=None)
    dsIso = dsIso.where(dsIso['R18O'] != 0.0)
    dsIso['R18O'] = dsIso['R18O'].ffill('z_t', limit=None)

    
    ## getting just the month and year
    print("Extracting month and year...")
    dsTemp['month'] = dsTemp['time'].dt.month
    dsTemp['year'] = dsTemp['time'].dt.year

    dsSaline['month'] = dsSaline['time'].dt.month
    dsSaline['year'] = dsSaline['time'].dt.year

    dsIso['month'] = dsIso['time'].dt.month
    dsIso['year'] = dsIso['time'].dt.year

    ## calculating the expert years
    expertTemp = xr.apply_ufunc(getExpertYear, dsTemp['time'], vectorize=True)
    expertSaline = xr.apply_ufunc(getExpertYear, dsSaline['time'], vectorize=True)
    expertIso = xr.apply_ufunc(getExpertYear, dsIso['time'], vectorize=True)

    ## assigning the new columns the appropriate coordinates
    dsTemp = dsTemp.assign_coords(year=expertTemp)
    dsSaline = dsSaline.assign_coords(year=expertSaline)
    dsIso = dsIso.assign_coords(year=expertIso)

    dsTemp = dsTemp.assign_coords(month=dsTemp['time'].dt.month)
    dsSaline = dsSaline.assign_coords(month=dsSaline['time'].dt.month)
    dsIso = dsIso.assign_coords(month=dsIso['time'].dt.month)

    ## getting the monthly means for each specific month (i.e. January 1980)
    print("Computing monthly mean temp and salinity...")
    iCESMAnomTemp = dsTemp['TEMP'].groupby(['year', 'month']).mean('time')
    iCESMAnomSaline = dsSaline['SALT'].groupby(['year', 'month']).mean('time')
    iCESMAnomIso = dsIso['R18O'].groupby(['year', 'month']).mean('time')

    ## getting the means for each month overall (i.e. January)
    print("Computing monthly means...")
    monthlyMeansTemp =  dsTemp['TEMP'].groupby('month').mean('time')
    monthlyMeansSaline =  dsSaline['SALT'].groupby('month').mean('time')
    monthlyMeansIso =  dsIso['R18O'].groupby('month').mean('time')

    ## subtracting the monthly mean from each specific month
    print("Calculating anomalies...")
    tempAnomalies = iCESMAnomTemp - monthlyMeansTemp
    saltAnomalies = iCESMAnomSaline - monthlyMeansSaline
    isoAnomalies = iCESMAnomIso - monthlyMeansIso
    
    ## averaging over space and selecting a specific depth
    spatialMeanAnomsTemp = tempAnomalies.mean(dim=['nlat', 'nlon'])
    spatialMeanAnomsTemp = spatialMeanAnomsTemp.sel(z_t = 30000, method = 'nearest')
    spatialMeanAnomsSaline = saltAnomalies.mean(dim=['nlat', 'nlon'])
    spatialMeanAnomsSaline = spatialMeanAnomsSaline.sel(z_t = 30000, method = 'nearest')
    spatialMeanAnomsIso = isoAnomalies.mean(dim=['nlat', 'nlon'])
    spatialMeanAnomsIso = spatialMeanAnomsIso.sel(z_t = 30000, method = 'nearest')

    ## getting the mean for each overall year
    print("Computing annual anomalies...")
    expertTempAnoms = spatialMeanAnomsTemp.groupby('year').mean('month')
    expertSalineAnoms = spatialMeanAnomsSaline.groupby('year').mean('month')
    expertIsoAnoms = spatialMeanAnomsIso.groupby('year').mean('month')
    
    ## removing the first and last years from the dataset
    yearsValid = expertTempAnoms['year'].values[1:-1]
    expertTempAnoms = expertTempAnoms[expertTempAnoms['year'].isin(yearsValid)]
    expertSalineAnoms = expertSalineAnoms[expertSalineAnoms['year'].isin(yearsValid)]
    expertIsoAnoms = expertIsoAnoms[expertIsoAnoms['year'].isin(yearsValid)]

    ## combining the temperature and salinity results
    print("Combining the results...")
    resultAnomalies = xr.Dataset()
    resultAnomalies['temp'] = expertTempAnoms
    resultAnomalies['salt'] = expertSalineAnoms
    resultAnomalies['iso'] = expertIsoAnoms

    ## returning the overall expert anomalies
    print("Returning results.")
    return resultAnomalies

iCESMExpertAnoms = calcSodaAnoms("./iCESM/selections/tempISLEAUHAUT.nc", "./iCESM/selections/saltISLEAUHAUT.nc", "./iCESM/selections/isoISLEAUHAUT.nc")