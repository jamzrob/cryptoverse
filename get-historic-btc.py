import snscrape.modules.twitter as sntwitter
import json
from pymongo import MongoClient
from textblob import TextBlob
import cryptocompare
from datetime import datetime

def dateToInt(date):
    return int(date.replace('-', ''))

def main():
    MONGO_HOST= 'mongodb://localhost/cryptoverse'
    client = MongoClient(MONGO_HOST)
    db = client.cryptoverse

    btc_prices = cryptocompare.get_historical_price_day('BTC', curr='USD')

    for i, price in enumerate(btc_prices):

        if dateToInt('2020-08-01') <= dateToInt(datetime.fromtimestamp(price['time']).strftime('%Y-%m-%d')) <= dateToInt('2020-11-01'):
            price['date'] = datetime.fromtimestamp(price['time']).strftime('%Y-%m-%d')
            db.btc_prices.insert_one(price)


if __name__ == "__main__":
    main()
