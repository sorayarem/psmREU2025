## code modified from svenja ryan
## and nina whitney
## developed by soraya remaili
import os
import xarray as xr
import numpy as np
import pandas as pd
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

ds = xr.open_dataset("./iCESM/selections/saltISLEAUHAUT.nc")
temp_ave = ds.mean('time')
temp_ave = temp_ave.mean('z_t')
temp_ave = temp_ave['SALT']

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

##plotting the data, including lon, lat, trends (the actual data in this case), vmin and vmax define the upper and lower limits of your colorbar, 'cmo_balance' comes from a matplotlib python package
lon = (ds['TLONG'].values + 180) % 360 - 180
lat = ds['TLAT'].values

for i in range(temp_ave.shape[0]):
    for j in range(temp_ave.shape[1]):
        if not np.isnan(temp_ave[i, j]):
            ax1.plot(
                lon[i, j],
                lat[i, j],
                marker='o',
                color='red',       
                markersize=8,
                transform=ccrs.PlateCarree(),
                zorder=90
            )

GeorgesBank = ax1.plot([-67.805333], [40.727667],
         color='blue', marker='o', markeredgecolor = 'blue', markeredgewidth = 2, markersize = 2,linestyle = 'None',zorder = 103
         )
Seguin= ax1.plot([-69.75], [43.7],
         color='blue', marker='o', markeredgecolor = 'blue', markeredgewidth = 2, markersize = 2,linestyle = 'None',zorder = 103
         )
IsleauHaut= ax1.plot([-68.6789], [44.0398],
         color='blue', marker='o', markeredgecolor = 'blue', markeredgewidth = 2, markersize = 2,linestyle = 'None',zorder = 103
         )
Station5_Delmarva= ax1.plot([-74.0868], [38.2268],
         color='blue', marker='o', markeredgecolor = 'blue', markeredgewidth = 2, markersize = 2,linestyle = 'None',zorder = 103
         )
Jonesport= ax1.plot([-67.44], [44.44],
         color='blue', marker='o', markeredgecolor = 'blue', markeredgewidth = 2, markersize = 2,linestyle = 'None',zorder = 103
         )
LongIsland= ax1.plot([-73.01238], [40.09925],
         color='blue', marker='o', markeredgecolor = 'blue', markeredgewidth = 2, markersize = 2,linestyle = 'None',zorder = 103
         )

plt.show()