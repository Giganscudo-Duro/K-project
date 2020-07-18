def show(twitter, params):
    url = "https://api.twitter.com/1.1/statuses/show.json"
    res = twitter.get(url, params = params)
    return res


def home_timeline(twitter, params):
    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    res = twitter.get(url, params = params)
    return res


def user_timeline(twitter, params):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    res = twitter.get(url, params = params)
    return res
