
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[1]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np
get_ipython().magic('matplotlib inline')
def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'key')


# In[101]:

def load_data():
    df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/key.csv',
                     parse_dates= ['Date'])
    df = df[~((df.Date.dt.month == 2) & (df.Date.dt.day == 29))]
    return df


# In[66]:

from datetime import datetime
import time
data = load_data()


# In[100]:

# Manipulating data for processing
data['group'] = data['Date'].apply(lambda x: datetime.strptime(str(x.date()),'%Y-%M-%d').strftime('%M-%d'))
data['DayofYear'] = data.Date.dt.dayofyear


# In[80]:

# Data upto 2015
sliced = data[data.Date <= datetime.strptime('2014-12-31','%Y-%M-%d')]
sliced=sliced.sort_values('Date')
# Data for 2015
df_2015 = data[data.Date > datetime.strptime('2014-12-31','%Y-%M-%d')]
df_2015=df_2015.sort_values('Date')


# In[99]:

# Creating separate TMIN and TMAX frames
min_set=sliced.loc[sliced.groupby(['group']).Data_Value.idxmin()]
min_set=min_set.reset_index()
max_set=sliced.loc[sliced.groupby(['group']).Data_Value.idxmax()]
max_set = max_set.reset_index()

# Creating separate TMIN and TMAX frames for 2015
min_2015=df_2015.loc[df_2015.groupby(['group']).Data_Value.idxmin()]
min_2015=min_2015.reset_index()
max_2015=df_2015.loc[df_2015.groupby(['group']).Data_Value.idxmax()]
max_2015 = max_2015.reset_index()

# Check record high and low
min_2015 = min_2015[min_2015.Data_Value < min_set.Data_Value]
max_2015 = max_2015[max_2015.Data_Value > max_set.Data_Value]

# Plotting of data 
plt.scatter(max_2015.DayofYear, max_2015.Data_Value, label = 'Record High 2015', color= 'green')
plt.scatter(min_2015.DayofYear, min_2015.Data_Value, label = 'Record Low 2015', color= 'red')
plt.plot(max_set.DayofYear, max_set.Data_Value,label='Max Temp')
plt.plot(min_set.DayofYear, min_set.Data_Value,label='Min Temp')
plt.legend(loc='lower center')
plt.fill_between(max_set.DayofYear, min_set.Data_Value, max_set.Data_Value, color='grey')
plt.xlabel('No. of Days')
plt.ylabel('Temperature')
plt.title('Record High and Low temperature (2005-2015)')
plt.show()


# In[ ]:



