from twython import Twython
from anytree import Node, RenderTree
import codecs
import sys
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

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
#hashtag = input("Enter the hashtag:");
#hashtag="".join(["#",query]);

hashtag = "#TriviaHeineken2018"
tweetsCountSearchLimit = 20
# Documentation: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
search = twitter.search(q=hashtag, count=tweetsCountSearchLimit, result_type='recent')
tweets = search['statuses']

# Search tweet by id
#id_of_tweet = 972831156767985664
#tweet = twitter.show_status(id=id_of_tweet)

# Remove the retweets
filteredTweets_withoutRT = []
for tweet in tweets:
    testString = tweet['text']
    if testString[0:2] != "RT":
        filteredTweets_withoutRT.append(tweet)
tweets = filteredTweets_withoutRT

print('(' + str(len(tweets)) + ') results for hashtag: ' + hashtag)

# TODO: Tree
tweetsNodes = []

# Documentation: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
for tweet in tweets:
    # Tweet ID
    print('Tweet id: ', tweet['id_str'])
    # Tweet text
    print('\ttweet:', tweet['text'])
    # Tweet creation datetime
    print('\tcreated at (UTC):', tweet['created_at'])
    # Original poster info [screen name & id]
    print('\toriginal poster:', '@' + tweet['user']['screen_name'] + ' (id: ' + tweet['user']['id_str'] + ')')
    # If it is a reply, show the original tweet id and OP screen name
    if tweet['in_reply_to_status_id_str'] is not None and tweet['in_reply_to_screen_name'] is not None:
        print('\tin reply to tweet', tweet['in_reply_to_status_id_str'], 'from',  '@' + tweet['in_reply_to_screen_name'])
    # Retweet count
    print('\tretweet count:', tweet['retweet_count'])
    # Favorite count
    print('\tfavorite count:', tweet['favorite_count'])
    # Related hastags
    tweetRelatedHashtags = []
    for hashtag in tweet['entities']['hashtags']:
        tweetRelatedHashtags.append('#' + hashtag['text'])
    print('\trelated hashtags: ' + ', '.join(tweetRelatedHashtags))
    print('')

    # Tree?
    # https://pypi.python.org/pypi/anytree
    # Documentation: http://anytree.readthedocs.io/en/latest/api.html
    #node = Node(tweet['id_str'])
    #tweetsNodes.append(tweet['id_str'])
    #if tweet['in_reply_to_status_id_str'] is not None:
    #    if tweet['in_reply_to_status_id_str'] in tweetsNodes:
