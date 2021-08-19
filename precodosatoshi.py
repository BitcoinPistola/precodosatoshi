### Imports
import tweepy
import schedule
import time
from datetime import datetime
from os import environ
from pycoingecko import CoinGeckoAPI

### Environment Variables
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

### API Initialization - Tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

### API Initialization - CoinGecko
cg = CoinGeckoAPI()

### Functions
## Tweet
def new_tweet():
    satoshi_price = get_satoshi_price()
    tweet = '\U0001f1e7\U0001f1f7 BRL - R$ ' + satoshi_price['brl'] + '\n' \
                + '\U0001f1fa\U0001f1f8 USD - $ ' + satoshi_price['usd'] + '\n' \
                + '\U0001f1ea\U0001f1fa EUR - € ' + satoshi_price['eur'] + '\n' \
                + '\U0001f1ef\U0001f1f5 JPY - ¥ ' + satoshi_price['jpy'] + '\n' \
                + '\U0001f1ec\U0001f1e7 GBP - £ ' + satoshi_price['gbp'] + '\n' \
                + '\U0001f1e8\U0001f1ed CHF - Fr ' + satoshi_price['chf'] + '\n' \
                + '\U0001f1e8\U0001f1f3 CNY - ¥ ' + satoshi_price['cny'] + '\n' \
                + '\U0001f1e6\U0001f1f7 ARS - $ ' + satoshi_price['ars'] + '\n' \
                + '\n' + 'Stack Sats!' + '\n' + '\n' + '#Bitcoin'

    # Try to tweet
    try:
        api.update_status(tweet)
        print(tweet)
    except Exception as error:
        print(error)

## Get bitcoin price from CoinGeckoAPI and calculate the satoshi price for each fiat currency
def get_satoshi_price():
        response = cg.get_price(ids='bitcoin', vs_currencies='brl, usd, eur, jpy, gbp, chf, cny, ars')
        bitcoin_price = response['bitcoin']
        satoshi_price = {'brl': 0, 'usd': 0, 'eur': 0, 'jpy': 0, 'gbp': 0, 'chf': 0, 'cny': 0, 'ars': 0}

        for key in bitcoin_price:
            satoshi_price[key] = bitcoin_price[key] / 100000000
            satoshi_price[key] = format(satoshi_price[key], '.8f')

        return satoshi_price

### Main
def main():
    schedule.every().hour.at(":00").do(new_tweet)
    while True:
        print('Bot running: ' + str(datetime.now()))
        schedule.run_pending()
        time.sleep(1)

### Start
if __name__ == '__main__':
    main()