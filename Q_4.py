import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Packages from fire_pytools
from utils.monthly_date import *

from portools.find_breakpoints import find_breakpoints
from portools.sort_portfolios import sort_portfolios

#Directory in my computer where files are stored
directory = 'D:/Gautham/Columbia/Coursework/Semester 2/B9334-Big Data in Finance/Lira Mota/big_data2020/'

#Reading PKL File outputted by stock_monthly.py code
raw_df = pd.read_pickle(directory + 'homeworks/hm_ii/output/stock_annual.pkl')

#Set names
raw_df.drop(columns='inv', inplace=True)
raw_df.rename(columns={'mesum_june': 'me', 'inv_gvkey': 'inv'}, inplace=True) #inv_permco

# %% Create Filters
# shrcd must be (10,11)
print('Data deleted due to shrcd: %f' % np.round((1-raw_df.shrcd.isin([10, 11]).mean())*100, 2))
sort_data = raw_df[raw_df.shrcd.isin([10, 11])].copy()

# exchcd must be (1, 2, 3)
# ------------------------
print('Data deleted due to exchcd: %f' % np.round((1-sort_data.exchcd.isin([1, 2, 3]).mean())*100, 2))
sort_data = sort_data[sort_data.exchcd.isin([1, 2, 3])]

# %% Portfolio Sorts
## ME X BEME
# notice that the way we defined beme or beme is null if be<=0
sample_filters = ((sort_data.me > 0) &
                  (sort_data.mesum_dec > 0) &
                  (sort_data.beme.notnull()))

beme_sorts = sort_portfolios(data=sort_data[sample_filters],
                             quantiles={'me': [0.5], 'beme': [0.3, 0.7]},
                             id_variables=['rankyear', 'permno', 'exchcd'],
                             exch_cd=[1]
                             )

#Merging Sorted Data with beme_sorts for summing
merged_df = pd.merge(sort_data, beme_sorts, on = ['permno', 'rankyear'], how = 'inner')
merged_df = merged_df[['rankyear', 'bemeportfolio', 'be', 'me']]
merged_df['be_sum'] = merged_df.groupby(['rankyear', 'bemeportfolio'])['be'].transform('sum')
merged_df['me_sum'] = merged_df.groupby(['rankyear', 'bemeportfolio'])['me'].transform('sum')

#Dropping duplicates and calculating the ratio
merged_df = merged_df.drop_duplicates(['rankyear', 'bemeportfolio'])
merged_df['spread'] = np.log((merged_df['be_sum'] / merged_df['me_sum']))
#Sorting
merged_df = merged_df.sort_values(['rankyear', 'bemeportfolio'])

#Plotting
fig, ax = plt.subplots()
for name, group in merged_df.groupby('bemeportfolio'):
    group.plot(x = 'rankyear', y = 'spread', ax = ax, label = name)
plt.show()