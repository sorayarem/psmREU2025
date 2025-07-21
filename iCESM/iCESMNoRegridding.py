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


ds = xr.open_dataset("./iCESM/iCESMIso.nc")
## ds = ds['R18O']

def mean_weighted(self, dim=None, weights=None):
    if weights is None:
        return self.mean(dim)
    else:
        return (self * weights.values).sum(dim,skipna=True) / weights.sum(dim,skipna=True)

def cut_latlon_box(field,lon,lat,lon_bnds,lat_bnds,drop=True,coords='2D'):
        # ### cut data for box
        if coords=='2D':
            ds = field.where((lon_bnds[0] < lon) & (lon < lon_bnds[1])
                     & (lat_bnds[0] < lat) & (lat < lat_bnds[1]), drop=drop)
            # because we have 2D coordinates we have to use the command where, otherwise we could use the
            # sel & slice commands from xarray
        elif coords=='1D':
            ds = field.sel(lon=slice(*lon_bnds),lat=slice(*lat_bnds),drop=drop)
        return ds

xbnds = [284,296] #define your range of longitudes
ybnds = [36.0,45.0] #define your range of latitudes
## temp_ave = cut_latlon_box(ds,ds.TLONG,ds.TLAT,xbnds,ybnds,drop=True)
temp_ave = ds.mean('time')
temp_ave = temp_ave['R18O'].sel(z_t = 60, method = 'nearest')

#create figure
fig, ax1 = plt.subplots(figsize=(10,10))

#making the borders of figure invisible
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
#getting rid of x and y ticks
ax1.set_xticks([])
ax1.set_yticks([])
#getting rid of labels (because it screws things up when making a map)
ax1.xlabels_bottom = False
ax1.ylabels_left = False

#defining the projection and the resolution of the coastline
ax1 = plt.axes(projection=ccrs.PlateCarree())
ax1.coastlines(resolution='50m', color='gray')

#defining the lat and lon limits of the map (what you can see, not actually doing anything to the data)
ax1.set_xlim([-76,-64])
ax1.set_ylim([36, 45])

#plotting the data, including lon, lat, trends (the actual data in this case), vmin and vmax define the upper and lower limits of your colorbar, 'cmo_balance' comes from a matplotlib python package
decade_trend_map = ax1.pcolormesh(temp_ave.TLONG, temp_ave.TLAT, temp_ave, vmin=1.0005,vmax=1.0009, cmap = plt.get_cmap('cmo.deep'))

#plotting the color bar
fig.colorbar(decade_trend_map, orientation='vertical', label='Seawater Isotope Trend ($^\circ$C/decade)', shrink = 0.4)

GeorgesBank = ax1.plot([-67.805333], [40.727667],
         color='yellow', marker='o', markeredgecolor = 'yellow', markeredgewidth = 2, markersize = 2,linestyle = 'None',zorder = 103
         )
Seguin= ax1.plot([-69.75], [43.7],
         color='yellow', marker='o', markeredgecolor = 'yellow', markeredgewidth = 2, markersize = 2,linestyle = 'None',zorder = 103
         )
IsleauHaut= ax1.plot([-68.6789], [44.0398],
         color='yellow', marker='o', markeredgecolor = 'yellow', markeredgewidth = 2, markersize = 2,linestyle = 'None',zorder = 103
         )
Station5_Delmarva= ax1.plot([-74.0868], [38.2268],
         color='yellow', marker='o', markeredgecolor = 'yellow', markeredgewidth = 2, markersize = 2,linestyle = 'None',zorder = 103
         )
Jonesport= ax1.plot([-67.44], [44.44],
         color='yellow', marker='o', markeredgecolor = 'yellow', markeredgewidth = 2, markersize = 2,linestyle = 'None',zorder = 103
         )
LongIsland= ax1.plot([-73.01238], [40.09925],
         color='yellow', marker='o', markeredgecolor = 'yellow', markeredgewidth = 2, markersize = 2,linestyle = 'None',zorder = 103
         )

plt.show()