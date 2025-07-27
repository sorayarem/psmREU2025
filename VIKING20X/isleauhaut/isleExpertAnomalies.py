## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

## method to establish an expert season (oct-sep)
def getExpertYear(time):
    time = pd.Timestamp(time)
    return time.year + int(time.month >= 10)

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

    ## calculating the expert years
    expertTemp = xr.apply_ufunc(getExpertYear, dsTemp['time_counter'], vectorize=True)
    expertSaline = xr.apply_ufunc(getExpertYear, dsSaline['time_counter'], vectorize=True)

    ## assigning the new columns the appropriate coordinates
    dsTemp = dsTemp.assign_coords(year=expertTemp)
    dsSaline = dsSaline.assign_coords(year=expertSaline)

    dsTemp = dsTemp.assign_coords(month=dsTemp['time_counter'].dt.month)
    dsSaline = dsSaline.assign_coords(month=dsSaline['time_counter'].dt.month)

    ## getting the monthly means for each specific month (i.e. January 1980)
    print("Computing monthly mean temp and salinity...")
    vikingAnomTemp = dsTemp['votemper'].groupby(['year', 'month']).mean('time_counter')
    vikingAnomSaline = dsSaline['vosaline'].groupby(['year', 'month']).mean('time_counter')

    ## getting the means for each month overall (i.e. January)
    print("Computing monthly means...")
    monthlyMeansTemp =  dsTemp['votemper'].groupby('month').mean('time_counter')
    monthlyMeansSaline =  dsSaline['vosaline'].groupby('month').mean('time_counter')

    ## subtracting the monthly mean from each specific month
    print("Calculating anomalies...")
    tempAnomalies = vikingAnomTemp - monthlyMeansTemp
    saltAnomalies = vikingAnomSaline - monthlyMeansSaline
    
    ## averaging over space and selecting a specific depth
    spatialMeanAnomsTemp = tempAnomalies.mean(dim=['y', 'x'])
    spatialMeanAnomsTemp = spatialMeanAnomsTemp.sel(deptht = 80, method = 'nearest')
    spatialMeanAnomsSaline = saltAnomalies.mean(dim=['y', 'x'])
    spatialMeanAnomsSaline = spatialMeanAnomsSaline.sel(deptht = 80, method = 'nearest')

    ## getting the mean for each overall year
    print("Computing expert anomalies...")
    expertTempAnoms = spatialMeanAnomsTemp.groupby('year').mean('month')
    expertSalineAnoms = spatialMeanAnomsSaline.groupby('year').mean('month')
    
    ## removing the first and last years from the dataset
    yearsValid = expertTempAnoms['year'].values[1:-1]
    expertTempAnoms = expertTempAnoms[expertTempAnoms['year'].isin(yearsValid)]
    expertSalineAnoms = expertSalineAnoms[expertSalineAnoms['year'].isin(yearsValid)]

    ## combining the temperature and salinity results
    print("Combining the results...")
    resultAnomalies = xr.Dataset()
    resultAnomalies['temp'] = expertTempAnoms
    resultAnomalies['salt'] = expertSalineAnoms

    ## returning the overall expert anomalies
    print("Returning results.")
    return resultAnomalies

vikingExpertAnoms = calcSodaAnoms("./VIKING20X/selections/tempISLEAUHAUT.nc", "./VIKING20X/selections/saltISLEAUHAUT.nc")