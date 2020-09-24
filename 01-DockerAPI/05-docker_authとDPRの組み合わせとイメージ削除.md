# 参考URL
 - [YAMLファイルでコメントを記述する - まだプログラマーですが何か？](http://dotnsf.blog.jp/archives/1074215802.html)
 - [proxy環境下でDocker Registryの構築 - Qiita](https://qiita.com/kanegoon/items/e250c0a328673b0fca82)
 - [第49回 Dockerプライベートレジストリにユーザー認証を付ける（準備編） - ITmedia](https://www.itmedia.co.jp/enterprise/articles/1710/02/news018.html)
 - [第50回　Dockerプライベートレジストリにユーザー認証を付ける（活用編） - ITmedia](https://www.itmedia.co.jp/enterprise/articles/1710/16/news016.html)
 - []()
 - []()
 - [Docker Registry の使い方 - GitHub](https://gist.github.com/takenoco82/b9559a1abd57eb0845a77041860cd26e)
 - [Dockerのプライベートレジストリからimageを削除する方法 - Qiita](https://qiita.com/Gin/items/c58c4485caae1c139e8f)
 - []()
 - []()
 - []()



# 環境構築手順



## 必要パッケージのインストール

以下のコマンドを実行。
```sh
# apt install openssl
# apt install apache2-utils
```
docker をインストールするため、以下のコマンドを実行。




## 証明書用ディレクトリ＆証明書ファイルの作成

証明書を格納するディレクトリを作成し、そこに証明書ファイルを作成＆格納する
```sh
# mkdir -p /home/auth_server/ssl
# openssl req \
    -x509 \
    -nodes \
    -days 365 \
    -newkey rsa:2048 \
    -keyout /home/auth_server/ssl/server.key \
    -out    /home/auth_server/ssl/server.pem
```

## 暗号化されたパスワードを生成


admin ユーザ用のパスワードを作成
```sh
# htpasswd -nbB admin admin-passwd | cut -d: -f2
--[実行結果]----------
$2y$05$qm6djieFVAgtipS5YHn14ewQqqvtay5TxzQWuUT5PuNbzPsqbcktq
```

user01 ユーザ用のパスワードを作成
```sh
# htpasswd -nbB user01 user01-passwd | cut -d: -f2
--[実行結果]----------
$2y$05$MJfq57DY1imzu1nIG1TzYu7re3hvunthNcjF.5M0r9lVRE6vzPLq.
```


user02 ユーザ用のパスワードを作成
```sh
# htpasswd -nbB user02 user02-passwd | cut -d: -f2
--[実行結果]----------
$2y$05$R/78VMwYW351w5nSxu5YJeuDsBVkre1UK.Wnhc03kfA645d70TaMa
```

## アクセス制御用の yaml ファイルを作成

以下のサイトにアクセスし、テンプレートを入手する。  
https://github.com/cesanta/docker_auth/blob/master/examples/simple.yml

アクセス制御用のファイルを作成するため、以下のコマンドを実行。
```yml
# mkdir -p /home/auth_server/config
# vim /home/auth_server/config/auth_config.yml
```

今回作成したファイルは以下の通り。

- `/home/auth_server/config/auth_config.yml`
    ```yml
    server:
            addr: ":5001"                   # ポート番号
            certificate: "/ssl/server.pem"  # 生成した証明書の相対パスを指定
            key: "/ssl/server.key"          # 生成した秘密鍵の相対パスを指定
    token:
            issuer: "Auth Service"
            expiration: 900
    users:
            "admin":        # Dockerプライベートレジストリにアクセスするユーザー「admin」
                password: "$2y$05$qm6djieFVAgtipS5YHn14ewQqqvtay5TxzQWuUT5PuNbzPsqbcktq"        # adminのパスワード
            "user01":       # Dockerプライベートレジストリにアクセスするユーザー「user01」
                password: "$2y$05$MJfq57DY1imzu1nIG1TzYu7re3hvunthNcjF.5M0r9lVRE6vzPLq."        # user01のパスワード
            "user02":       # Dockerプライベートレジストリにアクセスするユーザー「user02」
                password: "$2y$05$R/78VMwYW351w5nSxu5YJeuDsBVkre1UK.Wnhc03kfA645d70TaMa"        # user02のパスワード
    acl:
            - match: {account: "admin"}
              actions: ["*"]        # adminは、DPRを使ったdocker pullとdocker pushが可能
            - match: {account: "user01"}
              actions: ["pull"]     # user01は、DPRを使ったdocker pullは可能だがdocker pushはできない
            - match: {account: "user02"}
              actions: [""]         # user02は、DPRを使ったdocker pullもdocker pushもできない
    ```


## 認証用のコンテナを起動
以下のコマンドを実行。
```sh
# docker run \
    -d \
    -v /home/auth_server/config:/config:ro \
    -v /home/log/docker_auth:/logs \
    -v /home/auth_server/ssl:/ssl \
    -p 5001:5001 \
    --restart=always \
    --name docker_auth01 \
    cesanta/docker_auth /config/auth_config.yml
```


## DPR コンテナを起動
以下のコマンドを実行。
```sh
# mkdir -p /home/docker_registy/data
# docker run -d -p 5000:5000 \
    -e REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/var/lib/registry \
    -e REGISTRY_AUTH=token \
    -e REGISTRY_AUTH_TOKEN_REALM=https://localhost:5001/auth \
    -e REGISTRY_AUTH_TOKEN_SERVICE="Docker registry" \
    -e REGISTRY_AUTH_TOKEN_ISSUER="Auth Service" \
    -e REGISTRY_AUTH_TOKEN_ROOTCERTBUNDLE=/ssl/server.pem \
    -e REGISTRY_STORAGE_DELETE_ENABLED=true   \
    -v /home/auth_server/ssl:/ssl \
    -v /home/docker_registry/data:/var/lib/registry \
    --restart=always \
    --name registry01 registry:latest
```

ここまでで、ひとまず環境作成は完了。



## セキュアでないレジストリを使うための設定
暗号化されていない http 通信を用いて DPR とやり取りする場合、「insecure-registry」として登録しておかないと、利用することができない。  
今回作った環境は正にそれに該当するので、DPR にアクセスするクライアント側で、以下の処理を実施しておく。

1. `/etc/docker/daemon.json`を生成
    ```json
    { "insecure-registries":["localhost:5000"] }
    ```
2. 設定を反映して docker デーモンを再起動
    ```sh
    # systemctl daemon-reload
    # systemctl restart docker
    ```


これで環境構築は完了。





# 実際に使ってみる




## お試しでイメージを取得
以下のコマンドを実行
```sh
# docker pull centos:7
```


## 作成した DPR にログインしてイメージを push/pull を試す

### ユーザ「admin」でお試し


#### DPR にログイン
以下のコマンドを実行
```sh
# docker login localhost:5000
--[実行結果]----------
Username: admin
Password:
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```
ログインに成功した。


#### お試しイメージの準備
お試し push 用のイメージをつくるためタグ付けするため、以下のコマンドを実行
```sh
# docker tag centos:7 localhost:5000/admin-image:tag1
```
現時点ではこんな感じになってるはず。
```sh
# docker images
--[実行結果]----------
REPOSITORY                   TAG                 IMAGE ID            CREATED             SIZE
centos                       7                   7e6257c9f8d8        6 weeks ago         203MB
localhost:5000/admin-image   tag1                7e6257c9f8d8        6 weeks ago         203MB
registry                     latest              2d4f4b5309b1        3 months ago        26.2MB
cesanta/docker_auth          latest              9866a04a2227        6 months ago        17.3MB
```

#### お試ししメージのpush
以下のコマンドを実行
```sh
# docker push localhost:5000/admin-image:tag1
--[実行結果]----------
The push refers to repository [localhost:5000/admin-image]
613be09ab3c0: Pushed
tag1: digest: sha256:fe2347002c630d5d61bf2f28f21246ad1c21cc6fd343e70b4cf1e5102f8711a9 size: 529
```

#### ログアウト
以下のコマンドを実行。
```sh
# docker logout localhost:5000
--[実行結果]----------
Removing login credentials for localhost:5000
```

# API を叩いてイメージの削除を試みる

イメージの削除は docker コマンドでは実行できないので、基本的にイメージの削除は以下の流れになる

1. curl で、リポジトリ一覧を取得する
2. curl で、指定したリポジトリのタグ一覧を取得する
3. curl で、指定したイメージのダイジェストを取得する
4. curl で、イメージを削除する
5. registryコンテナ内でGC(Garbage collection)を起動させる


とりあえず順番に試してみる。

## リポジトリ一覧を取得する

以下のコマンドを実行。
```sh
# curl -v -s -k localhost:5000/v2/_catalog
--[実行結果]----------
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> GET /v2/_catalog HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
>
< HTTP/1.1 401 Unauthorized
< Content-Type: application/json; charset=utf-8
< Docker-Distribution-Api-Version: registry/2.0
< Www-Authenticate: Bearer realm="https://localhost:5001/auth",service="Docker registry",scope="registry:catalog:*"
< X-Content-Type-Options: nosniff
< Date: Thu, 24 Sep 2020 22:18:47 GMT
< Content-Length: 145
<
{"errors":[{"code":"UNAUTHORIZED","message":"authentication required","detail":[{"Type":"registry","Class":"","Name":"catalog","Action":"*"}]}]}
* Connection #0 to host localhost left intact
```

認証コンテナを起動してるので、エラーが返ってきた。  
仕方ないので、エラーメッセージに従い、トークンを取得する

```sh
USERNAME="admin"
PASSWORD="admin-passwd"
HOST="localhost:5001"
curl -s -k \
    -u ${USERNAME}:${PASSWORD} \
    -d "service=Docker registry"  \
    -d "scope=registry:catalog:*"  \
    -d "account=${USERNAME}"  \
    https://${HOST}/auth | jq
--[実行結果]----------
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkdOM0I6STVOTDpTV0dXOk1YQzQ6T1NRSzpWQkJPOkRWQVA6WUpNVDpEV1o2OkJSSzM6VjU3UzpBS1pEIn0.eyJpc3MiOiJBdXRoIFNlcnZpY2UiLCJzdWIiOiJhZG1pbiIsImF1ZCI6IkRvY2tlciByZWdpc3RyeSIsImV4cCI6MTYwMDk4ODczNiwibmJmIjoxNjAwOTg3ODI2LCJpYXQiOjE2MDA5ODc4MzYsImp0aSI6IjMyMTMwOTA1NTcyMTE2NTg5OTkiLCJhY2Nlc3MiOlt7InR5cGUiOiJyZWdpc3RyeSIsIm5hbWUiOiJjYXRhbG9nIiwiYWN0aW9ucyI6WyIqIl19XX0.C796_jZKys0DF3CJvxhxJtEiDOHtFR5UC1yS6FTe89XWx5202lnQecF6vv11iiPmfc4OgzJZdwIA6Xmn31iSigrmHBXKhdJ8cHA5aZ2w9GA-It6r7KDwk7mBBAWL50disOTXq08tFCyYGqs6y9vxMZGC5Weud4qkGnuV0-r9Gp5Oawrq8IYOKZur_36uY75NxOiJv-_g7H5TG1BwubvvT0YNdgGnqAtNTeN996qSJFqWnqV7V_T2SImqD6w_0sxnrqoBE8vwzT0GIlGsZpzecwws5iPG8uccilwBA6AlC1O62dsZPniIaEChcu5RfVlpT7c-_j5lxjCE-hVHKutRFw",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkdOM0I6STVOTDpTV0dXOk1YQzQ6T1NRSzpWQkJPOkRWQVA6WUpNVDpEV1o2OkJSSzM6VjU3UzpBS1pEIn0.eyJpc3MiOiJBdXRoIFNlcnZpY2UiLCJzdWIiOiJhZG1pbiIsImF1ZCI6IkRvY2tlciByZWdpc3RyeSIsImV4cCI6MTYwMDk4ODczNiwibmJmIjoxNjAwOTg3ODI2LCJpYXQiOjE2MDA5ODc4MzYsImp0aSI6IjMyMTMwOTA1NTcyMTE2NTg5OTkiLCJhY2Nlc3MiOlt7InR5cGUiOiJyZWdpc3RyeSIsIm5hbWUiOiJjYXRhbG9nIiwiYWN0aW9ucyI6WyIqIl19XX0.C796_jZKys0DF3CJvxhxJtEiDOHtFR5UC1yS6FTe89XWx5202lnQecF6vv11iiPmfc4OgzJZdwIA6Xmn31iSigrmHBXKhdJ8cHA5aZ2w9GA-It6r7KDwk7mBBAWL50disOTXq08tFCyYGqs6y9vxMZGC5Weud4qkGnuV0-r9Gp5Oawrq8IYOKZur_36uY75NxOiJv-_g7H5TG1BwubvvT0YNdgGnqAtNTeN996qSJFqWnqV7V_T2SImqD6w_0sxnrqoBE8vwzT0GIlGsZpzecwws5iPG8uccilwBA6AlC1O62dsZPniIaEChcu5RfVlpT7c-_j5lxjCE-hVHKutRFw"
}
```

必要なのは token だけなので、変数にでもコピーしておく。

```sh
USERNAME="admin"
PASSWORD="admin-passwd"
HOST="localhost"
TOKEN=`curl -s -k \
  -u ${USERNAME}:${PASSWORD} \
  -d "service=Docker registry"  \
  -d "scope=registry:catalog:*"  \
  -d "account=${USERNAME}"  \
  https://${HOST}:5001/auth | jq '.token' -r `
curl -s -k -H "Authorization: Bearer ${TOKEN}" http://${HOST}:5000/v2/_catalog | jq
--[実行結果]----------
{
  "repositories": [
    "admin-image",
    "kana",
    "ubuntu"
  ]
}
```
これで、イメージリストは取得できた。
(kana と ubuntu はお遊びで登録してしまったイメージ)


## 指定したリポジトリのタグ一覧を取得
以下のコマンドを実行。

```sh
# curl -v -s -k localhost:5000/v2/admin-image/tags/list
--[実行結果]----------
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> GET /v2/admin-image/tags/list HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
>
< HTTP/1.1 401 Unauthorized
< Content-Type: application/json; charset=utf-8
< Docker-Distribution-Api-Version: registry/2.0
< Www-Authenticate: Bearer realm="https://localhost:5001/auth",service="Docker registry",scope="repository:admin-image:pull"
< X-Content-Type-Options: nosniff
< Date: Thu, 24 Sep 2020 22:55:23 GMT
< Content-Length: 154
<
{"errors":[{"code":"UNAUTHORIZED","message":"authentication required","detail":[{"Type":"repository","Class":"","Name":"admin-image","Action":"pull"}]}]}
* Connection #0 to host localhost left intact
```



面倒だけど、再びトークンを取得
```sh
$ curl -s -k \
    -u admin:admin-passwd \
    -d "service=Docker registry"  \
    -d "scope=repository:admin-image:pull"  \
    -d "account=admin"  \
    https://${HOST}/auth | jq
```

スクリプト化
```sh
USERNAME="admin"
PASSWORD="admin-passwd"
HOST="localhost"
API="v2/admin-image/tags/list"
IMAGE="admin-image"
SCOPE="repository:${IMAGE}:pull"
TOKEN=`curl -s -k \
  -u ${USERNAME}:${PASSWORD} \
  -d "service=Docker registry"  \
  -d "scope=${SCOPE}"  \
  -d "account=${USERNAME}"  \
  https://${HOST}:5001/auth | jq '.token' -r `
curl -s -k -H "Authorization: Bearer ${TOKEN}" http://${HOST}:5000/${API} | jq
--[実行結果]----------
{
  "name": "admin-image",
  "tags": [
    "tag1"
  ]
}
```


## 指定したイメージのダイジェストを取得

```sh
curl -X GET -H "Accept: application/vnd.docker.distribution.manifest.v2+json" -s -D - http://localhost:5000/v2/admin-image/manifests/tag1
--[実行結果]----------
HTTP/1.1 401 Unauthorized
Content-Type: application/json; charset=utf-8
Docker-Distribution-Api-Version: registry/2.0
Www-Authenticate: Bearer realm="https://localhost:5001/auth",service="Docker registry",scope="repository:admin-image:pull"
X-Content-Type-Options: nosniff
Date: Thu, 24 Sep 2020 23:03:35 GMT
Content-Length: 154

{"errors":[{"code":"UNAUTHORIZED","message":"authentication required","detail":[{"Type":"repository","Class":"","Name":"admin-image","Action":"pull"}]}]}
```

面倒だけど、再びトークンを取得
```sh
$ curl -s -k \
    -u admin:admin-passwd \
    -d "service=Docker registry"  \
    -d "scope=repository:admin-image:pull"  \
    -d "account=admin"  \
    https://localhost:5001/auth | jq
```

スクリプト化
```sh
USERNAME="admin"
PASSWORD="admin-passwd"
HOST="localhost"
IMAGE="admin-image"
TAG="tag1"
SCOPE="repository:${IMAGE}:pull"
API="v2/${IMAGE}/manifests/${TAG}"
TOKEN=`curl -s -k \
  -u ${USERNAME}:${PASSWORD} \
  -d "service=Docker registry"  \
  -d "scope=${SCOPE}"  \
  -d "account=${USERNAME}"  \
  https://${HOST}:5001/auth | jq '.token' -r `
curl -v -H "Authorization: Bearer ${TOKEN}" -H "Accept: application/vnd.docker.distribution.manifest.v2+json" http://${HOST}:5000/${API}
--[実行結果]----------
> Accept: application/vnd.docker.distribution.manifest.v2+json
>
< HTTP/1.1 200 OK
< Content-Length: 529
< Content-Type: application/vnd.docker.distribution.manifest.v2+json
< Docker-Content-Digest: sha256:fe2347002c630d5d61bf2f28f21246ad1c21cc6fd343e70b4cf1e5102f8711a9
< Docker-Distribution-Api-Version: registry/2.0
< Etag: "sha256:fe2347002c630d5d61bf2f28f21246ad1c21cc6fd343e70b4cf1e5102f8711a9"
< X-Content-Type-Options: nosniff
< Date: Thu, 24 Sep 2020 23:10:19 GMT
<
{
   "schemaVersion": 2,
   "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
   "config": {
      "mediaType": "application/vnd.docker.container.image.v1+json",
      "size": 2794,
      "digest": "sha256:7e6257c9f8d8d4cdff5e155f196d67150b871bbe8c02761026f803a704acb3e9"
   },
   "layers": [
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 75863188,
         "digest": "sha256:75f829a71a1c5277a7abf55495ac8d16759691d980bf1d931795e5eb68a294c0"
      }
   ]
* Connection #0 to host localhost left intact
}
```
必要なのは、「Docker-Content-Digest」の項目だけ。


## イメージを削除する
先程指定した「Docker-Content-Digest」を指定して、削除を試みる。
```sh
curl -v -X DELETE http://localhost:5000/v2/admin-image/manifests/sha256:fe2347002c630d5d61bf2f28f21246ad1c21cc6fd343e70b4cf1e5102f8711a9
--[実行結果]----------
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 5000 (#0)
> DELETE /v2/admin-image/manifests/sha256:fe2347002c630d5d61bf2f28f21246ad1c21cc6fd343e70b4cf1e5102f8711a9 HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.58.0
> Accept: */*
>
< HTTP/1.1 401 Unauthorized
< Content-Type: application/json; charset=utf-8
< Docker-Distribution-Api-Version: registry/2.0
< Www-Authenticate: Bearer realm="https://localhost:5001/auth",service="Docker registry",scope="repository:admin-image:delete"
< X-Content-Type-Options: nosniff
< Date: Thu, 24 Sep 2020 23:11:23 GMT
< Content-Length: 156
<
{"errors":[{"code":"UNAUTHORIZED","message":"authentication required","detail":[{"Type":"repository","Class":"","Name":"admin-image","Action":"delete"}]}]}
* Connection #0 to host localhost left intact
```

面倒だけど、再びトークンを取得
```sh
$ curl -s -k \
    -u admin:admin-passwd \
    -d "service=Docker registry"  \
    -d "scope=repository:admin-image:delete"  \
    -d "account=admin"  \
    https://localhost:5001/auth | jq
```

スクリプト化
```sh
USERNAME="admin"
PASSWORD="admin-passwd"
HOST="localhost"
IMAGE="admin-image"
TAG="tag1"
DIGEST="sha256:fe2347002c630d5d61bf2f28f21246ad1c21cc6fd343e70b4cf1e5102f8711a9"
SCOPE="repository:${IMAGE}:delete"
API="v2/${IMAGE}/manifests/${DIGEST}"
TOKEN=`curl -s -k \
  -u ${USERNAME}:${PASSWORD} \
  -d "service=Docker registry"  \
  -d "scope=${SCOPE}"  \
  -d "account=${USERNAME}"  \
  https://${HOST}:5001/auth | jq '.token' -r `
curl -X DELETE -H "Authorization: Bearer ${TOKEN}" http://${HOST}:5000/${API}
--[実行結果]----------
```
必要なのは、「Docker-Content-Digest」の項目だけ。













