import json
from requests_oauthlib import OAuth1Session

from callAPI import post_status
from callAPI import get_status
from callAPI import post_user
from callAPI import get_user
from callAPI import get_account

def delete(twitter, args):
    if args.all :
        # 全部削除する場合
        params = {
            "include_entities" : "false",
            "skip_status" : "true",
            "include_email" : "true"
        }
        res = get_account.verify_credentials(twitter, params = params)
        userinfo = json.loads(res.text)
        params = {
            "user_id" : userinfo['screen_name']
        }
        res = get_status.user_timeline(twitter, params = params)
        if res.status_code == 200:
            timelines = json.loads(res.text)
            for line in timelines: #タイムラインリストをループ処理
                params = {
                    "id" : line['id_str']
                }
                res = post_status.destroy(twitter, params = params)
        else:
            print("DEBUG: Failed. : %d"% res.status_code)
    else :
        params = {
            "id" : args.id
        }
        res = post_status.destroy(twitter, params = params)
    if res.status_code == 200:
        print("DEBUG: Delete Success.")
    else:
        print("DEBUG: Delete Failed. : %d"% res.status_code)
