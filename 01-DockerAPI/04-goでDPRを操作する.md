# 参考 URL

## Docker Private Registry 系
- [第46回 Dockerのプライベートレジストリを活用する（準備編） - ITmedia エンタープライズ](https://www.itmedia.co.jp/enterprise/articles/1708/10/news052.html)
-[第48回 Dockerプライベートレジストリにユーザー認証を付けるには（概要編） - ITmedia エンタープライズ](https://www.itmedia.co.jp/enterprise/articles/1709/25/news017.html)
-[第49回 Dockerプライベートレジストリにユーザー認証を付ける（準備編） - ITmedia エンタープライズ](https://www.itmedia.co.jp/enterprise/articles/1710/02/news018.html)
- [Registry 設定リファレンス - Dpcker-docs-ja](http://docs.docker.jp/v1.12/registry/configuration.html)
- [ cesanta / docker_auth - GitHub](https://github.com/cesanta/docker_auth/tree/master/examples)

## API 叩く go のライブラリ系
- [Examples using the Docker Engine SDKs and Docker API - Dpcker-docs](https://docs.docker.com/engine/api/sdk/examples/)
- [github.com/docker/docker/client - GoDoc](https://godoc.org/github.com/docker/docker/client)
- [リモート API クライアント・ライブラリ - Docker-docs-ja](http://docs.docker.jp/engine/reference/remote_api_client_libraries.html)

## 基本形
- [nginxでBasic認証を設定する - DIGITAL COFFEE－デジタルコーヒー](https://plugout.hatenablog.com/entry/2017/01/15/131656)
- [YAML ファイルでコメントを記述する - まだプログラマーですが何か？](http://dotnsf.blog.jp/archives/1074215802.html)


# 普通の Docker Private Registry 

## 普通の DockerPrivateRegistry を作ってみる

とりあえず、登録されたイメージを保管するディレクトリを作成。
```sh
# mkdir -p /home/docker_regisrty/data
```

そんで必要なコンテナイメージを取得
```sh
# docker pull registry
```

最後にコンテナとして DPR を起動
```sh
# docker run -d \
-p 5000:5000 \
-e REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/var/lib/registry \
-v /home/docker_registry/data:/var/lib/registry \
--restart=always \
--name registry01 registry:latest
```

以上。


## 普通の DockerPrivateRegistry にイメージを登録してみる

まずは登録するため、適当なイメージを作成する
```sh
# docker pull ubuntu:18.04
```

次に、入手したイメージにオリジナルのタグを付ける
このタグを元に登録するレジストリが決まるので、さっき作ったやつをちゃんと指定すること
```sh
# docker tag ubuntu:18.04 localhost:5000/ubuntu:Kana-1
```

登録するとこんな感じになる。
```sh
# docker images
--[実行結果]------------------------------
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
ubuntu                  18.04               4e5021d210f6        15 hours ago        64.2MB
localhost:5000/ubuntu   Kana-1              4e5021d210f6        15 hours ago        64.2MB
registry                latest              708bc6af7e5e        8 weeks ago         25.8MB
```

念の為、まだイメージが登録されていないことを、確認してみる
```sh
# ll /home/docker_registry/data/
--[実行結果]------------------------------
合計 8
drwxr-xr-x 2 root root 4096  3月 21 18:54 ./
drwxr-xr-x 3 root root 4096  3月 21 18:54 ../
```

確認できたので、 push してみる
```sh
# docker push localhost:5000/ubuntu:Kana-1
```

ちゃんとイメージが登録されたか観てみる。
```sh
# tree -L 7 /home/docker_registry/
--[実行結果]------------------------------
/home/docker_registry/
`-- data
    `-- docker
        `-- registry
            `-- v2
                |-- blobs
                |   `-- sha256
                |       |-- 4e
                |       |-- 5b
                |       |-- 78
                |       |-- 93
                |       |-- e5
                |       `-- f1
                `-- repositories
                    `-- ubuntu
                        |-- _layers
                        |-- _manifests
                        `-- _uploads
17 directories, 0 files
```

登録できたっぽいので、コレで完了




# docker_auth と組み合わせた DockerPrivateRegistry

今回は LDAP と連動するなんてことはせず、単純に Basic 認証を用いた認証を用意する。


## 環境の構築

まずは openssl コマンドで、秘密鍵と、証明書を作成する。
以下のコマンドを実行。
```sh
# mkdir -p /hostdir/auth_server/ssl
# openssl req \
  -x509 \
  -nodes \
  -days 365 \
  -newkey rsa:2048 \
  -keyout /hostdir/auth_server/ssl/server.key \
  -out    /hostdir/auth_server/ssl/server.pem
```
質問事項については基本的に無視して、全部何入力せずに Enter。
```sh
# ls -1 /hostdir/auth_server/ssl/
server.key
server.pem
```
上記のようにファイルが2つ作成されたらOK。


DPR にアクセスするユーザ用のパスワードを作成する。
いちおう `htpasswd` コマンドを使って暗号化されたパスワードとして生成する。
まず、以下のコマンドを実行して、必要なパッケージをインストール。
```sh
# apt install apache2-utils
```
次に、admin ユーザ用のパスワードと、一般ユーザ二人（user01、user02）用のパスワードを生成。
- admin
    ```sh
    # htpasswd -nbB admin password | cut -d: -f2
    $2y$05$WZPNziWEEKWHPZP9b1pJM.4DYbouItTZ9HfbuDXjcBgrEMxkM8SkG
    ```
- user01
    ```sh
    # htpasswd -nbB user01 password01 | cut -d: -f2
    $2y$05$p.FC38D6ar1T.p0BN4/y1OB5mCQs7tyM3y9WKs/zBxc/csT0sNdCy
    ```
- user02
    ```sh
    # htpasswd -nbB user02 password02 | cut -d: -f2
    $2y$05$hNuM0B5EVzRjm0WGW52ETOYnXDMRrurNQPiePWQA02po7NUOiKUsq
    ```
上記のように、出力結果をメモしたらOK。

次は、アクセス制御用の設定ファイル「auth_config/yml」を作成する。
設定ファイルには、以下の項目を記述する。
- 作成した秘密鍵
- 証明書
- 暗号化したユーザのパスワード
- 各ユーザの実行権限

とりあえず作成したファイルが以下。
- /hostdir/auth_server/config/auth_config.yml
    ```yml
    server:
            addr: ":5001"  # -------------------- ポート番号
            certificate: "/ssl/server.pem"  # --- 生成した証明書の相対パスを指定
            key: "/ssl/server.key"  # ----------- 生成した秘密鍵の相対パスを指定
    token:
            issuer: "Auth Service"
            expiration: 900
    users:
            "admin":  # ---- ユーザー「admin」 を定義。パスワードも一緒に定義。
                    password: "$2y$05$WZPNziWEEKWHPZP9b1pJM.4DYbouItTZ9HfbuDXjcBgrEMxkM8SkG"
            "user01":  # ---- ユーザー「user01」 を定義。パスワードも一緒に定義。
                    password: "$2y$05$p.FC38D6ar1T.p0BN4/y1OB5mCQs7tyM3y9WKs/zBxc/csT0sNdCy"
            "user02":  # ---- ユーザー「user02」 を定義。パスワードも一緒に定義。
                    password: "$2y$05$hNuM0B5EVzRjm0WGW52ETOYnXDMRrurNQPiePWQA02po7NUOiKUsq"
    acl:
            - match: {account: "admin"}
              actions: ["*"]  # ----------- admin は、DPRを使ったdocker pullとdocker pushが可能
            - match: {account: "user01"}
              actions: ["pull"]  # -------- user01 は、DPRを使ったdocker pullは可能だがdocker pushはできない
            - match: {account: "user02"}
              actions: [""]  # ------------ user02 は、DPRを使ったdocker pullもdocker pushもできない
    ```

これでひとまず、必要なものは全部揃ったので、認証用のコンテナを立ち上げる。  
以下のコマンドを実行。
```sh
# docker run \
-d \
-v /hostdir/auth_server/config:/config:ro \
-v /hostdir/log/docker_auth:/logs \
-v /hostdir/auth_server/ssl:/ssl \
-p 5001:5001 \
--restart=always \
--name docker_auth01 \
cesanta/docker_auth /config/auth_config.yml
```
うまく動いてるか確認するため、以下のコマンドを実行。
```sh
# docker ps
CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS              PORTS                    NAMES
2c60f409cf02        cesanta/docker_auth   "/docker_auth/auth_s…"   8 seconds ago       Up 5 seconds        0.0.0.0:5001->5001/tcp   docker_auth01
```
動作してれば成功。  
これでひとまず認証に使われるコンテナは起動できたということになる。

そんで、このコンテナに割り当てられている IP アドレスを確認しておく。  
(結局 `docker inspect` から欲しい情報だけとってきただけ)
```sh
# docker inspect -f    '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' docker_auth01
172.17.0.2
```

次は、この認証コンテナと連動する Docker Private Registry を起動する。  
`REGISTRY_AUTH_TOKEN_REALM` 部分に先程確認した IP アドレスを記述して、以下のコマンドを実行。
```sh
# docker run -d -p 5000:5000 \
-e REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/var/lib/registry \
-e REGISTRY_AUTH=token \
-e REGISTRY_AUTH_TOKEN_REALM=https://172.17.0.2:5001/auth \
-e REGISTRY_AUTH_TOKEN_SERVICE="Docker registry" \
-e REGISTRY_AUTH_TOKEN_ISSUER="Auth Service" \
-e REGISTRY_AUTH_TOKEN_ROOTCERTBUNDLE=/ssl/server.pem \
-v /hostdir/auth_server/ssl:/ssl \
-v /hostdir/docker_registry/data:/var/lib/registry \
--restart=always \
--name registry01 registry:latest
```

そんで、コンテナが起動しているかをチェック。
```sh
# docker ps
CONTAINER ID        IMAGE                 COMMAND                  CREATED             STATUS              PORTS                    NAMES
bae574311d32        registry:latest       "/entrypoint.sh /etc…"   4 seconds ago       Up 3 seconds        0.0.0.0:5000->5000/tcp   registry01
2c60f409cf02        cesanta/docker_auth   "/docker_auth/auth_s…"   13 minutes ago      Up 13 minutes       0.0.0.0:5001->5001/tcp   docker_auth01
```


## 試しに動作確認してみる

正しく動作しているか、確認してみる。  
検証に使うイメージのベースは、以下のコマンドで予め取得しておく。
```sh
# docker pull supertest2014/nyan
```

- admin の場合
    1. ログイン  
        期待通り成功した
        ```sh
        # docker login localhost:5000
        Username: admin
        Password:
        WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
        Configure a credential helper to remove this warning. See
        https://docs.docker.com/engine/reference/commandline/login/#credentials-store
        
        Login Succeeded
        ```
    2. 新規イメージをタグ付けして push  
        期待通り成功した
        ```sh
        # docker tag supertest2014/nyan:latest localhost:5000/adminimage:1
        # docker push localhost:5000/adminimage:1
        The push refers to repository [localhost:5000/adminimage]
        5f70bf18a086: Pushed
        de532d116b89: Pushed
        56ff4794c2bd: Pushed
        cd42986834fa: Pushed
        4ee4b11cb732: Pushed
        1: digest: sha256:5e02468ee21d39506c8fdd795eaaffe46d1ac8f451c0251d4a8f263c6636ecfc size: 1775
        ```
    3. admin ユーザが push したイメージの pull  
        期待通り成功した
        ```sh
        # docker rmi localhost:5000/adminimage:1
        Untagged: localhost:5000/adminimage:1
        Untagged: localhost:5000/adminimage@sha256:5e02468ee21d39506c8fdd795eaaffe46d1ac8f451c0251d4a8f263c6636ecfc
        # docker pull localhost:5000/adminimage:1
        1: Pulling from adminimage
        Digest: sha256:5e02468ee21d39506c8fdd795eaaffe46d1ac8f451c0251d4a8f263c6636ecfc
        Status: Downloaded newer image for localhost:5000/adminimage:1
        localhost:5000/adminimage:1
        ```
    4. ログアウト  
        期待通り成功した
        ```sh
        # docker logout localhost:5000
        Removing login credentials for localhost:5000
        ```

- user01 の場合
    1. ログイン  
        期待通り成功した
        ```sh
        # docker login localhost:5000
        Username: user01
        Password:
        WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
        Configure a credential helper to remove this warning. See
        https://docs.docker.com/engine/reference/commandline/login/#credentials-store
        
        Login Succeeded
        ```
    2. 新規イメージをタグ付けして push  
        期待通り失敗した
        ```sh
        # docker tag supertest2014/nyan:latest localhost:5000/user01image:1
        # docker push localhost:5000/user01image:1
        The push refers to repository [localhost:5000/user01image]
        5f70bf18a086: Preparing
        de532d116b89: Preparing
        56ff4794c2bd: Preparing
        cd42986834fa: Preparing
        4ee4b11cb732: Preparing
        denied: requested access to the resource is denied
        ```
    3. admin ユーザが push したイメージの pull  
        期待通り成功した
        ```sh
        # docker pull localhost:5000/adminimage:1
        1: Pulling from adminimage
        Digest: sha256:5e02468ee21d39506c8fdd795eaaffe46d1ac8f451c0251d4a8f263c6636ecfc
        Status: Downloaded newer image for localhost:5000/adminimage:1
        localhost:5000/adminimage:1
        ```
    4. ログアウト  
        期待通り成功した
        ```sh
        # docker logout localhost:5000
        Removing login credentials for localhost:5000
        ```


- user02 の場合
    1. ログイン  
        期待通り成功した
        ```sh
        # docker login localhost:5000
        Username: user02
        Password:
        WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
        Configure a credential helper to remove this warning. See
        https://docs.docker.com/engine/reference/commandline/login/#credentials-store
        
        Login Succeeded
        ```
    2. 新規イメージをタグ付けして push  
        期待通り失敗した
        ```sh
        # docker tag supertest2014/nyan:latest localhost:5000/user02image:1
        # docker push localhost:5000/user02image:1
        The push refers to repository [localhost:5000/user02image]
        5f70bf18a086: Preparing
        de532d116b89: Preparing
        56ff4794c2bd: Preparing
        cd42986834fa: Preparing
        4ee4b11cb732: Preparing
        denied: requested access to the resource is denied
        ```
    3. admin ユーザが push したイメージの pull  
        期待通り失敗した
        ```sh
        # docker pull localhost:5000/adminimage:1
        Error response from daemon: pull access denied for localhost:5000/adminimage, repository does not exist or may require 'docker login': denied: requested access to the resource is denied
        ```
    4. ログアウト  
        期待通り成功した
        ```sh
        # docker logout localhost:5000
        Removing login credentials for localhost:5000
        ```


# go のライブラリを使って、DPR に対してイメージを push してみる

参考になりそうなのは、以下辺りか。

- [Examples using the Docker Engine SDKs and Docker API - Dpcker-docs](https://docs.docker.com/engine/api/sdk/examples/)
- [github.com/docker/docker/client - GoDoc](https://godoc.org/github.com/docker/docker/client)
- [github.com/docker/docker - GoDoc](https://godoc.org/github.com/docker/docker)
- [リモート API クライアント・ライブラリ - Docker-docs-ja](http://docs.docker.jp/engine/reference/remote_api_client_libraries.html)
-  [Go言語でdockerを操作する【イメージのpull,コンテナ作成，exec等】 - Qiita](https://qiita.com/jacky_dev/items/5429e75e5c0711add93a)
- [Goでdocker SDK を試してみる１ - yanom blog](https://yanomy.hatenablog.com/entry/2018/11/23/214549)
- [Ubuntu 19.04 に新しいバージョンの Go (プログラミング言語)をインストールする](https://www.randynetwork.com/blog/install-golang-for-ubuntu-1904/)


今週はちょっと調べるための時間を全然確保できてないな...。

ひとまず、実行に必要なパッケージや、ライブラリを導入。  
以下のコマンドを実行。

```sh
# apt install golang
```
その後、必要なライブラリをインストールしておく。
```sh
$ go get github.com/docker/docker/api/types
$ go get github.com/docker/docker/client
```

```sh
kanamaru@vm-ubuntu18:~$ go get github.com/docker/docker/api/types
kanamaru@vm-ubuntu18:~$ go get github.com/docker/docker/client
-- [実行結果] -----
# github.com/docker/docker/vendor/github.com/containerd/containerd/errdefs
go/src/github.com/docker/docker/vendor/github.com/containerd/containerd/errdefs/errors.go:54:9: undefined: "github.com/docker/docker/vendor/github.com/pkg/errors".Is
go/src/github.com/docker/docker/vendor/github.com/containerd/containerd/errdefs/errors.go:59:9: undefined: "github.com/docker/docker/vendor/github.com/pkg/errors".Is
go/src/github.com/docker/docker/vendor/github.com/containerd/containerd/errdefs/errors.go:65:9: undefined: "github.com/docker/docker/vendor/github.com/pkg/errors".Is
go/src/github.com/docker/docker/vendor/github.com/containerd/containerd/errdefs/errors.go:71:9: undefined: "github.com/docker/docker/vendor/github.com/pkg/errors".Is
go/src/github.com/docker/docker/vendor/github.com/containerd/containerd/errdefs/errors.go:76:9: undefined: "github.com/docker/docker/vendor/github.com/pkg/errors".Is
go/src/github.com/docker/docker/vendor/github.com/containerd/containerd/errdefs/errors.go:81:9: undefined: "github.com/docker/docker/vendor/github.com/pkg/errors".Is
go/src/github.com/docker/docker/vendor/github.com/containerd/containerd/errdefs/errors.go:86:9: undefined: "github.com/docker/docker/vendor/github.com/pkg/errors".Is
go/src/github.com/docker/docker/vendor/github.com/containerd/containerd/errdefs/errors.go:92:9: undefined: "github.com/docker/docker/vendor/github.com/pkg/errors".Is
```
エラーがでたな。Is がないとかなんとか。  
ちょっとホントに無いのか、チェックしてみるか。



```sh
kanamaru@vm-ubuntu18:~$ ls -1 /home/kanamaru/go/src/github.com/docker/docker/vendor/github.com/pkg/errors/
LICENSE
README.md
errors.go
go113.go
stack.go
```
ディレクトリ内にある `errors.go` の中には、たしかに `Is` ってメソッドはなかった。  
ただ、他にもチェックしてみると、以下のファイルに定義があった。

```sh
kanamaru@vm-ubuntu18:~$ cat /home/kanamaru/go/src/github.com/docker/docker/vendor/github.com/pkg/errors/go113.go
// +build go1.13

package errors

import (
        stderrors "errors"
)

// Is reports whether any error in err's chain matches target.
//
// The chain consists of err itself followed by the sequence of errors obtained by
// repeatedly calling Unwrap.
//
// An error is considered to match a target if it is equal to that target or if
// it implements a method Is(error) bool such that Is(target) returns true.
func Is(err, target error) bool { return stderrors.Is(err, target) }

// As finds the first error in err's chain that matches target, and if so, sets
// target to that error value and returns true.
//
// The chain consists of err itself followed by the sequence of errors obtained by
// repeatedly calling Unwrap.
//
// An error matches target if the error's concrete value is assignable to the value
// pointed to by target, or if the error has a method As(interface{}) bool such that
// As(target) returns true. In the latter case, the As method is responsible for
// setting target.
//
// As will panic if target is not a non-nil pointer to either a type that implements
// error, or to any interface type. As returns false if err is nil.
func As(err error, target interface{}) bool { return stderrors.As(err, target) }

// Unwrap returns the result of calling the Unwrap method on err, if err's
// type contains an Unwrap method returning error.
// Otherwise, Unwrap returns nil.
func Unwrap(err error) error {
        return stderrors.Unwrap(err)
}
```

ぱっと観た感じ、go のバージョンが 1.13 以上じゃあないと利用できないっぽいな。  
とりあえず、自分の環境をチェックしてみる。

```sh
kanamaru@vm-ubuntu18:~$ go version
go version go1.10.4 linux/amd64
```

古いな。  
仕方ないので [Ubuntu 19.04 に新しいバージョンの Go (プログラミング言語)をインストールする](https://www.randynetwork.com/blog/install-golang-for-ubuntu-1904/) を参考にして、go を 1.13 にしてみるか。

以下を実行。
```sh
# add-apt-repository ppa:longsleep/golang-backports
# apt update
# apt install golang
```

アップデートした結果、こうなった。
```sh
kanamaru@vm-ubuntu18:~$ go version
go version go1.14.2 linux/amd64
```

まぁこれならば動くだろ。







とりあえず、イメージ取得用のコードを書いてみる。



- `~/00-work/main.go`
    ```go
     1 package main
     2
     3 import (
     4     "context"
     5     "fmt"
     6     "bufio"
     7     "encoding/json"
     8
     9     "github.com/docker/docker/client"
    10     "github.com/docker/docker/api/types"
    11 )
    12
    13 func main()  {
    14     cli, err := client.NewClientWithOpts(client.FromEnv)
    15     if err != nil {
    16         panic(err)
    17     }
    18     ctx := context.Background()
    19
    20     resp, err := cli.ImagePull(ctx, "localhost:5000/ubuntu:Kana-1", types.ImagePullOptions{})
    21     if err != nil {
    22         panic(err)
    23     }
    24     defer resp.Close()
    25
    26     payload := struct {
    27         ID             string `json:"id"`
    28         Status         string `json:"status"`
    29         Progress       string `json:"progress"`
    30         ProgressDetail struct {
    31             Current uint16 `json:"current"`
    32             Total   uint16 `json:"total"`
    33         } `json:"progressDetail"`
    34     }{}
    35
    36     scanner := bufio.NewScanner(resp)
    37     for scanner.Scan() {
    38         json.Unmarshal(scanner.Bytes(), &payload)
    39         fmt.Printf("\t%+v\n", payload)
    40     }
    41
    42 }
    ```

ちなみに、イメージのプルは `ImagePull` に対して、第2引数にpullしたいイメージ名を指定することで実行できる。  
今回はローカルのレジストリなので `localhost:5000/ubuntu:Kana-1` みたいな感じで指定することになる。  
何も指定しない場合はlatestがpullされるらしい。

第3引数にはpull時のオプションを指定できて、利用できるオプションは以下の通りらしい。
```go
type ImagePullOptions struct {
    All           bool   // If true,all tags for the given image to be pulled.
    RegistryAuth  string // RegistryAuth is the base64 encoded credentials for the registry
    PrivilegeFunc RequestPrivilegeFunc
    Platform      string //Platform in the format os[/arch[/variant]]
}
```

実際に実行してみると、以下のエラーが出た。
```sh
kanamaru@vm-ubuntu18:~/00-work$ go run main.go
panic: Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post "http://%2Fvar%2Frun%2Fdocker.sock/v1.41/images/create?fromImage=localhost%3A5000%2Fubuntu&tag=Kana-1": dial unix /var/run/docker.sock: connect: permission denied

goroutine 1 [running]:
main.main()
        /home/kanamaru/00-work/main.go:22 +0x36e
exit status 2
```

パーミッションエラーだな。まぁ一般ユーザの権限で docker を叩いてるわけだから、そりゃ怒られるか。  
とりあえず、`sudo` つけて実行してみる。  
(駄目ならちょっと調べてみる)

```sh
kanamaru@vm-ubuntu18:~/00-work$ sudo go run ./main.go
panic: Error response from daemon: client version 1.41 is too new. Maximum supported API version is 1.40

goroutine 1 [running]:
main.main()
        /home/kanamaru/00-work/main.go:22 +0x36e
exit status 2
```

あーやっぱエラー内容が変わったね。  
これについては、API と docker のバージョンが対応してないときのエラーらしいから、ちょっとソースを弄ってみる。

- `~/00-work/main.go`
    ```go
     1 package main
     2
     3 import (
     4     "context"
     5     "fmt"
     6     "bufio"
     7     "encoding/json"
     8
     9     "github.com/docker/docker/client"
    10     "github.com/docker/docker/api/types"
    11 )
    12
    13 func main()  {
    14     cli, err := client.NewClientWithOpts(client.WithVersion("1.40"))  // ★ココをいじった
    15     if err != nil {
    16         panic(err)
    17     }
    18     ctx := context.Background()
    19
    20     resp, err := cli.ImagePull(ctx, "localhost:5000/ubuntu:Kana-1", types.ImagePullOptions{})
    21     if err != nil {
    22         panic(err)
    23     }
    24     defer resp.Close()
    25
    26     payload := struct {
    27         ID             string `json:"id"`
    28         Status         string `json:"status"`
    29         Progress       string `json:"progress"`
    30         ProgressDetail struct {
    31             Current uint16 `json:"current"`
    32             Total   uint16 `json:"total"`
    33         } `json:"progressDetail"`
    34     }{}
    35
    36     scanner := bufio.NewScanner(resp)
    37     for scanner.Scan() {
    38         json.Unmarshal(scanner.Bytes(), &payload)
    39         fmt.Printf("\t%+v\n", payload)
    40     }
    41
    42 }
    ```

そんで、改めて実行してみる。

```sh
kanamaru@vm-ubuntu18:~/00-work$ sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              18.04               d27b9ffc5667        7 days ago          64.2MB
registry            latest              2d4f4b5309b1        3 weeks ago         26.2MB

kanamaru@vm-ubuntu18:~/00-work$ sudo go run ./main.go
        {ID:Kana-1 Status:Pulling from ubuntu Progress: ProgressDetail:{Current:0 Total:0}}
        {ID:Kana-1 Status:Digest: sha256:3013b0d761d4bad6ff16dd2805887a2f2c3fc140d6206086698b5c3e44e0f7fe Progress: ProgressDetail:{Current:0 Total:0}}
        {ID:Kana-1 Status:Status: Downloaded newer image for localhost:5000/ubuntu:Kana-1 Progress: ProgressDetail:{Current:0 Total:0}}

kanamaru@vm-ubuntu18:~/00-work$ sudo docker images
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
ubuntu                  18.04               d27b9ffc5667        7 days ago          64.2MB
localhost:5000/ubuntu   Kana-1              d27b9ffc5667        7 days ago          64.2MB
registry                latest              2d4f4b5309b1        3 weeks ago         26.2MB
```
何か取れたっぽいな。

とりあえず、確認してみる。

```sh
root@vm-ubuntu18:~# docker images
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
ubuntu                  18.04               d27b9ffc5667        6 days ago          64.2MB
localhost:5000/ubuntu   Kana-1              d27b9ffc5667        6 days ago          64.2MB
registry                latest              2d4f4b5309b1        3 weeks ago         26.2MB
```

確かにイメージの取得に成功したっぽいから、これでおｋとするか。




