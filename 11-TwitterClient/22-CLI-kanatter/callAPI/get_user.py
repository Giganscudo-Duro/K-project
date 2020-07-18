
def show(twitter, params):
    url = "https://api.twitter.com/1.1/users/show.json"
    res = twitter.get(url, params = params)
    return res




def timeline(twitter, params):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    res = twitter.get(url, params = params)
    return res
