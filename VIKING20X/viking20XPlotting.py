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
ds = xr.open_dataset("1_VIKING20X.L46-KFS003_1m_19710101_19711231_votemper_45W_80W_30N_57N_upper1000m.nc")

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

xbnds = [-76.1,-64.0] #define your range of longitudes
ybnds = [36.0,45.0] #define your range of latitudes
temp_ave = cut_latlon_box(ds,ds.nav_lon,ds.nav_lat,xbnds,ybnds,drop=True)
temp_ave = temp_ave.mean('time_counter')
target_depth = temp_ave['votemper'].sel(deptht = 38, method = 'nearest')

##select all areas where temperature does not equal 0 (temperature equals 0 on land in VIKING20X so this is essentially getting all ocean data)

yearly_alldepths_NaN = temp_ave.where(temp_ave['votemper'] != 0.0)

##The ffill() function stands for forward fill. This function fills missing values (NaNs) by propagating the last valid (non-NaN) value forward (in other words to deeper depths in this case because we have specified ‘deptht’ in the .ffill function). Because values at depth below the seafloor show up as NaNs, this means that it is filling in those values below the sea floor for a given area with the last actual data value at that location i.e., the temperature value at the seafloor##

yearly_alldepths_backfilled = yearly_alldepths_NaN['votemper'].ffill('deptht', limit=None)

##here, we’re just selecting the very bottom depth in the model because we have forwardfilled the dataframe so that all of the temperatures values at the bottom depth of 1136 meters will be the temperature value of the actual seafloor at that location##

yearly_alldepths_bottom = yearly_alldepths_backfilled.sel(deptht=1136.922)

# cut temp field

compare = yearly_alldepths_bottom - target_depth

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

temp_ave
#plotting the data, including lon, lat, trends (the actual data in this case), vmin and vmax define the upper and lower limits of your colorbar, 'cmo_balance' comes from a matplotlib python package
decade_trend_map = ax1.pcolormesh(compare.nav_lon, compare.nav_lat, compare, vmin=-7,vmax=7, cmap = plt.get_cmap('cmo.balance'))

#plotting the color bar
fig.colorbar(decade_trend_map, orientation='vertical', label='Bottom Temperature Trend ($^\circ$C/decade)', shrink = 0.4)

GeorgesBank = ax1.plot([-67.805333], [40.727667],
         color='yellow', marker='o', markeredgecolor = 'yellow', markeredgewidth = 2, markersize = 5,linestyle = 'None',zorder = 103
         )
Seguin= ax1.plot([-69.75], [43.7],
         color='yellow', marker='o', markeredgecolor = 'yellow', markeredgewidth = 2, markersize = 5,linestyle = 'None',zorder = 103
         )
IsleauHaut= ax1.plot([-68.6789], [44.0398],
         color='yellow', marker='o', markeredgecolor = 'yellow', markeredgewidth = 2, markersize = 5,linestyle = 'None',zorder = 103
         )
Station5_Delmarva= ax1.plot([-74.0868], [38.2268],
         color='yellow', marker='o', markeredgecolor = 'yellow', markeredgewidth = 2, markersize = 5,linestyle = 'None',zorder = 103
         )
Jonesport= ax1.plot([-67.44], [44.44],
         color='yellow', marker='o', markeredgecolor = 'yellow', markeredgewidth = 2, markersize = 5,linestyle = 'None',zorder = 103
         )
LongIsland= ax1.plot([-73.01238], [40.09925],
         color='yellow', marker='o', markeredgecolor = 'yellow', markeredgewidth = 2, markersize = 5,linestyle = 'None',zorder = 103
         )

plt.show()

