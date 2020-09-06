# 参考URL

- [jq - Github](https://stedolan.github.io/jq/)
- [bashでJSONに変数を埋め込むための3つの方法 - Developers.IO](https://dev.classmethod.jp/articles/how-to-inject-variable-to-json-on-bash/)
- [jqコマンドの基本的な使い方と便利なおぷしょんまとめ - 瀬戸内の雲のように](https://www.setouchino.cloud/blogs/19)
- [jqコマンド(jsonデータの加工、整形)の使い方 - わくわくBank](https://www.wakuwakubank.com/posts/676-linux-jq/)
- [jqコマンドを使う日常のご紹介 - Qiita](https://qiita.com/takeshinoda@github/items/2dec7a72930ec1f658af)
- [jqコマンドでjsonデータを整形・絞り込み - Qiita](https://qiita.com/Nakau/items/272bfd00b7a83d162e3a)
- [シェルスクリプトでJSONを扱う - Qiita](https://qiita.com/unhurried/items/c62d29540de3e10a50ad)
- [JSON入門 - とほほのwww入門](http://www.tohoho-web.com/ex/json.html)




# 概要
REST API を用いた Web サービスを開発する場合、操作の実行結果等は基本的に Json 形式で返却されることになる。  
そうなった場合、シェルスクリプトによる ST テストを実施する際は Json を必要に応じて自由に操作できるようになっていなければ、テスト工程のコストが多くかかる。  
そのため、Json データを jq コマンドで自由に整形できるようになっておくスキルが必要になるため、学習することにした。


# 利用準備
以下のコマンドを実行して、パッケージをインストールしておく。

- fedora 系
    ```sh
    # yum install jq
    ```
- debian 系
    ```sh
    # apt install jq
    ```



# お試し


## 返却されるデータの例
Json 形式だと、以下のようなデータが返ってくる。  
今回のお勉強では以下のデータが返ってくるものとして、学習を進める


- 正常系
    ```json
    {
      "id": 1,
      "name": "kanamaru",
      "description": "test-description",
      "param": {
        "hobby1": "baseball",
        "hobby2": "camp"
      },
      "tags": [
        "test-user",
        "male"
      ]
    }
    ```

- 異常系（エラーが起きた場合）
    ```json
    {
      "Error": "Invalid parameters to context creation"
    }
    ```


## json データを作ってみる
JSON作成にはヒアドキュメントを使う

REST API を実装するのは非常に面倒なので、json を受け取った体でデータだけ作って、それに対して `jq` コマンドを使ってみる。  
早い話、通常 `JSON=$(curl <REST API>)` とするところを、REST API を叩くのではなく直接データを放り込む感じ。

```json
id=1
name="kanamaru"
description="test-description"
hobby1="baseball"
hobby2="camp"
json=$(cat << EOS
{
  "id": ${id},
  "name": "${name}",
  "description": "${description}",
  "param": {
    "hobby1": "${hobby1}",
    "hobby2": "${hobby2}"
  },
  "tags": [
    "test-user",
    "male"
  ]

}
EOS
)
```


実際、上記で作った変数 JSON を表示してみるとこんな感じになる。
```sh
kanamaru@study-ladap:~$ echo $json
{ "id": 1, "name": "kanamaru", "description": "test-description", "param": { "hobby1": "baseball", "hobby2": "camp" }, "tags": [ "test-user", "male" ] }
kanamaru@study-ladap:~$ echo $json | jq
{
  "id": 1,
  "name": "kanamaru",
  "description": "test-description",
  "param": {
    "hobby1": "baseball",
    "hobby2": "camp"
  },
  "tags": [
    "test-user",
    "male"
  ]
}
```

異常系（エラー）の場合の JSON はこんな感じ。
```json
msg="Invalid parameters to context creation"
json=$(cat << EOS
{
  "Error": "${msg}"
}
EOS
)
```



