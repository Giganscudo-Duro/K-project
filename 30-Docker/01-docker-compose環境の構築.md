# docker-compose のインストール
docker-compose には専用のパッケージなどは無いので、実行ファイルをダウンロード＆実行権限付与という操作になる。
先ずは上記を実行するため、以下のコマンドを実行する。
```shell
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.28.6/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
```
実行権限を付与できないときは、以下のコマンドで代用する。
```shell
$ sudo chmod 755 /usr/local/bin/docker-compose
```

# docker-compose のアップグレード
docker-compose は実行ファイルをダウンロードして使うという性質上、`yum` コマンドでアップグレード出来無い。
そのため、以下のコマンドを実行して、アップグレードを行うことになる。
ただ、`--help` 見ても、そんなオプションないんだよなぁ。
```shell
$ sudo docker-compose migrate-to-labels
```

# docker-compose のアンインストール
docker-compose をアンインストールしたい場合は、docker-compose の実行ファイルを削除すればOK。
以下のコマンドを実行する。
```shell
$ sudo rm /usr/local/bin/docker-compose
```


# 参考URL

- [Install Docker Compose - Docker Docs](https://docs.docker.com/compose/install/)
