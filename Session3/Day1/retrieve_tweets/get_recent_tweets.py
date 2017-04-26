import tweepy

def get_recent_tweets(N, twitter_acct):
    consumer_key = "bhzpKBdspYr2xSDb0RxpI586q"
    consumer_secret = "FfddeX3qatIeXoA51LJbgHs4qNsYAoNoWIqnlMISr3E7P4x03L"
    access_key = "855466876364877825-pUkJcfH48x3rEnlFKvSLJaWZ0jzg6Nc"
    access_secret = "9JHPalnxb6PVineBeCFFU5L98PD7EMOUBuwemM8vj8hA9"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name=twitter_acct, count=N)

    return [tweet.text for tweet in tweets]
