## code modified from svenja ryan
## and nina whitney
## developed by soraya remaili
import xarray as xr
import glob

# turn off warnings
import warnings
warnings.filterwarnings("ignore")

'''
files = sorted(glob.glob("./vikingSALINE/*.nc"))
viking_ALLSALINE = xr.open_mfdataset(files, combine='by_coords')
viking_ALLSALINE.to_netcdf('viking_ALLSALINE.nc')
'''

from brokenaxes import brokenaxes
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
ds = xr.open_dataset("./VIKING20X/data/vikingTEMP.nc")
xbnds = [-74.15, -74.05] #define your range of longitudes
ybnds = [38.15, 38.25] #define your range of latitudes

delmarva = cut_latlon_box(ds,ds.nav_lon,ds.nav_lat,xbnds,ybnds,drop=True)
delmarva.to_netcdf(path = './VIKING20X/selections/tempDELMARVA.nc') 
'''

'''
ds = xr.open_dataset("./VIKING20X/data/vikingSALT.nc")
xbnds = [-73.05, -72.95] #define your range of longitudes
ybnds = [40.05, 40.15] #define your range of latitudes

longisland = cut_latlon_box(ds,ds.nav_lon,ds.nav_lat,xbnds,ybnds,drop=True)
longisland.to_netcdf(path = './VIKING20X/selections/saltLONGISLAND.nc') 
'''

'''
ds = xr.open_dataset("./VIKING20X/data/vikingTEMP.nc")
xbnds = [-67.85, -67.75] #define your range of longitudes
ybnds = [40.65, 40.75] #define your range of latitudes

georges = cut_latlon_box(ds,ds.nav_lon,ds.nav_lat,xbnds,ybnds,drop=True)
georges.to_netcdf(path = './VIKING20X/selections/tempGEORGES.nc') 
'''

'''
ds = xr.open_dataset("./VIKING20X/data/vikingSALT.nc")
xbnds = [-68.75, -68.65] #define your range of longitudes
ybnds = [43.95, 44.05] #define your range of latitudes

isleauhaut = cut_latlon_box(ds,ds.nav_lon,ds.nav_lat,xbnds,ybnds,drop=True)
isleauhaut.to_netcdf(path = './VIKING20X/selections/saltISLEAUHAUT.nc') 
'''

'''
ds = xr.open_dataset("./VIKING20X/data/vikingTEMP.nc")
xbnds = [-69.85, -69.75] #define your range of longitudes
ybnds = [43.65, 43.75] #define your range of latitudes

seguin = cut_latlon_box(ds,ds.nav_lon,ds.nav_lat,xbnds,ybnds,drop=True)
seguin.to_netcdf(path = './VIKING20X/selections/tempSEGUIN.nc') 
'''

'''
ds = xr.open_dataset("./VIKING20X/data/vikingSALT.nc")
xbnds = [-67.45,-67.35] #define your range of longitudes
ybnds = [44.35,44.45] #define your range of latitudes

jonesport = cut_latlon_box(ds,ds.nav_lon,ds.nav_lat,xbnds,ybnds,drop=True)
jonesport.to_netcdf(path = './VIKING20X/selections/saltJONESPORT.nc') 
'''

'''
xbnds = [-76.1,-64.0] #define your range of longitudes
ybnds = [36.0,45.0] #define your range of latitudes

extension = '.nc'

## downloading and trimming the .nc files
start =  '1_VIKING20X.L46-KFS003_1m_'
end =  '_votemper_45W_80W_30N_57N_upper1000m'
extension = '.nc'
for i in range (1958, 2020):
    ds = xr.open_dataset(start + str(i) + '0101_' + str(i) + '1231' + end + extension)
    temp_ave = cut_latlon_box(ds,ds.nav_lon,ds.nav_lat,xbnds,ybnds,drop=True)
    temp_ave.to_netcdf(path = './vikingTEMP/vikingTEMP' + str(i) + extension) 
'''