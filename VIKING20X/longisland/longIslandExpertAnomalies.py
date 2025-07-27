## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

def getExpertYear(time):
    time = pd.Timestamp(time)
    return time.year - int(time.month < 10)

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

    expertTemp = xr.apply_ufunc(getExpertYear, dsTemp['time_counter'], vectorize=True)
    expertSaline = xr.apply_ufunc(getExpertYear, dsSaline['time_counter'], vectorize=True)

    dsTemp = dsTemp.assign_coords(year=expertTemp)
    dsSaline = dsSaline.assign_coords(year=expertSaline)

    dsTemp = dsTemp.assign_coords(month=dsTemp['time_counter'].dt.month)
    dsSaline = dsSaline.assign_coords(month=dsSaline['time_counter'].dt.month)

    print("Computing monthly mean temp and salinity...")
    vikingAnomTemp = dsTemp['votemper'].groupby(['year', 'month']).mean('time_counter')
    vikingAnomSaline = dsSaline['vosaline'].groupby(['year', 'month']).mean('time_counter')

    print("Computing monthly means...")
    monthlyMeansTemp =  dsTemp['votemper'].groupby('month').mean('time_counter')
    monthlyMeansSaline =  dsSaline['vosaline'].groupby('month').mean('time_counter')

    print("Calculating anomalies...")
    tempAnomalies = vikingAnomTemp - monthlyMeansTemp
    saltAnomalies = vikingAnomSaline - monthlyMeansSaline

    spatialMeanAnomsTemp = tempAnomalies.mean(dim=['y', 'x'])
    spatialMeanAnomsTemp = spatialMeanAnomsTemp.sel(deptht = 80, method = 'nearest')
    spatialMeanAnomsSaline = saltAnomalies.mean(dim=['y', 'x'])
    spatialMeanAnomsSaline = spatialMeanAnomsSaline.sel(deptht = 80, method = 'nearest')

    print("Computing annual anomalies...")
    annualTempAnoms = spatialMeanAnomsTemp.groupby('year').mean('month')
    annualSalineAnoms = spatialMeanAnomsSaline.groupby('year').mean('month')

    print("Combining the results...")
    resultAnomalies = xr.Dataset()
    resultAnomalies['temp'] = annualTempAnoms
    resultAnomalies['salt'] = annualSalineAnoms

    print("Returning results.")
    return resultAnomalies

vikingExpertAnoms = calcSodaAnoms("./VIKING20X/selections/tempLONGISLAND.nc", "./VIKING20X/selections/saltLONGISLAND.nc")
