from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

df=pd.read_csv("..\Raw Data\TrumpTweets.csv")

firstTweet = True
compound_list =[]
sentiments =[]
count =0

for index, row in df.iterrows():
    #Run Vader Analysis on each tweet
    sentence =row["text"]
    #Tweet datetime object
    new_date = row["created_at"]
    if(firstTweet == False):
        if(old_date != new_date):
            compound= np.mean(compound_list)
            compound_list =[]
            #Store the Sentiments
            sentiments.append({"Compound":compound,
                "Date" : old_date,
                "Count" : count})
            #Resetting count
            count =0
    else:
        firstTweet = False
    compound_list.append(analyzer.polarity_scores(sentence)["compound"])
    count +=1
    old_date = new_date
	
#Put all data into dataframe and export to csv file
sentiments_df = pd.DataFrame.from_dict(sentiments)

for index, row in sentiments_df.iterrows():
    #row['startdate']=row['startdate'].date()
    d= datetime.strptime(row['Date'], '%m/%d/%y')
    sentiments_df.loc[index, 'Date'] = d.strftime('%Y-%m-%d')
sentiments_df=sentiments_df.loc[(sentiments_df['Date'] > '2017-01-19') & (sentiments_df['Date'] < '2018-01-01')]