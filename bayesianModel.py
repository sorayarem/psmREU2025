## developed by soraya remaili
import pymc as pm
import numpy as np
import matplotlib.pyplot as plt

## known value for north atlantic
S = 0.97002

with pm.Model() as model:
    ## establishing the priors for the process levels
    mu = pm.Normal('mu', mu = 14.5, sigma = 10)
    phi = pm.Uniform('phi', lower = 0, upper = 1)
    sigmaT = pm.HalfCauchy('sigmaT', beta = 1)
    beta0 = pm.Normal('beta0', mu = 0, sigma = 10)
    beta1 = pm.Normal('beta1', mu = -0.22, sigma = 0.1)
    sigmaO = pm.HalfCauchy('sigmaT', beta = 1)
    sigmaP = pm.HalfCauchy('sigmaP', beta = 1)

    ## known values from the legrande paper
    alpha1 = -0.22
    alpha2 = 0.55

    ## model for the process level
    T = pm.AR('T', mu = mu, phi = phi, sigma = sigmaT, shape = years)

    ## models for the data level
    ## for the pseudocarbonate
    pseudo = pm.Normal('pseudo', mu = alpha1 * T + alpha2 * S, sigma = sigmaP, observed = dataPseudo)

    ## for the shell isotope records
    obs = pm.Normal('obs', mu = beta0 +beta1*T, sigma = sigmaO, observed = dataObs)

    trace = pm.sample(2000, return_inferencedata=True)






