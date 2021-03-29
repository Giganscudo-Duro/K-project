import json
from requests_oauthlib import OAuth1Session
from callAPI import post_status
from callAPI import get_status
from callAPI import post_user
from callAPI import get_user

def postTweet(twitter, args):
    if args.replyid is None :
        params = {
            "status" : args.messages,
            "in_reply_to_status_id" : args.replyid,
            "lat" : args.lat,
            "long" : args.long,
            "possibly_sensitive" : args.sensitive,
            "media_ids" : args.mediaids
            }
    else :
        params = {
            "id" : args.replyid
        }
        res = get_status.show(twitter, params = params)
        tweetinfo = json.loads(res.text)
        params = {
            "status" : "@"+tweetinfo['user']['screen_name']+" "+args.messages,
            "in_reply_to_status_id" : args.replyid,
            "lat" : args.lat,
            "long" : args.long,
            "possibly_sensitive" : args.sensitive,
            "media_ids" : args.mediaids
        }
    res = post_status.update(twitter, params = params) #post送信
    if res.status_code == 200:  #正常投稿出来た場合
        print("DEBUG: Post Success.")
    else:                       #正常投稿出来なかった場合
        print("DEBUG: Post Failed. : %d"% res.status_code)
