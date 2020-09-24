# 参考URL




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





















