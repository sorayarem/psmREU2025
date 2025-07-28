## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd

## calculating d18O anomalies from the bivalve record
def calcOxyIsoAnoms(d18ORaw):
  ## loading the data
  d18ORaw = pd.read_csv(d18ORaw)
  ## computing avg d18O
  d18OAvg = d18ORaw["delmarvaIso"].mean()     
  ## computing the anomalies 
  d18ORaw["d18OAnoms"] = d18ORaw["delmarvaIso"] - d18OAvg
  return d18ORaw[["year", "d18OAnoms"]]

## returning the trimmed raw data
def processFile(d18ORaw):
  ## loading the data
  d18ORaw = pd.read_csv(d18ORaw)
  return d18ORaw[["year", "delmarvaIso"]]

## storing the result of the function
d18OAnoms = calcOxyIsoAnoms("./d18O_data/delmarva")
d18OData = processFile("./d18O_data/delmarva")