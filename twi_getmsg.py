import csv
import tweepy
import re, string, sys, csv
import pandas as pd
import oauth2 as oauth
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

consumer_key = "szz5uQacEbPqsMfedhwnpwolS"
consumer_secret = "3sh0Gb8KZnGU0wve0mjrqcSUFsv6TIluOWmWPAapyFVG9EXN2D"
access_token = "929536179648778240-yE3B1AD3WN7frvLEPAT6ECDPqdUhpU6"
access_token_secret = "FbloQf8uPHSbu2IE4XFqWlIL5iV2b2xzS5TDsx028Ksye"
store = []


class MyStreamListener(tweepy.StreamListener):
    # step1 creating a streamlistener
    msgstr = ''
    count = 10
    store = []
    dic1 = {}
    df1 = pd.DataFrame([dic1], columns = dic1.keys())

    def __init__(self, api, hashtag):
        self.api = api
        self.hashtag = hashtag

    def on_status(self, status):
        #dic1,dic2 = {}, {}
        #data1 = pd.DataFrame([dic1], columns = dic1.keys())
        msg = status._json['text'].encode("utf-8")
            # self.msgstr = "tweet: "+ msg
        self.msgstr = msg
        # print self.msgstr
        pmsg = self.pruner(self.msgstr)
        self.count -= 1
        if self.count == 0:
            #stransfer dataframe to csv
            self.df1.to_csv('result.csv', sep = ',', index = False)
            sys.exit("Searching finished")

        if len(pmsg) > 1 and '@' in pmsg.split(' ')[0]:
            id = pmsg.split()[0]
            pmsg = re.sub('[^a-zA-Z0-9\-\#\,\!\.\~\?\"\ \'\$]+', '', pmsg)
            dic2.update({'id':id,'msg':pmsg.split(" ", 1)[1]})
            #data1 = pd.DataFrame([dic1], columns = dic1.keys())
            df2 = pd.DataFrame([dic2], columns = dic2.keys())
            self.df1 = self.df1.merge(df2, how = "outer")

        # with open('./data.csv', 'a') as f:
        #     msg = status._json['text'].encode("utf-8")
        #     # self.msgstr = "tweet: "+ msg
        #     self.msgstr = msg
        #     # print self.msgstr
        #     pmsg = self.pruner(self.msgstr)
        #     self.count -= 1
        #     if self.count == 0:
        #         # print self.store
        #         sys.exit("Searching finished")
        #     if len(pmsg) > 1 and '@' in pmsg.split(' ')[0]:
        #         writer = csv.writer(f)
        #         data = [(pmsg.split()[0], pmsg.split(' ', 1)[1])]
        #         writer.writerows(data)
        #         # print pmsg
        #         # self.store.append(pmsg)
        # f.close()

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

    def pruner(self, msg):

        # get rid of the facial marks
        msg = re.sub('[^a-zA-Z0-9\-\#\@\,\!\.\~\?\"\ \'\$]+', '', msg)
        # get rid of https,rt, #'s hashtag
        msg = msg.lower()
        stopwords = ["https", "rt", "#"]
        #this is not correct bug
        # for stop in stopwords:
        #     buffer = ''
        #     for word in msg.split():
        #         if stop not in word:
        #             buffer = buffer + word + " "
        #     msg = buffer
        #     # print msg
        # return msg


if __name__ == "__main__":
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    #hashtag = "happy"
    #hashtag = ' '
    with open ("hashtag", 'r') as f:
        a = f.readline()
        words = a.split(" ")[1:]

    for word in words:
        hashtag = word
    # step2 creating a stream
    myStreamListener = MyStreamListener(api, hashtag)
    myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener(api, hashtag))
    # step3 starting a stream
    myStream.filter(track=[hashtag])