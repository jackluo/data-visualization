# In[]:
# Import required libraries
import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as ts
import cufflinks as cf


# In[]:
# Time series model
cf.go_offline()

# Views
m = np.log(250)  # Trend base
dm = np.log(1.0007)  # Trend drift
s = [0.12, 0.15, 0.10, 0.11, 0.05, -0.32, -0.37]  # Weekly seasonality
sigma = [0.1, 0.1, 0.07, 0.25, 0.05, 0.17, 0.17]  # Residual variance

# Jump diffusion
lamda = 2/365  # Annual probability
mu = 0.5  # Average EV
delta = 0.25  # Jump volatility

# Cumulative jump diffusion
cum_lambda = 15/365
cum_mu = 0.01
cum_delta = 0.10

# Ratios for other metrics
visit_ratio = 2.2
visit_sigma = 0.1
visit_jump_ratio = 1.25
visit_jump_sigma = 0.75
conversion_rate = 0.07
conversion_sigma = 0.25


# In[]:
# Make time series

# Make sure data look too much like a straight up exponential curve
stationarity_threshold = -1

while True:

    ls = []
    cum_poi = 0

    for i in range(1825):

        m += dm
        # Poission process
        poi = np.random.poisson(lamda) * np.random.normal(mu, delta)
        # Cumulative poisson process
        dcum_poi = np.random.poisson(cum_lambda) * np.random.normal(cum_mu, cum_delta)
        cum_poi += dcum_poi

        views = np.exp(
            m +
            s[i % 7] +
            1/2 * 0.5 * np.random.normal(0, sigma[i % 7]) +
            cum_poi
        )

        visits = views / (visit_ratio * np.exp(np.random.normal(0, visit_sigma)))
        views_jumped = views * np.exp(poi)
        visits += (views_jumped - views) / max(1, (visit_jump_ratio * np.exp(np.random.normal(0, visit_jump_sigma))))
        conversions = visits * (conversion_rate * np.exp(np.random.normal(0, conversion_sigma)))

        ls.append([views_jumped, visits, conversions])

    df = pd.DataFrame(ls)
    df = df.round(decimals=0)
    df.columns = ['Views', 'Visits', 'Conversions']

    # Stationarity test
    result = ts.adfuller(df['Views'].values)

    if result[0] < stationarity_threshold and df['Views'].values[-1] > df['Views'].values[0]:
        break

df['Pages / Visit'] = df['Views']/df['Visits']
df['Conversion Rate'] = df['Conversions']/df['Visits']
df.iplot(fill=True, margin=(40,10,40,10))
df.to_csv('data/traffic.csv')
