def update(twitter, params):
    url = "https://api.twitter.com/1.1/statuses/update.json"
    res = twitter.post(url, params = params) #post送信
    return res


def destroy(twitter, params):
    # 自分で削除したいIDを含んだURLを作成しなければならないので注意。
    url = "https://api.twitter.com/1.1/statuses/destroy/"+params['id']+".json"
    res = twitter.post(url, params = params)
    return res





