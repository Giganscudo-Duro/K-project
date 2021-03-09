import json    #標準のjsonモジュールの読み込み
import config
import argparse
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み
from subcommand import post
from subcommand import timeline
from subcommand import delete


# サブコマンドの実際の処理を記述するコールバック関数
def command_post(twitter, args):
    post.postTweet(twitter, args)

def command_hometimeline(twitter, args):
    timeline.home_timeline(twitter, args)

def command_usertimeline(twitter, args):
    timeline.user_timeline(twitter, args)

def command_delete(twitter, args):
    delete.delete(twitter, args)

def command_help(args):
    print(parser.parse_args([args.command, "--help"]))


# コマンドラインパーサーを作成
parser = argparse.ArgumentParser(description="Kanatter!!!!")
subparsers = parser.add_subparsers()


# post コマンドの parser を作成
parser_add = subparsers.add_parser("post", help="see `post -h`")
parser_add.add_argument("messages", type=str, help="messages of tweet")
parser_add.add_argument("--replyid", default=None, help="ID of tweetID")
parser_add.add_argument("--lat", default=config.GEO_LAT, help="param of lat")
parser_add.add_argument("--long", default=config.GEO_LONG, help="param of long")
parser_add.add_argument("--sensitive", default="false", help="bool of sensitive")
parser_add.add_argument("--mediaids", default=None, help="id of media")
parser_add.set_defaults(handler=command_post)

# hometimeline コマンドの parser を作成
parser_add = subparsers.add_parser("hometimeline", help="see `hometimeline -h`")
parser_add.add_argument("--count", default="10", help="num of tweet")
parser_add.set_defaults(handler=command_hometimeline)

# usertimeline コマンドの parser を作成
parser_add = subparsers.add_parser("usertimeline", help="see `usertimeline -h`")
parser_add.add_argument("username", type=str, help="user name")
parser_add.add_argument("--count", default="20", help="num of tweet(1~200)")
parser_add.set_defaults(handler=command_usertimeline)

# delete コマンドの parser を作成
parser_add = subparsers.add_parser("delete", help="see `delete -h`")
parser_add.add_argument("--id", type=str, help="Trget tweetID")
parser_add.add_argument("--all", action='store_true', help="flag of AllDelete")
parser_add.set_defaults(handler=command_delete)

# help コマンドの parser を作成
parser_help = subparsers.add_parser("help", help="see `help -h`")
parser_help.add_argument("command", help="command name which help is shown")
parser_help.set_defaults(handler=command_help)


args = parser.parse_args()

if __name__ == "__main__":

    if hasattr(args, "handler"):
        # コマンドライン引数をパースして対応するハンドラ関数を実行
        CK = config.CONSUMER_KEY
        CS = config.CONSUMER_SECRET
        AT = config.ACCESS_TOKEN
        ATS = config.ACCESS_TOKEN_SECRET
        twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理
        args.handler(twitter, args)
    else:
        # 未知のサブコマンドの場合はヘルプを表示
        parser.print_help()


