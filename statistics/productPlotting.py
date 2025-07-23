## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

soda = pd.read_csv("./csv_clean/megaCSV.csv")
## converting from string to date-time object
print("Converting time column...")
soda['time'] = pd.to_datetime(soda['time'], format= 'mixed')
soda['time'] = soda['time'].dt.to_period('M')

## getting just the month and year
print("Extracting month and year...")
soda['month'] = soda['time'].dt.month
soda['year'] = soda['time'].dt.year

print("Computing daily mean temp and salinity...")
sodaDaily = soda.groupby(['time', 'month'], as_index=False).agg({'temp': 'mean', 'salt': 'mean'})
print("Computing monthly means...")
sodaMonthly = sodaDaily.groupby('month', as_index=False).agg({'temp': 'mean', 'salt': 'mean'})

ds = xr.open_dataset("./iCESM/iCESMTemp.nc")
iCESM = ds.mean(dim=['z_t', 'nlat', 'nlon'])

## getting just the month and year
print("Extracting month and year...")
iCESM['month'] = iCESM['time'].dt.month
iCESM['year'] = iCESM['time'].dt.year

iCESM = iCESM.assign_coords(year=iCESM['time'].dt.year,month=iCESM['time'].dt.month)

print("Computing monthly means...")
iCESMMonthly =  iCESM['TEMP'].groupby('month').mean('time')

ds = xr.open_dataset("./VIKING20X/vikingTEMP.nc")
viking = ds.mean(dim=['deptht', 'y', 'x'])

## getting just the month and year
print("Extracting month and year...")
viking['month'] = viking['time_counter'].dt.month
viking['year'] = viking['time_counter'].dt.year

viking = viking.assign_coords(year=viking['time_counter'].dt.year,month=viking['time_counter'].dt.month)

print("Computing monthly means...")
vikingMonthly =  viking['votemper'].groupby('month').mean('time_counter')

## plotting the graph
plt.figure(figsize=(12, 6))
plt.plot(sodaMonthly['month'], sodaMonthly['temp'], label='SODA', linestyle='-', color = "green")
plt.plot(iCESMMonthly['month'], iCESMMonthly, label='iCESM', linestyle='-', color="orange")
plt.plot(vikingMonthly['month'], vikingMonthly, label='VIKING20X', linestyle='-', color="blue")

## formatting the graph
plt.xlabel('Month  ')
plt.ylabel('Temperature')
plt.title('Temperature of Different Products')
plt.legend()
plt.grid(True)

# showing the graph
plt.show()

ds = xr.open_dataset("./iCESM/iCESMSalt.nc")
iCESM = ds.mean(dim=['z_t', 'nlat', 'nlon'])

## getting just the month and year
print("Extracting month and year...")
iCESM['month'] = iCESM['time'].dt.month
iCESM['year'] = iCESM['time'].dt.year

iCESM = iCESM.assign_coords(year=iCESM['time'].dt.year,month=iCESM['time'].dt.month)

print("Computing monthly means...")
iCESMMonthly =  iCESM['SALT'].groupby('month').mean('time')

ds = xr.open_dataset("./VIKING20X/vikingSALT.nc")
viking = ds.mean(dim=['deptht', 'y', 'x'])

## getting just the month and year
print("Extracting month and year...")
viking['month'] = viking['time_counter'].dt.month
viking['year'] = viking['time_counter'].dt.year

viking = viking.assign_coords(year=viking['time_counter'].dt.year,month=viking['time_counter'].dt.month)

print("Computing monthly means...")
vikingMonthly =  viking['vosaline'].groupby('month').mean('time_counter')

## plotting the graph
plt.figure(figsize=(12, 6))
plt.plot(sodaMonthly['month'], sodaMonthly['temp'], label='SODA', linestyle='-', color = "green")
plt.plot(iCESMMonthly['month'], iCESMMonthly, label='iCESM', linestyle='-', color="orange")
plt.plot(vikingMonthly['month'], vikingMonthly, label='VIKING20X', linestyle='-', color="blue")

## formatting the graph
plt.xlabel('Month  ')
plt.ylabel('Salinity')
plt.title('Salinity of Different Products')
plt.legend()
plt.grid(True)

# showing the graph
plt.show()

