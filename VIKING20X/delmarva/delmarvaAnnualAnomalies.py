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

    ## fixing the 0.0 values with forward fill
    dsTemp = dsTemp.where(dsTemp['votemper'] != 0.0)
    dsTemp['votemper'] = dsTemp['votemper'].ffill('deptht', limit=None)
    dsSaline = dsSaline.where(dsSaline['vosaline'] != 0.0)
    dsSaline['vosaline'] = dsSaline['vosaline'].ffill('deptht', limit=None)
    
    ## getting just the month and year
    print("Extracting month and year...")
    dsTemp['month'] = dsTemp['time_counter'].dt.month
    dsTemp['year'] = dsTemp['time_counter'].dt.year

    dsSaline['month'] = dsSaline['time_counter'].dt.month
    dsSaline['year'] = dsSaline['time_counter'].dt.year

    ## assigning the new columns the appropriate coordinates
    dsTemp = dsTemp.assign_coords(year=dsTemp['time_counter'].dt.year,month=dsTemp['time_counter'].dt.month)
    dsSaline = dsSaline.assign_coords(year=dsSaline['time_counter'].dt.year,month=dsSaline['time_counter'].dt.month)

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
    spatialMeanAnomsTemp = spatialMeanAnomsTemp.sel(deptht = 1136.922, method = 'nearest')
    spatialMeanAnomsSaline = saltAnomalies.mean(dim=['y', 'x'])
    spatialMeanAnomsSaline = spatialMeanAnomsSaline.sel(deptht = 1136.922, method = 'nearest')

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

vikingAnnualAnoms = calcSodaAnoms("./VIKING20X/selections/tempDELMARVA.nc", "./VIKING20X/selections/saltDELMARVA.nc")