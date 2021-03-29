import json
from requests_oauthlib import OAuth1Session
from callAPI import post_status
from callAPI import get_status
from callAPI import post_user
from callAPI import get_user


def user_timeline(twitter, args):
    params = {
        "user_id" : None,
        "screen_name" : args.username
    }
    res = get_user.show(twitter, params = params)
    userinfo = json.loads(res.text)
    params = {
        "user_id" : userinfo['id'],
        "count" : args.count
    }
    res = get_status.user_timeline(twitter, params = params)
    if res.status_code == 200:
        print("DEBUG: user_timeline Success.")
        timelines = json.loads(res.text)
        print('*******************************************')
        for line in timelines: #タイムラインリストをループ処理
            print(line['user']['name']+' -> '+line['created_at'])
            print("-----")
            print(line['id'])
            print(line['text'])
            print('*******************************************')
    else:
        print("DEBUG: user_timeline Failed. : %d"% res.status_code)


def home_timeline(twitter, args):
    params = {
        "count" : args.count
    }
    res = get_status.home_timeline(twitter, params = params)
    if res.status_code == 200:
        print("DEBUG: home_timeline Success.")
        timelines = json.loads(res.text) #レスポンスからタイムラインリストを取得
        print('*******************************************')
        for line in timelines: #タイムラインリストをループ処理
            print(line['user']['name']+' -> '+line['created_at'])
            print("-----")
            print(line['id'])
            print(line['text'])
            print('*******************************************')
    else:
        print("DEBUG: home_timeline Failed. : %d"% res.status_code)
