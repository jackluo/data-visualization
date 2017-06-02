# In[]:
# Import required libraries
import pandas as pd
import pickle


# In[]:
# Load required dataframes
df = pd.read_csv('data/wellspublic.csv', low_memory=False,
                 index_col='API_WellNo')
dataset = df.to_dict(orient='index')

columns1 = ['API Well Number', 'Months in Production', 'Gas Produced, MCF',
            'Water Produced, bbl', 'Reporting Year']
columns2 = ['API Well Number', 'Months in Production', 'Gas Produced, MCF',
            'Water Produced, bbl', 'Oil Produced, bbl', 'Reporting Year']
df1 = pd.read_csv('data/Oil_and_Gas_Annual_Production__1985_-_2000.csv',
                  low_memory=False)[columns1]
df2 = pd.read_csv('data/Oil_and_Gas_Annual_Production__Beginning_2001.csv',
                  low_memory=False)[columns2]


# In[]:
# Concatenate dataframes
df = pd.concat([df1, df2])


# In[]:
# Append production data to each API
columns = ['Months in Production', 'Gas Produced, MCF', 'Water Produced, bbl',
           'Oil Produced, bbl', 'Reporting Year']
for api, df_well in df.groupby('API Well Number'):
    df_well = df_well[columns]
    df_well.index = df_well['Reporting Year']
    try:
        dataset[api]['Production'] = df_well
    except:
        print('Failed to find', api)


# In[]:
# Serialise to Pickle
with open('data/dataset.pickle', 'wb') as f:
    pickle.dump(dataset, f, protocol=pickle.HIGHEST_PROTOCOL)
