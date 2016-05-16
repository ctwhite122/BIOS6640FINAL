# -*- coding: utf-8 -*-
"""
Created on Tue May 10 09:27:57 2016

@author: Chris White
"""
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from time import gmtime, strftime
pd.set_option('display.height', 500)
pd.set_option('display.max_rows', 500)

tweets_data_path = 'C:/Users/Admin/Documents/Python Scripts/data/fetched_tweets.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

print len(tweets_data)

#STEPS FOR SAMPLE DATASET
#Create sample data sets for data management, first a list
tweets_sample = tweets_data[0:1000]
#Create data frame of sample data
tweets_sampledf = pd.DataFrame(tweets_data[0:1000])
#Because 'user' has lists instead of single values, create dataframe of these lists
tweets_sampledfuser = pd.DataFrame(tweets_sampledf['user'].tolist())

#Merge the sub-list dataframe to the whole sample dataset
tweets_sampledfmerge = pd.concat([tweets_sampledf, tweets_sampledfuser, ], axis=1)
#Select specific columns for analysis
tweets_sampleanalysis = tweets_sampledfmerge[['created_at', 'geo', 'lang', 'place', 'text', 'location', 'time_zone']]
#2 columns named 'created_at' and 'lang'. Delete date user created account.
tweets_sampleanalysis.columns = ['tweet_time', 'created_at', 'geo', 'language', 'user_location', 'place', 'text', 'user_location', 'time_zone']
del tweets_sampleanalysis['created_at']

#Subset only tweets with location, and count number of tweets with location
tweetswithplace = tweets_sampleanalysis['place'].dropna()
tweetswithplacedf = pd.DataFrame(tweetswithplace.tolist())
count_row = tweetswithplacedf.shape[0]
count_row

#Create column of month and day from 'tweet_time', selecting only a subset of date string
tweets_sampleanalysis['month_day'] = tweets_sampleanalysis['tweet_time'].str[4:10]
tweets_sampleanalysis[0:10]

#Decide how to group tweets: month_day, country, time_zone, language, user_location, etc
#NEXT: Test grouping and doing simple counts per group

#Tweet counts grouped by Language
tweets_by_lang = tweets_sampleanalysis['language'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 Languages For Zika Tweets', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')

#Tweet counts grouped by country
tweets_by_country = tweetswithplacedf['country'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 Countries for Zika Tweets', fontsize=15, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')

#Tweet counts grouped by day of the week
tweets_by_day = tweets_sampleanalysis['month_day'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Tweets by Day', fontsize=15, fontweight='bold')
tweets_by_day.plot(ax=ax, kind='bar', color='blue')

#Tweet counts grouped by time zone
tweets_by_timezone = tweets_sampleanalysis['time_zone'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Tweets by Time Zone', fontsize=15, fontweight='bold')
tweets_by_timezone[:10].plot(ax=ax, kind='bar', color='blue')


#STEPS FOR FULL DATASET
#Create data frame of full data
tweets_df = pd.DataFrame(tweets_data)
#Certain rows have empty information except for 'limit', delete these
#Get these rows
tweets_todelete = tweets_df['limit'].dropna()
tweets_todelete.index
#Delete these rows
tweets_dfnew = tweets_df.drop(tweets_todelete.index)
#Because 'user' has lists instead of single values, create dataframe of these lists
tweets_dfuser = pd.DataFrame(tweets_dfnew['user'].tolist())

#Merge the sub-list dataframe to the whole dataset
tweets_dfmerge = pd.concat([tweets_dfnew, tweets_dfuser, ], axis=1)
#Select specific columns for analysis
tweets_analysis = tweets_dfmerge[['created_at', 'lang', 'place', 'text', 'location', 'time_zone']]
#2 columns named 'created_at' and 'lang'. Delete date user created account.
tweets_analysis.columns = ['tweet_time', 'created_at', 'language', 'user_defined_lang', 'place', 'text', 'user_location', 'time_zone']
del tweets_analysis['created_at']

#Subset only tweets with location, and count number of tweets with location
tweetswithplace = tweets_analysis['place'].dropna()
tweetswithplacedf = pd.DataFrame(tweetswithplace.tolist())
count_row = tweetswithplacedf.shape[0]
count_row
tweetswithplace_city = pd.DataFrame(tweetswithplacedf.loc[tweetswithplacedf['place_type'] == 'city'])

tweetswithplace_ventura = pd.DataFrame(tweetswithplacedf.loc[tweetswithplacedf['full_name'] == 'Ventura, CA'])
tweets_ventura = tweets_analysis.iloc[tweetswithplace_ventura.index]


#FOR TWEETS with PLACE DATA plot country, name
#3345 tweets have place data
tweetswithplace_country = tweetswithplacedf['country'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Country', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Tweets with Place: Top 5 Countries', fontsize=15, fontweight='bold')
tweetswithplace_country[:5].plot(ax=ax, kind='bar', color='red')

tweetswithplace_name = tweetswithplace_city['full_name'].value_counts()
tweetswithplace_name[0:10]

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('City', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 Cities for Zika Tweets', fontsize=15, fontweight='bold')
tweetswithplace_name[:5].plot(ax=ax, kind='bar', color='red')

#FOR ALL TWEETS INCLUDING THOSE WITH PLACE DATA
#Create column of month and day from 'tweet_time', selecting only a subset of date string
tweets_analysis['month_day'] = tweets_analysis['tweet_time'].str[4:10]


#Tweet counts grouped by Language
tweets_by_lang = tweets_analysis['language'].value_counts()
tweets_by_lang[0:5]
tweets_analysis['language'].isnull().sum()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 Languages For Zika Tweets', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')

#Tweet counts grouped by country
tweets_by_country = tweetswithplacedf['country'].value_counts()
tweets_by_country[0:5]


fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 Countries for Zika Tweets', fontsize=15, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='red')

#Tweet counts grouped by day of the week
tweets_by_day = pd.DataFrame(tweets_analysis['month_day'].value_counts())
tweets_by_day_sort = tweets_by_day.sort()

tweets_analysis['month_day'].isnull().sum()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Date', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Zika Tweets by Date', fontsize=15, fontweight='bold')
tweets_by_day_sort.plot(ax=ax, kind='bar', color='green')

#Tweet counts grouped by time zone
tweets_by_timezone = tweets_analysis['time_zone'].value_counts()
tweets_by_timezone[0:10]
tweets_by_timezone

tweets_analysis['time_zone'].isnull().sum()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Time Zone', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 10 Time Zones for Zika Tweets', fontsize=15, fontweight='bold')
tweets_by_timezone[:10].plot(ax=ax, kind='bar', color='blue')



