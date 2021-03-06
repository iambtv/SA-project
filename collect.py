import tweepy 
import pandas as pd
import numpy as np
import jsonpickle, sys, re, collections, math, os

api_key = "nEHpCxgQjOLpfHXAAmlWzxwYF"
api_secret = "Sfa8e7tZPC4gDS2QYVQ3ykqMYHsC7gNhbaWtBTeXwMhbAbIAcO"

msg_filters_format = ["https", "&", "RT", "@", "#"]
msg_filters_out = ["#Ad"]

#trim unnecessary elements and split msg
#data preparation for training
def trim(msg, filter_format = msg_filters_format):	

    msg = re.sub("[^\w\@\#\$\%\&\.\/'\\ ]+", '', msg)
    words = []
    
    for word in msg.split():
        #check if word contain any one of the special format
        if all(word.find(format) != 0 for format in msg_filters_format):

            if word[0] == "'":
                word = word[1:]

            if word and word[-1] == "'":
                word = word[:-1]

            if word:
                word = re.sub("[.]+",' ',word)
                words +=  word.split()

    if len(words) <= 5:
        return

    tweet = " ".join(words)
    return tweet#,msg

def collect(search_query,max_tweets):
    
    query_limit = 100
    tweets = []
    max_id = -1
    since_id = None

    tweet_count = 0
    
    while tweet_count < max_tweets:
        try:
            if max_id <= 0:
                if not since_id:
                    new_tweets = api.search(q = search_query, count = query_limit, show_user = True)
                else:
                    new_tweets = api.search(q = search_query, count = query_limit, since_id = since_id, show_user = True)
            else:
                if not since_id:
                    new_tweets = api.search(q = search_query, count = query_limit, max_id = str(max_id-1), show_user = True)
                else:
                    new_tweets = api.search(q = search_query, count = query_limit, max_id = str(max_id-1),since_id = since_id, show_user = True)

            #print jsonpickle.encode(new_tweets[0]._json, unpicklable = False)

            if not new_tweets:
                print "no more"
                break

            for msg in new_tweets:
                if msg.lang != "en":
                    #print msg.text.encode("utf-8")
                    continue

                msg_text = msg.text.encode("utf-8")
                user_id = msg.user.id

                #filter out any message contain rubbish
                for filter_item in msg_filters_out:
                    if filter_item in msg_text:
                        msg_text = ""
                        break
                
                if not msg_text:
                    continue
                #modify tweet
                tweet = trim(msg_text)
                if tweet:
                    tweets.append({"user_id":str(user_id),"trimmed_tweet":tweet,"original_tweet":msg_text})

            tweet_count += len(new_tweets)
            max_id = new_tweets[-1].id

        except tweepy.TweepError as e:
            print "error existed" + str(e)
            break

    return tweets


USAGE = """
usage: collect <database size> <Hashtag>
       database size: the num of unique tweets collected from twitter
       Default: 2000 'Trump'
       Running sample: python collect.py 5000 NBA
        or: python collect.py
       """


if __name__ == '__main__':

    args = sys.argv[1:]
    
    if args == []:
        search_number = 2000
        hashtag = '#Trump'
    elif len(args) == 2:
        hashtag = "#" + re.sub('[^a-zA-Z0-9]+', '', args[1])
        search_number = int(args[0])
    else:
        sys.exit(USAGE)

    auth = tweepy.AppAuthHandler(api_key,api_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

    if not api:
        print "Can't Authenticate"
        sys.exit(-1)

    tweets = collect(hashtag,search_number)
    df = pd.DataFrame(tweets)
    df = df[['user_id','trimmed_tweet','original_tweet']]

    df.to_csv(hashtag + '.csv',sep=',',index = False)
