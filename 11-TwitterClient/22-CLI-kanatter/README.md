# 利用方法

1. 利用に必要なパッケージのインストール  
    以下のコマンドを実行。
    ```sh
    $ sudo yum install pip
    $ pip install requests  ←---------- Python で Rest API 操作を簡単に行うためのライブラリ
    $ pip install requests-oauthlib  ←- Python で OAuth 認証を簡単に行うためのライブラリ
    ```

2. 開発者用のトークンを取得  
    Twitter にログインした状態で、開発者用ページ（[https://developer.twitter.com/en/apps/](https://developer.twitter.com/en/apps/)）にアクセスする。  
    「登録したアプリ」にある [Details] ボタンを選択して画面を切り替える。  
    [Keys and tokens] ボタンをクリックして画面を切り替える。  
    表示されたキーとトークンをメモする
    - API key
    - API secret key
    - Access token
    - Access token secret

3. config.py ファイルを作成する。  
    以下の内容でファイルを作成する。
    ```python
    CONSUMER_KEY = "<API key>"
    CONSUMER_SECRET = "<API secret key>"
    ACCESS_TOKEN = "<Access token>"
    ACCESS_TOKEN_SECRET = "<Access token secret>"
    GEO_LAT = "34.995272"                          # 緯度、設定したくなければ "" でおｋ
    GEO_LONG = "135.895358"                        # 経度、設定したくなければ "" でおｋ
    ```

4. あとはコマンドを実行


# CLI の仕様
```sh
$ kanatter COMMAND <OPTION>
```
上記を実現する場合、subparser を使うと良いとのこと。


# ［メモ］ツイッターで開発者として登録する
[https://developer.twitter.com/en/apps/](https://developer.twitter.com/en/apps/) にアクセスして設定すればいい。  
英語で色々と目的やら何やらを入力する必要がある。  
今はこんなサイトも用意されてるみたい（便利でいいね）  
[https://www.itti.jp/web-direction/how-to-apply-for-twitter-api/](https://www.itti.jp/web-direction/how-to-apply-for-twitter-api/)








# 参考サイト
- [Twitter 開発者ドキュメント日本語訳](http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/GET-trends-closest.cgi)
- [twitter api を使ったwebアプリケーション作成に必要なこと](https://belltzel.dev/twitter-api-prepare-for-application-creation/)
- [rest api](https://syncer.jp/Web/API/Twitter/REST_API/GET/statuses/user_timeline/)
- [twitter api docs](https://developer.twitter.com/en/docs)
- [python スクリプトを単一実行ファイルにする方法](https://qiita.com/hirohiro77/items/466e411fa41f144c8b2a)
- [お気楽python /tkinter 入門](http://www.nct9.ne.jp/m_hiroi/light/pytk05.html)
- [python でぬるオブジェクトの比較](https://qiita.com/tortuepin/items/44fdb63cc82dfd260575)
- [とほほのpython 入門](http://www.tohoho-web.com/python/function.html)
- [python でファイル処理のGUIプログラムを作ってみた](https://qiita.com/chanmaru/items/8e5ebf7d8b0b21c8fd3a)
- [](https://qiita.com/bakira/items/00743d10ec42993f85eb)
- [Syncer](https://syncer.jp/Web/API/Twitter/REST_API/GET/statuses/user_timeline/)


https://qiita.com/oohira/items/308bbd33a77200a35a3d
https://qiita.com/moroku0519/items/315cd25d3eaae3217103

