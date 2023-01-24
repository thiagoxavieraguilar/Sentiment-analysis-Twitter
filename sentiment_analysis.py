import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import re
from textblob import TextBlob

#Authenticate with the Twitter API 
api_key = "YOUR_CONSUMER_KEY"
api_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

keyword  = input('Keyword: ')


try:
    #get only tweets
    search =  f'#{keyword} -filter:retweets '
    tweet_cursor = tweepy.Cursor(api.search_tweets, q=search, lang='en', tweet_mode='extend').items(100)
    tweets  = [tweet.text for tweet in tweet_cursor]
    tweets_df  = pd.DataFrame(tweets, columns=['Tweets'])
    
    for _, row in tweets_df.iterrows():
        # Remove links
        row['Tweets']  = re.sub("http\S+", "", row['Tweets'])
        # Remove hashtags
        row['Tweets'] = re.sub("#\S+", "", row['Tweets'])
        # Remove mentions
        row['Tweets'] = re.sub("@\S+", "", row['Tweets'])

        row['Tweets'] = re.sub("\\n", "", row['Tweets'])


    #gives a value between -1 and 1 representing the polarity of the sentiment (negative or positive)
    tweets_df['Polarity'] =  tweets_df['Tweets'].map(lambda tweet: TextBlob(tweet).sentiment.polarity)
    tweets_df['Result'] = tweets_df['Polarity'].map(lambda pol: '+' if pol > 0 else '-')

    positive = tweets_df[tweets_df.Result == '+'].count()['Tweets']
    negative = tweets_df[tweets_df.Result == '-'].count()['Tweets']


    x = [0, 1]
    y = [positive, negative]
    plt.bar(x, y, color=['g', 'r'])
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Tweets")
    plt.legend(['Positive', 'Negative']) # fix the legend
    plt.xticks([0, 1], ['Positive', 'Negative']) # change the x-coordinates
    plt.show()
except:
    print('error')