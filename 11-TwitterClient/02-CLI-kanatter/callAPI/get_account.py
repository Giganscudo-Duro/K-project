def verify_credentials(twitter, params):
    url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    res = twitter.get(url, params = params)
    return res
