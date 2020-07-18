# 普通の DockerPrivateRegistry を作ってみる

参考：http://docs.docker.jp/v1.12/registry/configuration.html

参考：https://www.itmedia.co.jp/enterprise/articles/1708/10/news052_3.html


とりあえず、登録されたイメージを保管するディレクトリを作成。
```
# mkdir -p /home/docker_regisrty/data
```


そんで必要なコンテナイメージを取得
```
# docker pull registry
```



最後にコンテナとして DPR を起動
```
# docker run -d \
-p 5000:5000 \
-e REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/var/lib/registry \
-v /home/docker_registry/data:/var/lib/registry \
--restart=always \
--name registry01 registry:latest
```

以上。



# 普通の DockerPrivateRegistry にイメージを登録してみる


まずは登録するため、適当なイメージを作成する
```
# docker pull ubuntu:18.04
```

次に、入手したイメージにオリジナルのタグを付ける
このタグを元に登録するレジストリが決まるので、さっき作ったやつをちゃんと指定すること
```
# docker tag ubuntu:18.04 localhost:5000/ubuntu:Kana-1
```

登録するとこんな感じになる。
```
# docker images
--[実行結果]------------------------------
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
ubuntu                  18.04               4e5021d210f6        15 hours ago        64.2MB
localhost:5000/ubuntu   Kana-1              4e5021d210f6        15 hours ago        64.2MB
registry                latest              708bc6af7e5e        8 weeks ago         25.8MB

```

念の為、まだイメージが登録されていないことを、確認してみる
```
# ll /home/docker_registry/data/
--[実行結果]------------------------------
合計 8
drwxr-xr-x 2 root root 4096  3月 21 18:54 ./
drwxr-xr-x 3 root root 4096  3月 21 18:54 ../
```

確認できたので、 push してみる
```
# docker push localhost:5000/ubuntu:Kana-1
```


ちゃんとイメージが登録されたか観てみる。
```
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












# docker_auth と組み合わせた DockerPrivateRegistry を作ってみる








```
# docker run -d \
-p 5000:5000 \
-e REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/var/lib/registry \
-e REGISTRY_AUTH=token \
-e REGISTRY_AUTH_TOKEN_REALM=https://localhsot:5001/auth \
-e REGISTRY_AUTH_TOKEN_SERVICE="Docker registry" \
-e REGISTRY_AUTH_TOKEN_ISSUER="Auth Service" \
-e REGISTRY_AUTH_TOKEN_ROOTCERTBUNDLE=/ssl/server.pem \
-v /hostdir/auth_server/ssl:/ssl \
-v /hostdir/docker_registry/data:/var/lib/registry \
--restart=always \
--name registry01 registry:latest
```








