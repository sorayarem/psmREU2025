## code modified from branwen williams' 
## marine calcifier psm (2024)
## developed by soraya remaili
import pandas as pd

## calculating d18O anomalies from the bivalve record
def calcOxyIsoAnoms(d18ORaw):
  ## loading the data
  d18ORaw = pd.read_csv(d18ORaw)
  ## computing avg d18O
  d18OAvg = d18ORaw["seguinIso"].mean()     
  ## computing the anomalies 
  d18ORaw["d18OAnoms"] = d18ORaw["seguinIso"] - d18OAvg
  return d18ORaw[["year", "d18OAnoms"]]

def processFile(d18ORaw):
  ## loading the data
  d18ORaw = pd.read_csv(d18ORaw)
  return d18ORaw[["year", "seguinIso"]]

## storing the result of the function
d18OAnoms = calcOxyIsoAnoms("./d18O_data/seguin")
d18OData = processFile("./d18O_data/seguin")