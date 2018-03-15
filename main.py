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

#"to:$tweeterusername", sinceId = $tweetId


# Filter rewteeets OR replies
hashtag = "#TriviaHeineken2018  -filter:retweets -filter:replies"
test = "from:majogavilanesa #TriviaHeineken2018"
# Tweets search limit (Free limit is 100)
tweetsCountSearchLimit = 100
# Documentation: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
# Options:
#   result_type="mixed": Include both popular and real time results in the response.
#   result_type="recent": Return only the most recent results in the response
#   result_type="popular": Return only the most popular results in the response.
#   "top"
search = twitter.search(q=hashtag, count=tweetsCountSearchLimit, result_type="recent", exclude_replies=True)
tweets = search["statuses"]

# Search tweet by id
#id_of_tweet = 972831156767985664
#tweet = twitter.show_status(id=id_of_tweet)

print("(" + str(len(tweets)) + ") filtered results for hashtag: " + hashtag)

# TODO: Tree
rootNode = Node("root")

# Documentation: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
for tweet in tweets:

    tweetId = tweet["id_str"]
    parentTweetId = None
    if tweet["in_reply_to_status_id_str"] is not None:
        parentTweetId = tweet["in_reply_to_status_id_str"]

    # Tweet
    print("Tweet: ", "https://twitter.com/statuses/" + tweet["id_str"])
    # Tweet text
    print("\ttext:", tweet["text"])
    # Tweet creation datetime
    print("\tcreated at (UTC):", tweet["created_at"])
    # Original poster info [screen name & id]
    print("\toriginal poster:", "@" + tweet["user"]["screen_name"] + " (id: " + tweet["user"]["id_str"] + ")")
    # If it is a reply, show the original tweet id and OP screen name
    if tweet["in_reply_to_status_id_str"] is not None and tweet["in_reply_to_screen_name"] is not None:
        print("\tin reply to ", "@" + tweet["in_reply_to_screen_name"] + " (tweet:",
               "https://twitter.com/statuses/" + tweet["in_reply_to_status_id_str"] + ")")
    # Retweet count
    print("\tretweet count:", tweet["retweet_count"])
    # Favorite count
    print("\tfavorite count:", tweet["favorite_count"])
    # Related hastags
    tweetRelatedHashtags = []
    for hashtag in tweet["entities"]["hashtags"]:
        tweetRelatedHashtags.append("#" + hashtag["text"])
    print("\trelated hashtags: " + ", ".join(tweetRelatedHashtags))

    # Tree?
    # https://pypi.python.org/pypi/anytree
    # Documentation: http://anytree.readthedocs.io/en/latest/api.html

    # If the tweet IS a reply
    if tweet["in_reply_to_status_id_str"] is not None:
        print("Tweet IS a reply")
        parentOpScreenNameNode \
            = anytree.search.find(rootNode, lambda node: node.name == tweet["in_reply_to_screen_name"])
        # If the parent OP screen name IS NOT registered on the tree
        if parentOpScreenNameNode is None:
            print("Parent OP screen name is NOT registered on the tree")
            parentTweetId \
                = anytree.search.find(rootNode, lambda node: node.name == tweet["in_reply_to_status_id_str"])
            # If the parent tweet id IS registered on the tree
            if parentTweetId is not None:
                print("Parent tweet id IS registered on the tree")
                tweetIdNode = Node(tweet["id_str"], parent=parentTweetId)
            else:
                print("Parent tweet id IS NOT registered on the tree")
                parentTweetUserScreenNameNode = Node(tweet["in_reply_to_screen_name"], parent=rootNode)
                parentTweetId = Node(tweet["in_reply_to_status_id_str"], parent=parentTweetUserScreenNameNode)
                tweetIdNode = Node(tweet["id_str"], parent=parentTweetId)
        else:
            print("Parent OP screen name IS registered on the tree")
            parentTweetId \
                = anytree.search.find(rootNode, lambda node: node.name == tweet["in_reply_to_status_id_str"])
            # If the parent tweet id IS registered on the tree
            if parentTweetId is not None:
                print("Parent tweet id IS registered on the tree")
                tweetIdNode = Node(tweet["id_str"], parent=parentTweetId)
            else:
                print("Parent tweet id IS NOT registered on the tree")
                parentTweetId = Node(tweet["in_reply_to_status_id_str"], parent=parentTweetUserScreenNameNode)
                tweetIdNode = Node(tweet["id_str"], parent=parentTweetId)

    # If the tweet is NOT a reply
    else:
        print("Tweet is NOT a reply")
        parentOpScreenNameNode \
            = anytree.search.find(rootNode, lambda node: node.name == tweet["user"]["screen_name"])
        # If the OP screen name IS registered on the tree
        if parentOpScreenNameNode is not None:
            print("The OP screen name IS registered on the tree")
            tweetId \
                = anytree.search.find(rootNode, lambda node: node.name == tweet["id_str"])
            # If the tweet id IS NOT registered on the tree
            if tweetId is None:
                print("Tweet id IS NOT registered on the tree")
                tweetIdNode = Node(tweet["id_str"], parent=parentOpScreenNameNode)
            else:
                print("Tweet id IS registered on the tree")
        else:
            print("The OP screen name IS NOT registered on the tree")
            tweetOpScreenNameNode = Node(tweet["user"]["screen_name"], parent=rootNode)
            tweetIdNode = Node(tweet["id_str"], parent=tweetOpScreenNameNode)
    print("")
    print(RenderTree(rootNode, style=anytree.render.ContRoundStyle()))
    print("==========================================================")

print(twitter.get_home_timeline())
print(twitter.get_lastfunction_header('x-rate-limit-remaining'))
