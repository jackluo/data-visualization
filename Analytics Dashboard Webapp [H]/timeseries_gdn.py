# In[]:
# Import required libraries
import numpy as np
import pandas as pd
import cufflinks as cf


# In[]:
# Time series model
cf.go_offline()

# Impressions
mu = np.log(50000)
sigma = 0.20

# Ratios for other metrics
ctr = 0.0067
ct_sigma = 0.1
conversion_rate = 0.015
conversion_sigma = 0.15

cpc = 0.40
cpc_sigma = 0.20
max_budget = 100

# Make time series
ls = []
for i in range(1825):

    impressions = np.exp(mu + 1/2 * np.random.normal(0, sigma))
    clicks = impressions * ctr * np.exp(np.random.normal(0, ct_sigma))
    conversions = clicks * conversion_rate * np.exp(np.random.normal(0, conversion_sigma))
    cost = clicks * cpc * np.exp(np.random.normal(0, cpc_sigma))

    if cost > max_budget:
        impressions /= (cost/max_budget)
        clicks /= (cost/max_budget)
        cost = max_budget

    ls.append([impressions, clicks, conversions, cost])

df = pd.DataFrame(ls)
df[0] = df[0].round(decimals=0)
df[1] = df[1].round(decimals=0)
df[2] = df[2].round(decimals=0)
df[3] = df[3].round(decimals=2)
df.columns = ['Impressions', 'Clicks', 'Conversions', 'Cost']
df['CTR'] = df['Clicks']/df['Impressions']
df['Conversion Rate'] = df['Conversions']/df['Clicks']
df['CPM'] = df['Cost']/df['Impressions'] * 1000
df['CPC'] = df['Cost']/df['Clicks']
df['Cost / Conversion'] = df['Cost']/df['Conversions']

df.iplot(fill=True, margin=(40,10,40,10))
df.to_csv('data/gdn.csv')
