from flask import Flask, request
import tweepy
from tweepy import OAuthHandler
import json
from textblob import TextBlob
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

consumer_key = '****************'
consumer_secret = '****************'
access_token = '****************'
access_token_secret = '****************'
auth = OAuthHandler(consumer_key , consumer_secret)
auth.set_access_token(access_token , access_token_secret)
api = tweepy.API(auth)


app = Flask(__name__)


@app.route('/')
def home():
    return app.send_static_file('home.html')


@app.route('/getDetails', methods=['POST'])
def getDetails():
    print("Inside getDetails")
    keyword = request.form['keyword']
    count = request.form['count']
    city = request.form['city']
    getTweets(keyword , count , city)
    data = getWords()
    return json.dumps(data)


def getTweets(keyword , count , city):
    tweets = []
    latitude = ""
    longitude = ""
    distance = ""
    with open('country.json', 'r') as file:
        city_data = [json.loads(line) for line in file]
        for data in city_data:
            if city == data['city']:
                latitude = data['latitude']
                longitude = data['longitude']
                distance = data['distance']
    print(latitude, longitude, distance)
    geo_code = latitude + "," + longitude + "," + distance
    print(geo_code)
    with open('tweets.json' , 'w') as file :
        for tweet in tweepy.Cursor(api.search , q = keyword , count = count , lang = 'en' , geocode = geo_code).items(int(count)):
            tweets.append(tweet)
        print("\n".join(str(i) for i in tweets))
        for t in tweets:
            json.dump(t._json , file)
            file.write("\n")


def tokenize(t):
    tokenizer = RegexpTokenizer(r'\w+')
    t = tokenizer.tokenize(t)
    return t


def Stemming(t):
    stemming = []
    ps = PorterStemmer()
    for i in t:
        stemming.append(ps.stem(i))
    return stemming


def getWords():
    ptweets = []
    ntweets = []
    neutraltweets = []

    with open('tweets.json', 'r') as datafile:
        json_data = [json.loads(line) for line in datafile]
        tweets = [data['text'] for data in json_data]
        total_polarity = []
        ppolarity = []
        npolarity = []
        for t in tweets:
            t = tokenize(t)
            stemming = Stemming(t)
            for k in stemming:
                polarity = TextBlob(k).sentiment.polarity
                if polarity > 0:
                    ptweets.append(k)
                    total_polarity.append(polarity)
                    ppolarity.append(polarity)
                elif polarity < 0:
                    ntweets.append(k)
                    total_polarity.append(polarity)
                    npolarity.append(polarity)
                elif polarity == 0:
                    neutraltweets.append(k)

    words = []
    word = "text"
    frequency = "weight"
    sentiment = "sentiment"
    ptweets = Counter(ptweets)
    ntweets = Counter(ntweets)
    print(sum(total_polarity))
    print(sum(ppolarity))
    print(sum(npolarity))
    words.append({"polarity": "polarity", "total_polarity": sum(total_polarity)})
    for k , v  in ptweets.items():
        words.append({word: k , frequency: v, sentiment: "positive"})
    for k , v  in ntweets.items():
        words.append({word: k , frequency: v, sentiment: "negative"})
    return words


if __name__ == '__main__':
    app.run()
