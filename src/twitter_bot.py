import json
import tweepy
from random import choice

class TwitterBot:

    def __init__(self, name):
        botfile = open('../data/' + name, 'rb')
        self.data = json.load(botfile)
        botfile.close()
        quote_file = open('../data/quotes.json','rb')
        self.quotes_data = json.load(quote_file)
        quote_file.close()
        self.quotes = self.quotes_data['quotes']
        auth = tweepy.OAuthHandler(self.data['consumer_key'], self.data['consumer_secret'])
        auth.set_access_token(self.data['access_token'], self.data['access_token_secret'])
        self.api = tweepy.API(auth)
        self.retweet_keywords = self.data['retweet_keywords']

    def tweet_random_quote(self):
        trimmed_quote = self.random_quote()[:140]
        quote = trimmed_quote.encode('ascii', 'replace')
        print('quote to post: ', quote)
        result = self.api.update_status(quote)
        return result

    def random_quote(self):
        return choice(self.quotes)

    def retweet_keyword_home_timeline(self):
        statuses = self.api.home_timeline()
        for s in statuses:
            for keyword in self.retweet_keywords:
                if keyword in s.text.lower():
                    print('Keyword found: ',keyword)
                    print('Status:',s.text)
                    print('id=',s.id)
                    resp = self.api.retweet(int(s.id))
                    print('Resp retweet=',resp.text)


        return None
