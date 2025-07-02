## developed by soraya remaili
import xarray as xr
import pandas as pd

extension = '.nc'

## downloading and trimming the .nc files
filename =  'soda3.15.2_mn_ocean_reg_'
extension = '.nc'
for i in range (1980, 2020):
    ds = xr.open_dataset(filename + str(i) + extension)
    dsNew = ds.sel(xt_ocean=slice(284, 296), yt_ocean=slice(36, 45), st_ocean=slice(0, 300))
    dsNew.to_netcdf(path = 'soda_' + str(i) + extension)

in_dir = "./nc/"
out_dir = './csv/'
for i in range (1980, 2020):
    ds = xr.open_dataset(in_dir + 'soda_' + str(i) + extension)
    ds = ds[['time', 'xt_ocean', 'yt_ocean', 'st_ocean', 'temp', 'salt']]
    df = ds.to_dataframe()
    table = df.to_csv(out_dir+str(i)+'.csv')