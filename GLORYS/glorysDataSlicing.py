## code modified from svenja ryan
## and nina whitney
## developed by soraya remaili
import xarray as xr

# turn off warnings
import warnings
warnings.filterwarnings("ignore")

'''
ds = xr.open_dataset("./GLORYS/data/glorysSALT.nc")
delmarva = ds.sel(longitude = slice(-74.1 - 1/12, -74.1 + 1/12), latitude =slice(38.2 - 1/12, 38.2 + 1/12))
delmarva.to_netcdf(path = './GLORYS/selections/saltDELMARVA.nc') 
'''
'''
ds = xr.open_dataset("./GLORYS/data/glorysTEMP.nc")
longIsland = ds.sel(longitude = slice(-73.0 - 1/12, -73.0 + 1/12), latitude =slice(40.1 - 1/12, 40.1 + 1/12))
longIsland.to_netcdf(path = './GLORYS/selections/tempLONGISLAND.nc') 
'''
'''
ds = xr.open_dataset("./GLORYS/data/glorysSALT.nc")
georges = ds.sel(longitude = slice(-67.8 - 1/12, -67.8 + 1/12), latitude =slice(40.7 - 1/12, 40.7 + 1/12))
georges.to_netcdf(path = './GLORYS/selections/saltGEORGES.nc') 
'''
'''
ds = xr.open_dataset("./GLORYS/data/glorysTEMP.nc")
seguin = ds.sel(longitude = slice(-69.8 - 1/12, -69.8 + 1/12), latitude =slice(43.7 - 1/12, 43.7 + 1/12))
seguin.to_netcdf(path = './GLORYS/selections/tempSEGUIN.nc') 
'''
'''
ds = xr.open_dataset("./GLORYS/data/glorysSALT.nc")
isleAuHaut = ds.sel(longitude = slice(-68.7 - 1/12, -68.7 + 1/12), latitude =slice(44 - 1/12, 44 + 1/12))
isleAuHaut.to_netcdf(path = './GLORYS/selections/saltISLEAUHAUT.nc') 
'''
'''
ds = xr.open_dataset("./GLORYS/data/glorysTEMP.nc")
jonesport = ds.sel(longitude = slice(-67.4 - 1/12, -67.4 + 1/12), latitude =slice(44.4 - 1/12, 44.4 + 1/12))
jonesport.to_netcdf(path = './GLORYS/selections/tempJONESPORT.nc') 
'''