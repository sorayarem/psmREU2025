## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd

def getExpertYear(time):
    return time.year - int(time.month < 10)

## calculating the temp and salt anomalies for each month
def calcSodaAnoms(sodaRawFile):
    ## loading in the combined .csv file
    print("Loading file...")
    sodaRaw = pd.read_csv(sodaRawFile)
    print("Checking columns...", sodaRaw.columns)

    print(sodaRaw['time'].dtype)
    ## converting from string to date-time object
    ## converting to expert season
    print("Converting time column...")
    sodaRaw['time'] = pd.to_datetime(sodaRaw['time'], format= 'mixed')
    sodaRaw['expertYear'] = sodaRaw['time'].apply(getExpertYear)
    sodaRaw['time'] = sodaRaw['time'].dt.to_period('M')

    ## getting just the month and year
    print("Extracting month and year...")
    sodaRaw['month'] = sodaRaw['time'].dt.month
    sodaRaw['year'] = sodaRaw['expertYear']

    print("Computing monthly mean temp and salinity...")
    sodaAnom = sodaRaw.groupby(['time', 'year', 'month'], as_index=False).agg({'temp': 'mean', 'salt': 'mean'})

    print("Computing monthly means...")
    monthlyMeans = sodaAnom.groupby('month', as_index=False).agg({'temp': 'mean', 'salt': 'mean'})

    print("Merging anomalies with original data...")
    sodaAnom = sodaAnom.merge(monthlyMeans, on="month", suffixes=("", "_mean"))

    print("Calculating anomalies...")
    sodaAnom["tempAnoms"] = sodaAnom["temp"] - sodaAnom["temp_mean"]
    sodaAnom["saltAnoms"] = sodaAnom["salt"] - sodaAnom["salt_mean"]

    print("Computing annual means...")
    annualMeans = sodaAnom.groupby('year', as_index=False).agg({'tempAnoms': 'mean', 'saltAnoms': 'mean'})

    print("Returning results.")
    return annualMeans

sodaExpertAnoms = calcSodaAnoms("./csv_clean/georgesBankCSV.csv")

