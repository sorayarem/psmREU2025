## code modified from svenja ryan
## and nina whitney
## developed by soraya remaili
import os
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from cartopy import config
import cartopy.crs as ccrs
import numpy.polynomial.polynomial as npoly
import matplotlib.gridspec as gridspec
import cmocean as cmo  # cmocean colormaps
import cftime as cftime

from cartopy import config
import cartopy.crs as ccrs
import cmocean as cmo  # cmocean colormaps
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy

# plotting
import matplotlib.patches as mpatches
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy   # package to plot maps

# turn off warnings
import warnings
warnings.filterwarnings("ignore")


from brokenaxes import brokenaxes
dsTemp = xr.open_dataset("./VIKING20X/selections/tempSEGUIN.nc")
dsSaline = xr.open_dataset("./VIKING20X/selections/saltSEGUIN.nc")
dsSaline = dsSaline.where(dsSaline['vosaline'] != 0.0)
    
## getting just the month and year
print("Extracting month and year...")
dsTemp['month'] = dsTemp['time_counter'].dt.month
dsTemp['year'] = dsTemp['time_counter'].dt.year

dsSaline['month'] = dsSaline['time_counter'].dt.month
dsSaline['year'] = dsSaline['time_counter'].dt.year

## assigning the new columns the appropriate coordinates
dsTemp = dsTemp.assign_coords(year=dsTemp['time_counter'].dt.year,month=dsTemp['time_counter'].dt.month)
dsSaline = dsSaline.assign_coords(year=dsSaline['time_counter'].dt.year,month=dsSaline['time_counter'].dt.month)

## averaging over space and selecting a specific depth
spatialMeanAnomsTemp_0 = dsTemp.mean(dim=['y', 'x'])
spatialMeanAnomsTemp_0 = spatialMeanAnomsTemp_0.sel(deptht = 0, method = 'nearest')
spatialMeanAnomsSaline_0 = dsSaline.mean(dim=['y', 'x'])
spatialMeanAnomsSaline_0 = spatialMeanAnomsSaline_0.sel(deptht = 0, method = 'nearest')

## getting the mean for each overall year
print("Computing annual anomalies...")
annualTempAnoms_0 = spatialMeanAnomsTemp_0.groupby('year').mean()
annualSalineAnoms_0 = spatialMeanAnomsSaline_0.groupby('year').mean()

years_0 = annualTempAnoms_0['year'].values
temps_0 = annualTempAnoms_0['votemper'].values
salts_0 = annualSalineAnoms_0['vosaline'].values

## averaging over space and selecting a specific depth
spatialMeanAnomsTemp_30 = dsTemp.mean(dim=['y', 'x'])
spatialMeanAnomsTemp_30 = spatialMeanAnomsTemp_30.sel(deptht = 30, method = 'nearest')
spatialMeanAnomsSaline_30 = dsSaline.mean(dim=['y', 'x'])
spatialMeanAnomsSaline_30 = spatialMeanAnomsSaline_30.sel(deptht = 30, method = 'nearest')

## getting the mean for each overall year
print("Computing annual anomalies...")
annualTempAnoms_30 = spatialMeanAnomsTemp_30.groupby('year').mean()
annualSalineAnoms_30 = spatialMeanAnomsSaline_30.groupby('year').mean()

years_30 = annualTempAnoms_30['year'].values
temps_30 = annualTempAnoms_30['votemper'].values
salts_30 = annualSalineAnoms_30['vosaline'].values

## averaging over space and selecting a specific depth
spatialMeanAnomsTemp_50 = dsTemp.mean(dim=['y', 'x'])
spatialMeanAnomsTemp_50 = spatialMeanAnomsTemp_50.sel(deptht = 50, method = 'nearest')
spatialMeanAnomsSaline_50 = dsSaline.mean(dim=['y', 'x'])
spatialMeanAnomsSaline_50 = spatialMeanAnomsSaline_50.sel(deptht = 50, method = 'nearest')

## getting the mean for each overall year
print("Computing annual anomalies...")
annualTempAnoms_50 = spatialMeanAnomsTemp_50.groupby('year').mean()
annualSalineAnoms_50 = spatialMeanAnomsSaline_50.groupby('year').mean()

years_50 = annualTempAnoms_50['year'].values
temps_50 = annualTempAnoms_50['votemper'].values
salts_50 = annualSalineAnoms_50['vosaline'].values

## averaging over space and selecting a specific depth
spatialMeanAnomsTemp_80 = dsTemp.mean(dim=['y', 'x'])
spatialMeanAnomsTemp_80 = spatialMeanAnomsTemp_80.sel(deptht = 80, method = 'nearest')
spatialMeanAnomsSaline_80 = dsSaline.mean(dim=['y', 'x'])
spatialMeanAnomsSaline_80 = spatialMeanAnomsSaline_80.sel(deptht = 80, method = 'nearest')

## getting the mean for each overall year
print("Computing annual anomalies...")
annualTempAnoms_80 = spatialMeanAnomsTemp_80.groupby('year').mean()
annualSalineAnoms_80 = spatialMeanAnomsSaline_80.groupby('year').mean()

years_80 = annualTempAnoms_80['year'].values
temps_80 = annualTempAnoms_80['votemper'].values
salts_80 = annualSalineAnoms_80['vosaline'].values

'''
plt.figure(figsize=(10, 5))
plt.plot(years_0, temps_0, label='depth 0', linestyle='-', color='#008080') 
plt.plot(years_30, temps_30, label='depth 30', linestyle='-', color='purple') 
plt.plot(years_50, temps_50, label='depth 50', linestyle='-', color='#D2691E')
plt.plot(years_80, temps_80, label='depth 80', linestyle='-', color='green')  
plt.xlabel('Year')
plt.ylabel('Value')
plt.title('Temperature Over Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
'''

plt.figure(figsize=(10, 5))
plt.plot(years_0, salts_0, label='depth 0', linestyle='-', color='#008080') 
plt.plot(years_30, salts_30, label='depth 30', linestyle='-', color='purple') 
plt.plot(years_50, salts_50, label='depth 50', linestyle='-', color='#D2691E')
plt.plot(years_80, salts_80, label='depth 80', linestyle='-', color='green')  
plt.xlabel('Year')
plt.ylabel('Value')
plt.title('Salinity Over Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


