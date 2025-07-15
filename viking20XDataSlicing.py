## code modified from svenja ryan
## and nina whitney
## developed by soraya remaili
import xarray as xr

# turn off warnings
import warnings
warnings.filterwarnings("ignore")


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