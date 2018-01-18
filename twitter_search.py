
import twitter
import json

consumer_key = 'V7NMDq4w2jqY3XfuhVMQIus6U'
consumer_secret = 'Fh91YD6XAui8Cv37bwDVJa1IwdFUAtavIUpzLHHLiz7OE1SY84'
oauth_token = '886811149156491265-MiLUyDvaI2tdsRjhk0s1X8bVTnChTSQ'
oauth_token_secret = 'KfuBI33I2pPxez2llydllT8qSZJPLBHbW485hNAYz3VOg'


auth = twitter.oauth.OAuth(oauth_token,oauth_token_secret,
    consumer_key,consumer_secret)

twitter_api = twitter.Twitter(auth=auth)


def twitter_search(twitter_api, q,lang, max_results=200, **kw):
    search_results = twitter_api.search.tweets(q=q, count=100, **kw)
    statuses = search_results['statuses']
    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.
    # Enforce a reasonable limit
    max_results = min(1000, max_results)
    for _ in range(10): # 10*100 = 1000 
        try:
            next_results = search_results['search_metadata']['next_results'] 
        except KeyError as e: # No more results when next_results doesn't exist
            break
# Create a dictionary from next_results, which has the following form: # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ]) 
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses'] 
        if len(statuses) > max_results:
            break 

    return statuses


q = "Amazon"
lang = "en"
results = twitter_search(twitter_api, q,lang, max_results=10) # Show one sample search result by slicing the list...
print(len(results))
print (json.dumps(results, indent=1))