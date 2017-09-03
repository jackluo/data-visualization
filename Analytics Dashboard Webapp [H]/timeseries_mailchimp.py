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
m = np.log(100)  # Trend base
dm = np.log(1.001)  # Trend drift
s = [-0.23, 0.14, 0.35, 0.33, 0.14, -0.21, -0.47]  # Weekly seasonality
sigma = [0.21, 0.14, 0.05, 0.45, 0.15, 0.17, 0.17]  # Residual variance


# Ratios for other metrics
send_rate = 0.92
send_sigma = 0.2
delivery_rate = 0.91
delivery_sigma = 0.02
open_rate = 0.45
open_sigma = 0.20
conversion_rate = 0.12
conversion_sigma = 0.25


# In[]:
# Make time series

# Make sure data look too much like a straight up exponential curve
stationarity_threshold = 20

while True:

    ls = []
    cum_poi = 0

    for i in range(1825):

        m += dm
        recipients = np.exp(
            m +
            0.25 * s[i % 7] +
            1/2 * 3 * np.random.normal(0, sigma[i % 7])
        )

        sends = recipients * (send_rate * min(1, np.exp(np.random.normal(0, send_sigma))))
        deliveries = sends * (delivery_rate * np.exp(np.random.normal(0, delivery_sigma)))
        opens = deliveries * (open_rate * np.exp(np.random.normal(0, open_sigma)))
        conversions = opens * (conversion_rate * np.exp(np.random.normal(0, conversion_sigma)))

        ls.append([recipients, sends, deliveries, opens, conversions])

    df = pd.DataFrame(ls)
    df = df.round(decimals=0)
    df.columns = ['Recipients', 'Sends', 'Deliveries', 'Opens', 'Conversions']

    # Stationarity test
    result = ts.adfuller(df['Sends'].values)

    break
    # if result[0] < stationarity_threshold and df['Views'].values[-1] > df['Views'].values[0]:
    #     break

df['Send Rate'] = df['Sends']/df['Recipients']
df['Delivery Rate'] = df['Deliveries']/df['Sends']
df['Open Rate'] = df['Opens']/df['Deliveries']
df['Conversion Rate'] = df['Conversions']/df['Opens']
df.iplot(fill=True, margin=(40,10,40,10))
df.to_csv('data/mailchimp.csv')
