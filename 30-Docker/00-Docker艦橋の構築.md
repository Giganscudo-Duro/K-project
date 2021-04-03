

# Red Hat 系の場合
**基本的に公式ページの要点抜粋！！ なので必要に応じて公式を参照のこと！！**


## 1. 公式以外の Docker を排除する
公式版と Red Hat 版の競合があるため、関係するパッケージ一式を排除する必要がある。
もし何らかの Docker をインストールしていた場合は、以下のコマンドを実行して排除する。

```shell
$ sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```




## 2. yum コマンド実行時に使うパッケージを導入する
公式版 Docker をインストールする際には、特定のリポジトリを有効化して `yum` コマンドを実行することになる。
先ずは、そのオプションを使うためのパッケージと、公式 Docker リポジトリを追加するため、以下のコマンドを実行する。

```shell
$ sudo yum install -y yum-utils

$ sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```


## 3. Docker-CE を導入する
とりあえず、最新版をいれればOKなので、以下のコマンドを実行する。

```shell
$ sudo yum install docker-ce docker-ce-cli containerd.io
```

## 4. Docker-CE をサービスとして登録＆スタートさせる


```shell
$ sudo systemctl enable docker
$ sudo systemctl start docker
```



# 番外編）Docker をアンインストールする場合
    Uninstall the Docker Engine, CLI, and Containerd packages:
関連パッケージを削除するため、以下のコマンドを実行する。
```shell
$ sudo yum remove docker-ce docker-ce-cli containerd.io
```

イメージやレイヤーなども削除するため、以下のコマンドを実行する。
```shell
$ sudo rm -rf /var/lib/docker
$ sudo rm -rf /var/lib/containerd
```



# 参考URL
[公式Docker導入の手順 - Doker Docs](https://docs.docker.com/get-docker/)
