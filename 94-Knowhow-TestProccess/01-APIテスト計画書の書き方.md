# 参考URL

- [［API］ API仕様書の書き方 - Qiita](https://qiita.com/sunstripe2011/items/9230396febfab2eae2c2)
- [API Firstで仕様をテストする - Qiita](https://qiita.com/shunjikonishi/items/87391a9a5262f4ec6dca)
- [Rest APIで使われるHTTPメソッドとURL設計 - Qiita](https://qiita.com/sfp_waterwalker/items/765abc2b53cc11d5e367)


# どんな感じに書くか

とりあえず、こんな感じに書けば良いのかもしれない。  
多分は正解は無い。



# APIテスト仕様一覧

## POST /login

- API 概要
    | 項目          | 概要                                          |
    |---------------|-----------------------------------------------|
    | 機能概要      | サービスにログインする（トークンを取得する）  |
    | アクセスURI   | /login                                        |
    | HTTPメソッド  | POST                                          |

- 実行例
    ここは適当。
    ```sh
    $ curl -i -X POST -H "Accept: application/json" \
        -d '{ "username": "kanamaru", "password": "testpassword" }' \
        https://localhost/login
    ```



- 提供データ（JSON）
    | 項目      | 型     | サイズ | 必須 | 概要                        | 制限    |
    |-----------|--------|--------|----- |-----------------------------|---------|
    | user      | 文字列 |        |      | ログインするユーザ名        |         |
    | password  | 文字列 |        |      | 上記に紐付いたパスワード    |         |



- 返却データ（JSON）
    - 成功時
        | 項目      | 型     | サイズ | 必須 | 概要                        | 制限    |
        |-----------|--------|--------|----- |-----------------------------|---------|
        | user      | 文字列 |        |      | ログインするユーザ名        |         |
        | password  | 文字列 |        |      | 上記に紐付いたパスワード    |         |
    - 失敗時
        | 項目      | 型     | 概要              |
        |-----------|--------|-------------------|
        | Error     | 文字列 | エラー内容        |






