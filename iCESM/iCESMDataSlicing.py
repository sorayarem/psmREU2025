## code modified from svenja ryan
## and nina whitney
## developed by soraya remaili
import numpy as np
import xarray as xr
import pandas as pd
import packaging as pk
import datetime
import cftime
from scipy.interpolate import griddata
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.util as cutil
import warnings

warnings.filterwarnings("ignore")

'''
ds0 = xr.open_dataset("./iCESM/iCESMSALINE.nc")
ds0 = ds0['SALT']
ds = ds0.sel(z_t = slice(0, 30000))
'''

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

'''
xbnds = [284,296] #define your range of longitudes
ybnds = [36.0,45.0] #define your range of latitudes
isotopes = cut_latlon_box(ds,ds.TLONG,ds.TLAT,xbnds,ybnds,drop=True)
isotopes.to_netcdf(path = './iCESM/iCESMSalt.nc') 
'''

'''
ds = xr.open_dataset("./iCESM/iCESMTemp.nc")
xbnds = [285, 286] #define your range of longitudes
ybnds = [38, 39] #define your range of latitudes

delmarva = cut_latlon_box(ds,ds.TLONG,ds.TLAT,xbnds,ybnds,drop=True)
delmarva.to_netcdf(path = './iCESM/selections/tempDELMARVA.nc') 
'''

'''
ds = xr.open_dataset("./iCESM/iCESMTemp.nc")
xbnds = [287, 288] #define your range of longitudes
ybnds = [39.5, 40.5] #define your range of latitudes

longisland = cut_latlon_box(ds,ds.TLONG,ds.TLAT,xbnds,ybnds,drop=True)
longisland.to_netcdf(path = './iCESM/selections/tempLONGISLAND.nc') 
'''

'''
ds = xr.open_dataset("./iCESM/iCESMTemp.nc")
xbnds = [292,293] #define your range of longitudes
ybnds = [40, 41] #define your range of latitudes

georges = cut_latlon_box(ds,ds.TLONG,ds.TLAT,xbnds,ybnds,drop=True)
georges.to_netcdf(path = './iCESM/selections/tempGEORGES.nc') 
'''

'''
ds = xr.open_dataset("./iCESM/iCESMTemp.nc")
xbnds = [291, 292] #define your range of longitudes
ybnds = [43.5, 44.5] #define your range of latitudes

isleauhaut = cut_latlon_box(ds,ds.TLONG,ds.TLAT,xbnds,ybnds,drop=True)
isleauhaut.to_netcdf(path = './iCESM/selections/tempISLEAUHAUT.nc') 
'''

'''
ds = xr.open_dataset("./iCESM/iCESMTemp.nc")
xbnds = [290, 291] #define your range of longitudes
ybnds = [43, 44] #define your range of latitudes

seguin = cut_latlon_box(ds,ds.TLONG,ds.TLAT,xbnds,ybnds,drop=True)
seguin.to_netcdf(path = './iCESM/selections/tempSEGUIN.nc') 
'''

'''
ds = xr.open_dataset("./iCESM/iCESMSalt.nc")
xbnds = [292,293] #define your range of longitudes
ybnds = [44.0,45.0] #define your range of latitudes

jonesport = cut_latlon_box(ds,ds.TLONG,ds.TLAT,xbnds,ybnds,drop=True)
jonesport.to_netcdf(path = './iCESM/selections/saltJONESPORT.nc') 
'''
