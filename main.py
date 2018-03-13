from nltk import word_tokenize
from twython import Twython
import codecs;
import sys;
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer);

# Twitter API tokens
KEY = "Your Key Here"
KEY_SECRET = "Your Key Here" 
ACCESS_TOKEN = "Your Key Here"
ACCESS_TOKEN_SECRET = "Your Key Here"

# Twython object
twitter = Twython(app_key=KEY,
            app_secret=KEY_SECRET,
            oauth_token=ACCESS_TOKEN,
            oauth_token_secret=ACCESS_TOKEN_SECRET)

# input hashtag
hashtag = input("Enter the hashtag:");
hashtag="".join(["#",query]);

#hashtag = "#TriviaHeineken2018"
tweetsCountSearchLimit = 30
# Documentation: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
search = twitter.search(q=hashtag, count=tweetsCountSearchLimit, result_type='recent')
tweets = search['statuses']

# Remove the retweets
filteredTweets_withoutRT = []
for tweet in tweets:
    testString = tweet['text']
    if testString[0:2] != "RT":
        filteredTweets_withoutRT.append(tweet)
tweets = filteredTweets_withoutRT

print('Results for hashtag: ' + hashtag)
# Documentation: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
for tweet in tweets:
    #tokens = word_tokenize(tweet['text'])
    #print(tokens)

    # Tweet ID
    print('Tweet id: ', tweet['id_str'])
    # Tweet text
    print('\ttweet:', tweet['text'])
    # Original poster info [screen name & id]
    print('\toriginal poster:', '@' + tweet['user']['screen_name'] + '(id: ' + tweet['user']['id_str'] + ')')
    # If it is a reply, show the OP screen name & id
    if tweet['in_reply_to_screen_name'] is not None:
        print('\tin reply to', '@' + tweet['in_reply_to_screen_name'] + '(id: ' + tweet['in_reply_to_user_id_str'] + ')')
    # Tweet creation datetime
    print('\tcreated at (UTC):', tweet['created_at'])
    # Retweet count
    print('\tretweet count:', tweet['retweet_count'])
    # Favorite count
    print('\tfavorite count:', tweet['favorite_count'])
    print('')
