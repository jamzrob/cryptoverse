
import pandas as pd
pd.options.plotting.backend = "plotly"
from datetime import datetime
from pymongo import MongoClient
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def main():

    MONGO_HOST= 'mongodb://localhost/cryptoverse'
    client = MongoClient(MONGO_HOST)
    db = client.cryptoverse


    btc_prices = [{'date': b['date'], 'price': b['high']} for b in db.btc_prices.find()]
    btc_prices_df =  pd.DataFrame.from_dict(btc_prices).groupby(['date'])['price'].mean()

    print(btc_prices_df)

    btc_tweets = [b for b in db.bitcoin_tweets.find()]
    btc_tweets_df = pd.DataFrame.from_dict(btc_tweets).groupby('date')['polarity'].mean()
    btc_tweets_agg = pd.DataFrame(btc_tweets_df).to_dict()

    print(btc_tweets_df)
    merged_df = pd.merge(btc_prices_df, btc_tweets_df, on='date')
    print(merged_df)
    merged_df.plot().show()
    merged = list(merged_df.to_dict().values())

    print(merged)


    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=[b['date'] for b in btc_prices], y=[b['price'] for b in btc_prices], name="Bitcoin Price"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=[b['date'] for b in btc_prices], y=[row['polarity'] for index, row in merged_df.iterrows()], name="Twitter Sentiment"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Bitcoin Price versus Twitter Sentiment"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="Bitcoin Price", secondary_y=False)
    fig.update_yaxes(title_text="Twitter Sentiment", secondary_y=True)

    fig.show()









if __name__ == "__main__":
    main()
