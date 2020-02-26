import pandas as pd

#Directory in my computer where files are stored
directory = 'D:/Gautham/Columbia/Coursework/Semester 2/B9334-Big Data in Finance/Lira Mota/big_data2020/'

#Reading PKL File Outputted by stock_monthly.py code
raw_df = pd.read_pickle(directory + 'homeworks/hm_ii/output/stock_monthly.pkl')
#Subsetting Returns for December 2019
dec_2019_df = raw_df[raw_df['date'] == '2019-12-31']

#Question 1
#Printing the total number of missing values
print('Number of missings in December 2019:', dec_2019_df['cret'].isna().sum())
#Printing the number of unique permons:
print('Number of unique permnos in December 2019:', dec_2019_df['permno'].nunique())
#Printing the average, minimum and maxmium for variable ret_11_1:
print('Average of ret_11_1 in December 2019:', round(dec_2019_df['cret'].mean(), 5))
print('Minimum of ret_11_1 in December 2019:', round(dec_2019_df['cret'].min(), 5))
print('Maximum of ret_11_1 in December 2019:', round(dec_2019_df['cret'].max(), 5))

#Question 2
dec_2019_df_high = dec_2019_df.nlargest(10, 'cret')
#printing by ticker
print('Tickers of the top 10 firms that had the highest 11-months performance returns as December 2019: \n' + 
      dec_2019_df_high['ticker'].to_string(index = False))

#Question 3
dec_2019_df_low = dec_2019_df.nsmallest(10, 'cret')
#printing by ticker
print('Tickers of the top 10 firms that had the lowest 11-months performance returns as December 2019: \n' + 
      dec_2019_df_low['ticker'].to_string(index = False))