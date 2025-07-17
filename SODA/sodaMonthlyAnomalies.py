## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd
import matplotlib.pyplot as plt

## calculating the temp and salt anomalies for each month
def calcSodaAnoms(sodaRawFile):
    ## loading in the combined .csv file
    print("Loading file...")
    sodaRaw = pd.read_csv(sodaRawFile)
    print("Checking columns...", sodaRaw.columns)

    ## converting from string to date-time object
    print("Converting time column...")
    sodaRaw['time'] = pd.to_datetime(sodaRaw['time'], format= 'mixed')
    sodaRaw['time'] = sodaRaw['time'].dt.to_period('M')

    ## getting just the month and year
    print("Extracting month and year...")
    sodaRaw['month'] = sodaRaw['time'].dt.month
    sodaRaw['year'] = sodaRaw['time'].dt.year

    print("Computing daily mean temp and salinity...")
    sodaAnom = sodaRaw.groupby(['time', 'month'], as_index=False).agg({'temp': 'mean', 'salt': 'mean'})

    print("Computing monthly means...")
    monthly_means = sodaAnom.groupby('month', as_index=False).agg({'temp': 'mean', 'salt': 'mean'})

    print("Merging anomalies with original data...")
    sodaAnom = sodaAnom.merge(monthly_means, on="month", suffixes=("", "_mean"))

    print("Calculating anomalies...")
    sodaAnom["tempAnoms"] = sodaAnom["temp"] - sodaAnom["temp_mean"]
    sodaAnom["saltAnoms"] = sodaAnom["salt"] - sodaAnom["salt_mean"]

    print("Returning results.")
    return sodaAnom[["time", "tempAnoms", "saltAnoms"]]

sodaAnoms = calcSodaAnoms("./csv_clean/megaCSV.csv")
print(sodaAnoms.head())

## creating a new data frame from the anomalies
data = sodaAnoms.copy()

## formatting time properly
data['time'] = data['time'].astype(str)
data['time'] = pd.to_datetime(data['time'], format='%Y-%m')

## plotting the graph
plt.figure(figsize=(12, 6))
plt.plot(data['time'], data['tempAnoms'], label='Temp Anomalies', linestyle='-', color='#008080')  # Teal
plt.plot(data['time'], data['saltAnoms'], label='Salt Anomalies', linestyle='-', color='#D2691E')  # Dark Orange

## formatting the graph
plt.xlabel('Time')
plt.ylabel('Anomaly Value')
plt.title('Temperature and Salinity Anomalies Over Time')
plt.legend()
plt.grid(True)

# showing the graph
plt.show()

