import sys
import json
import requests
from requests_oauthlib import OAuth1




def get_authenticated():

    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""
    ACCESS_KEY = ""
    ACCESS_SECRET = ""

    auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)

    return auth

def get_count_of_tweet(user_handle, URL, auth):

    URL = URL + "?screen_name={}".format(user_handle)

    try:
        response = requests.get(URL, auth=auth)
    except requests.exceptions.RequestException:
        print('No internet connection')
        sys.exit(1)

    data = response.json()
    count = data[0]["user"]["statuses_count"]

    return count

def get_json_data(user_handle, URL, no_of_tweets, auth):

    URL = URL + \
        "?screen_name={}&tweet_mode=extended&count={}".format(
            user_handle, no_of_tweets)

    try:
        response = requests.get(URL, auth=auth)
    except requests.exceptions.RequestException:
        print('No internet connection')
        sys.exit(1)

    data = response.json()

    return data

def save_data_into_file(data):

    with open('tweet.json', 'w') as f:
        json.dump(data, f, indent=4)

def main():

    user_handle = "midasIIITD"
    URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

    auth = get_authenticated()
    no_of_tweets = get_count_of_tweet(user_handle, URL, auth)
    data = get_json_data(user_handle, URL, no_of_tweets, auth)
    save_data_into_file(data)


if __name__ == '__main__':
    main()


def get_all_media_count(tweet):
    count = 0

    if 'extended_entities' in tweet:
        try:
            count += len(tweet['extended_entities']['media'])
        except KeyError:
            pass

    elif 'media' in tweet['entities']:
        count += len(tweet['entities']['media'])

   
    if 'retweeted_status' in tweet:
        count += get_all_media_count(tweet['retweeted_status'])

    return count