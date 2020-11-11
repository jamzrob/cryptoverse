import snscrape.modules.twitter as sntwitter
import json
from pymongo import MongoClient
from textblob import TextBlob
from datetime import timezone
from datetime import datetime



def main():
    MONGO_HOST= 'mongodb://localhost/cryptoverse'

    maxTweets = 10000  # the number of tweets you require
    three_month_btc_query = "(bitcoin OR btc) -giveaway min_faves:100 lang:en until:2020-11-01 since:2020-08-01 -filter:links -filter:replies"

    client = MongoClient(MONGO_HOST)
    db = client.cryptoverse

    tweets = sntwitter.TwitterSearchScraper(three_month_btc_query).get_items();

    for i,tweet in enumerate(tweets):
            if i > maxTweets :
                break

            try:
                analysis = TextBlob(tweet.content)


                tweet_object = {
                    "url": tweet.url,
                    "date": tweet.date.strftime('%Y-%m-%d'),
                    "time": tweet.date.replace(tzinfo=timezone.utc).timestamp(),
                    "content": tweet.content,
                    "username": tweet.username,
                    "polarity": analysis.sentiment.polarity,
                    "subjectivity": analysis.sentiment.subjectivity
                }

                #grab the 'created_at' data from the Tweet to use for display
                date = tweet_object['date']
                content = tweet_object['content']

                print(date)

                db.bitcoin_tweets.insert_one(tweet_object)


            except Exception as e:
               print(e)

if __name__ == "__main__":
    main()
