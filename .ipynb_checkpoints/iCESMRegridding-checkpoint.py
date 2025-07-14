## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import numpy as np
import xarray as xr
import pandas as pd
import packaging as pk
import datetime
import cftime
from scipy.interpolate import griddata
import pop_tools
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.util as cutil
import warnings

warnings.filterwarnings("ignore")

## getting the iCESM output .nc file
ds = xr.open_dataset("b.ie12.B1850C5CN.f19_g16.LME.003.pop.h.R18O.185001-200512.nc")

## selecting a single time slice and depth level (2D: nlat x nlon)
r18o_single = ds['R18O'].isel(time=0, z_t=10)
print("Selected R18O slice shape:", r18o_single.shape)  # should be (384, 320)

## loading POP horizontal grid lat/lon and ocean mask (curvilinear)
grid = pop_tools.get_grid('POP_gx1v6')
lat = grid['TLAT'].data    # (384, 320)
lon = grid['TLONG'].data   # (384, 320)
kmt = grid['KMT'].data

## building ocean mask (true for ocean points)
ocean_mask = (kmt > 0)
print(f"Ocean mask shape: {ocean_mask.shape}, number of ocean points: {np.sum(ocean_mask)}")

## applying ocean mask to R18O data (mask land points with NaN)
r18o_masked = r18o_single.where(ocean_mask)

## creating regular lat-lon grid (1° resolution)
lat_out = np.arange(-90, 90.1, 1.0)
lon_out = np.arange(0, 360.1, 1.0)
lon_grid, lat_grid = np.meshgrid(lon_out, lat_out)

## flattening the original lat, lon, and masked data arrays for interpolation
points = np.column_stack((lon.ravel(), lat.ravel()))          # (122880, 2)
values = r18o_masked.data.ravel()

## removing NaNs for interpolation
mask_valid = ~np.isnan(values)
points_valid = points[mask_valid]
values_valid = values[mask_valid]

print(f"Points before mask: {points.shape[0]}, after mask: {points_valid.shape[0]}")

## interpolating R18O from curvilinear grid to regular lat-lon grid (linear)
field_interp = griddata(points_valid, values_valid, (lon_grid, lat_grid), method='linear')

## interpolating ocean mask itself to the output grid using nearest neighbor
ocean_mask_float = ocean_mask.astype(float)
mask_interp = griddata(points, ocean_mask_float.ravel(), (lon_grid, lat_grid), method='nearest')
mask_interp_bool = mask_interp > 0.5  # True=Ocean, False=Land

## masking the interpolated R18O field with the output grid ocean mask to remove land spillover
field_interp_masked = np.where(mask_interp_bool, field_interp, np.nan)

## wrapping the masked interpolated data into an xarray.DataArray
ds_interp_masked = xr.DataArray(
    field_interp_masked,
    coords={'lat': lat_out, 'lon': lon_out},
    dims=['lat', 'lon'],
    name='R18O'
)

## defining the region of interest
lat_min, lat_max = 36, 45
lon_min, lon_max = 284, 296

## plotting the masked interpolated field on Robinson projection
fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree()})

ds_interp_masked.plot.pcolormesh(
    ax=ax,
    transform=ccrs.PlateCarree(),
    cmap='viridis',
    x='lon',
    y='lat'
)

## getting the coordinates for each site
lon = [360-74.0868, 360-73.01238, 360-67.8053, 360-69.75, 360-68.6789, 360-67.44]
lat = [38.2268, 40.09925, 40.727667, 43.7, 44.0398, 44.44]

## plotting the points
ax.plot(lon, lat, 'ro', markersize=6, transform=ccrs.PlateCarree(), label='Isotope Sites')

ax.set_extent([284, 296, 36, 45], crs=ccrs.PlateCarree()) 
ax.coastlines()
plt.title('R18O regridded and masked to ocean (no land spillover)')
plt.show()

## finding R18O values
siteLon =  360-73.01238
siteLat =  40.09925

## finding the nearest salinity value
nearest_salinity = ds_interp_masked.sel(
    lon = siteLon,
    lat = siteLat,
    method='nearest'
)

print(nearest_salinity)