from flask import Flask, request
import tweepy
from tweepy import OAuthHandler
import json
from textblob import TextBlob
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

consumer_key = 'cWwaOeIWLg6rpFAuSZqBkunKb'
consumer_secret = 'Vwl97myDiV71L0F4yL4X5zHyV0Qdg7N2WV2UtPh0DGyCd90oKS'
access_token = '1518593928-36tTKvBP2v9TxcXLBB3LlczT475cnYvOcTCYxPG'
access_token_secret = 'uBQNmqPToLnhyabdRfr5OJSbM1Ysnqygf8zwt5V6cFkK2'
auth = OAuthHandler(consumer_key , consumer_secret)
auth.set_access_token(access_token , access_token_secret)
api = tweepy.API(auth)


app = Flask(__name__)


@app.route('/')
def home():
    return app.send_static_file('companyAnalysis.html')


@app.route('/getData', methods=['POST'])
def getData():
    print("Inside getData")
    company1 = request.form['comp1']
    company2 = request.form['comp2']
    getCompany1Tweets(company1)
    getCompany2Tweets(company2)
    data = getGraphData(company1 , company2)
    return json.dumps(data)


def getCompany1Tweets(company1):
    print("Getting tweets")
    tweets = []
    count = 1000
    with open('company1.json' , 'w') as file :
        for tweet in tweepy.Cursor(api.search , q = company1 , count = count , lang = 'en').items(int(count)):
            tweets.append(tweet)
        print("\n".join(str(i) for i in tweets))
        for t in tweets:
            json.dump(t._json , file)
            file.write("\n")


def getCompany2Tweets(company2):
    tweets = []
    count = 1000
    with open('company2.json' , 'w') as file :
        for tweet in tweepy.Cursor(api.search , q = company2 , count = count , lang = 'en').items(int(count)):
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


def getGraphData(company1 , company2):
    with open('company1.json', 'r') as datafile:
        json_data = [json.loads(line) for line in datafile]
        tweets = [data['text'] for data in json_data]
        total_polarity_company1 = []
        for t in tweets:
            t = tokenize(t)
            stemming = Stemming(t)
            for k in stemming:
                polarity = TextBlob(k).sentiment.polarity
                if polarity > 0:
                    total_polarity_company1.append(polarity)
                elif polarity < 0:
                    total_polarity_company1.append(polarity)

    with open('company2.json', 'r') as datafile:
        json_data = [json.loads(line) for line in datafile]
        tweets = [data['text'] for data in json_data]
        total_polarity_company2 = []
        for t in tweets:
            t = tokenize(t)
            stemming = Stemming(t)
            for k in stemming:
                polarity = TextBlob(k).sentiment.polarity
                if polarity > 0:
                    total_polarity_company2.append(polarity)
                elif polarity < 0:
                    total_polarity_company2.append(polarity)


    words = []
    word = "text"
    frequency = "weight"
    print(sum(total_polarity_company1))
    print(sum(total_polarity_company2))
    words.append({word: company1 , frequency: sum(total_polarity_company1)})
    words.append({word: company2 , frequency: sum(total_polarity_company2)})
    print(words)
    return words


if __name__ == '__main__':
    app.run()