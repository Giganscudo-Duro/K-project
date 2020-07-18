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

以上。











# API 経由で pull してみる

事前調査してみて、有力そうなのは以下。
- 参考：https://docs.docker.com/registry/spec/api/#pulling-an-image
- 参考：https://qiita.com/ryuichi1208/items/e4e1b27ff7d54a66dcd9

さっき 「localhost:5000」 に登録した「ubuntu:Kana-1」を対象に pull を実行してみる
参考にするのは、公式の API ドキュメント。
ホントは `push` について知りたいのだけれど、まずは `pull` から。



## Pulling an Image Manifest

イメージのマニフェストを取得するため、以下のコマンドを実行
```
# curl -X GET <DPR>/v2/<NAME>/manifests/<REFERENCE>
----------------------------------------------------
    DPR        -> レジストリの URI
    NAME       -> 対象とするイメージの名前
    REFERENCE  -> 対象とするイメージのタグ or digest
```


とりあえず、先程の環境で実行すると、以下のような感じになった
```
# curl -X GET localhost:5000/v2/ubuntu/manifests/Kana-1
--[実行結果]------------------------------
{
   "schemaVersion": 1,
   "name": "ubuntu",
   "tag": "Kana-1",
   "architecture": "amd64",
   "fsLayers": [
      {
         "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
      },
      {
         "blobSum": "sha256:78bf9a5ad49e4ae42a83f4995ade4efc096f78fd38299cf05bc041e8cdda2a36"
      },
      {
         "blobSum": "sha256:930bda195c84cf132344bf38edcad255317382f910503fef234a9ce3bff0f4dd"
      },
      {
         "blobSum": "sha256:f11b29a9c7306674a9479158c1b4259938af11b97359d9ac02030cc1095e9ed1"
      },
      {
         "blobSum": "sha256:5bed26d33875e6da1d9ff9a1054c5fef3bbeb22ee979e14b72acf72528de007b"
      }
   ],
   "history": [
      {
         "v1Compatibility": "{\"architecture\":\"amd64\",\"config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/bin/bash\"],\"ArgsEscaped\":true,\"Image\":\"sha256:257f42741ca08b6d23bb7cc030bb3ce32278879eb87d1f7c8195ddf9057807cb\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"container\":\"f35b3af588999f5c47b8132845d7e6c3a220cedac21a8dada926f41de36eef55\",\"container_config\":{\"Hostname\":\"f35b3af58899\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/bin/sh\",\"-c\",\"#(nop) \",\"CMD [\\\"/bin/bash\\\"]\"],\"ArgsEscaped\":true,\"Image\":\"sha256:257f42741ca08b6d23bb7cc030bb3ce32278879eb87d1f7c8195ddf9057807cb\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":{}},\"created\":\"2020-03-20T19:20:22.835345724Z\",\"docker_version\":\"18.09.7\",\"id\":\"e3b70a2503b80c1049c85825982e2515f1d3896c86bd9d11ace9a1bbd3e95746\",\"os\":\"linux\",\"parent\":\"530714999d66683d03b28493dcf286a2e3885f13782a33b3297248f194d722f9\",\"throwaway\":true}"
      },
      {
         "v1Compatibility": "{\"id\":\"530714999d66683d03b28493dcf286a2e3885f13782a33b3297248f194d722f9\",\"parent\":\"f8f60a5a48f11db14452833d2fe054e5414f432172c71b481bcc305dca6d1e85\",\"created\":\"2020-03-20T19:20:22.640524898Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c mkdir -p /run/systemd \\u0026\\u0026 echo 'docker' \\u003e /run/systemd/container\"]}}"
      },
      {
         "v1Compatibility": "{\"id\":\"f8f60a5a48f11db14452833d2fe054e5414f432172c71b481bcc305dca6d1e85\",\"parent\":\"831cfbd6a00f9b2b733b457f7ade7f4a3bf53a010212495d527223d15fda9718\",\"created\":\"2020-03-20T19:20:21.887904759Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c set -xe \\t\\t\\u0026\\u0026 echo '#!/bin/sh' \\u003e /usr/sbin/policy-rc.d \\t\\u0026\\u0026 echo 'exit 101' \\u003e\\u003e /usr/sbin/policy-rc.d \\t\\u0026\\u0026 chmod +x /usr/sbin/policy-rc.d \\t\\t\\u0026\\u0026 dpkg-divert --local --rename --add /sbin/initctl \\t\\u0026\\u0026 cp -a /usr/sbin/policy-rc.d /sbin/initctl \\t\\u0026\\u0026 sed -i 's/^exit.*/exit 0/' /sbin/initctl \\t\\t\\u0026\\u0026 echo 'force-unsafe-io' \\u003e /etc/dpkg/dpkg.cfg.d/docker-apt-speedup \\t\\t\\u0026\\u0026 echo 'DPkg::Post-Invoke { \\\"rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true\\\"; };' \\u003e /etc/apt/apt.conf.d/docker-clean \\t\\u0026\\u0026 echo 'APT::Update::Post-Invoke { \\\"rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true\\\"; };' \\u003e\\u003e /etc/apt/apt.conf.d/docker-clean \\t\\u0026\\u0026 echo 'Dir::Cache::pkgcache \\\"\\\"; Dir::Cache::srcpkgcache \\\"\\\";' \\u003e\\u003e /etc/apt/apt.conf.d/docker-clean \\t\\t\\u0026\\u0026 echo 'Acquire::Languages \\\"none\\\";' \\u003e /etc/apt/apt.conf.d/docker-no-languages \\t\\t\\u0026\\u0026 echo 'Acquire::GzipIndexes \\\"true\\\"; Acquire::CompressionTypes::Order:: \\\"gz\\\";' \\u003e /etc/apt/apt.conf.d/docker-gzip-indexes \\t\\t\\u0026\\u0026 echo 'Apt::AutoRemove::SuggestsImportant \\\"false\\\";' \\u003e /etc/apt/apt.conf.d/docker-autoremove-suggests\"]}}"
      },
      {
         "v1Compatibility": "{\"id\":\"831cfbd6a00f9b2b733b457f7ade7f4a3bf53a010212495d527223d15fda9718\",\"parent\":\"8fb0b731671252f48390a80acfa8aa2a69453705b14d2ff67b3a12a0495baafd\",\"created\":\"2020-03-20T19:20:21.136950754Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c [ -z \\\"$(apt-get indextargets)\\\" ]\"]}}"
      },
      {
         "v1Compatibility": "{\"id\":\"8fb0b731671252f48390a80acfa8aa2a69453705b14d2ff67b3a12a0495baafd\",\"created\":\"2020-03-20T19:20:20.247087133Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop) ADD file:594fa35cf803361e69d817fc867b6a4069c064ffd20ed50caf42ad9bb11ca999 in / \"]}}"
      }
   ],
   "signatures": [
      {
         "header": {
            "jwk": {
               "crv": "P-256",
               "kid": "BXBO:HQHS:YLCS:XIII:DW2N:N32P:4BVM:XFY2:BHH5:IMQK:ROGU:XGFB",
               "kty": "EC",
               "x": "xwcmmv0KpR7BI6-0bOFUN8tB8kD4mUso7OCjBspeYOU",
               "y": "uGwx1TKq87IzhdX0ihMeyfOzpup6dJzjgOlp8KmrViA"
            },
            "alg": "ES256"
         },
         "signature": "Wr9Y6yV2K5ni3KFpiga2Ud1aFjByseKGfQLvXDfRX2FEBQbDGlJfeCPocZtyoDpo0ID6VrkJ5eJksghSZHJZkQ",
         "protected": "eyJmb3JtYXRMZW5ndGgiOjQ5MjIsImZvcm1hdFRhaWwiOiJDbjAiLCJ0aW1lIjoiMjAyMC0wMy0yMVQxMDoxNzowM1oifQ"
      }
   ]
}
```



ドキュメントによると、上記の `blobSum` に記載されているのが「digest」なのだとか。
以下は参考。
```
{
   "name": <name>,
   "tag": <tag>,
   "fsLayers": [
      {
         "blobSum": <digest>
      },
      ...
    ]
   ],
   "history": <v1 images>,
   "signature": <JWS>
}
```



あと、 `"schemaVersion": 1` ってのが気になる。
調べてみると、こんなページを見つけた。
```
Image Manifest V 2, Schema 1 -> https://docs.docker.com/registry/spec/manifest-v2-1/
Image Manifest V 2, Schema 2 -> https://docs.docker.com/registry/spec/manifest-v2-2/
```
上記を見た感じだと、 `"schemaVersion": 2` ってのも取れるのかね。



上記の URL を観た限りだと、指定できるものとしていかが用意されているらしい。
```
Media Types
The following media types are used by the manifest formats described here, and the resources they reference:

application/vnd.docker.distribution.manifest.v1+json:      schema1 (existing manifest format)
application/vnd.docker.distribution.manifest.v2+json:      New image manifest format (schemaVersion = 2)
application/vnd.docker.distribution.manifest.list.v2+json: Manifest list, aka "fat manifest"
application/vnd.docker.container.image.v1+json:            Container config JSON
application/vnd.docker.image.rootfs.diff.tar.gzip:         "Layer", as a gzipped tar
application/vnd.docker.image.rootfs.foreign.diff.tar.gzip: "Layer", as a gzipped tar that should never be pushed
application/vnd.docker.plugin.v1+json:                     Plugin config JSON
```


こっちでもやってみる。
とりあえず、以下のコマンドを実行。
```
# curl -X GET -H 'Accept: application/vnd.docker.distribution.manifest.v2+json' localhost:5000/v2/ubuntu/manifests/Kana-1
--[実行結果]------------------------------
{
   "schemaVersion": 2,
   "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
   "config": {
      "mediaType": "application/vnd.docker.container.image.v1+json",
      "size": 3408,
      "digest": "sha256:4e5021d210f65ebe915670c7089120120bc0a303b90208592851708c1b8c04bd"
   },
   "layers": [
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 26690587,
         "digest": "sha256:5bed26d33875e6da1d9ff9a1054c5fef3bbeb22ee979e14b72acf72528de007b"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 35372,
         "digest": "sha256:f11b29a9c7306674a9479158c1b4259938af11b97359d9ac02030cc1095e9ed1"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 848,
         "digest": "sha256:930bda195c84cf132344bf38edcad255317382f910503fef234a9ce3bff0f4dd"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 162,
         "digest": "sha256:78bf9a5ad49e4ae42a83f4995ade4efc096f78fd38299cf05bc041e8cdda2a36"
      }
   ]
}
```

どういうわけか「application/vnd.docker.image.rootfs.diff.tar.gzip」の情報も一緒についてきたっぽい。
まぁ多分、コンテナイメージは「ベースとなるイメージとその差分」なので、diff ってことは差分ファイルなのかもしれない。







## Existing Manifests
ちなみに、マニフェストが存在するか否かを簡潔に確認するだけならば、以下でも良いらしい。
```
HEAD /v2/<name>/manifests/<reference>
```

期待するのは、以下のようなレスポンス
```
200 OK
Content-Length: <length of manifest>
Docker-Content-Digest: <digest>
```




実行してみたけれど、`-X HEAD` とかは使えないみたい。

```
# curl -X HEAD localhost:5000/v2/ubuntu/manifests/Kana-1
--[実行結果]------------------------------
Warning: Setting custom HTTP method to HEAD with -X/--request may not work the
Warning: way you want. Consider using -I/--head instead.
^C
```

とりあえず `-I` で動いたからまぁいいや。
```
# curl -I localhost:5000/v2/ubuntu/manifests/Kana-1
--[実行結果]------------------------------
HTTP/1.1 200 OK
Content-Length: 5569
Content-Type: application/vnd.docker.distribution.manifest.v1+prettyjws
Docker-Content-Digest: sha256:bc12321026b5d738dde7bd29ddf7b7330d95623b409597dc5c2ee84cf5ca1c7b
Docker-Distribution-Api-Version: registry/2.0
Etag: "sha256:bc12321026b5d738dde7bd29ddf7b7330d95623b409597dc5c2ee84cf5ca1c7b"
X-Content-Type-Options: nosniff
Date: Sat, 21 Mar 2020 10:27:07 GMT
```

気になるのは、さっきだと「digest」は複数個あったのに、こっちだと1個しか無いこと。
どっちが正しいのだろうか。



## Pulling a Layer

とりあえず、digest なるものの情報は得られた。

候補１：
```
"fsLayers": [
   {"blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"},
   {"blobSum": "sha256:78bf9a5ad49e4ae42a83f4995ade4efc096f78fd38299cf05bc041e8cdda2a36"},
   {"blobSum": "sha256:930bda195c84cf132344bf38edcad255317382f910503fef234a9ce3bff0f4dd"},
   {"blobSum": "sha256:f11b29a9c7306674a9479158c1b4259938af11b97359d9ac02030cc1095e9ed1"},
   {"blobSum": "sha256:5bed26d33875e6da1d9ff9a1054c5fef3bbeb22ee979e14b72acf72528de007b"}
],
```




候補２：  
実際は候補１とほぼ同じ。  
無いのは `a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4` の部分。
```
"layers": [
   {"digest": "sha256:5bed26d33875e6da1d9ff9a1054c5fef3bbeb22ee979e14b72acf72528de007b"},
   {"digest": "sha256:f11b29a9c7306674a9479158c1b4259938af11b97359d9ac02030cc1095e9ed1"},
   {"digest": "sha256:930bda195c84cf132344bf38edcad255317382f910503fef234a9ce3bff0f4dd"},
   {"digest": "sha256:78bf9a5ad49e4ae42a83f4995ade4efc096f78fd38299cf05bc041e8cdda2a36"}
]
```



候補３：
```
Docker-Content-Digest: sha256:bc12321026b5d738dde7bd29ddf7b7330d95623b409597dc5c2ee84cf5ca1c7b
```

どれが正しいのかわからないけれど、とりあえずこれらを利用して pull してみる。

以下のコマンドを実行
```
# curl -X GET <DPR>/v2/<NAME>/blobs/<DIGEST>
----------------------------------------------------
    DPR     -> レジストリの URI
    NAME    -> 対象とするイメージの名前
    DIGEST  -> 対象とするイメージのdigest
```





候補１を使うと以下のようなレスポンス、エラーは起きなかった。
ちゃんとファイルを取得しようとしているみたい。
指示に従って `--output` をつければ、ちゃんと何かしらのファイルを取得できそう。
```
$ curl -X GET localhost:5000/v2/ubuntu/blobs/sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4
Warning: Binary output can mess up your terminal. Use "--output -" to tell
Warning: curl to output it to your terminal anyway, or consider "--output
Warning: <FILE>" to save to a file.
```
```
$ curl -X GET localhost:5000/v2/ubuntu/blobs/sha256:78bf9a5ad49e4ae42a83f4995ade4efc096f78fd38299cf05bc041e8cdda2a36
Warning: Binary output can mess up your terminal. Use "--output -" to tell
Warning: curl to output it to your terminal anyway, or consider "--output
Warning: <FILE>" to save to a file.
```
```
$ curl -X GET localhost:5000/v2/ubuntu/blobs/sha256:930bda195c84cf132344bf38edcad255317382f910503fef234a9ce3bff0f4dd
Warning: Binary output can mess up your terminal. Use "--output -" to tell
Warning: curl to output it to your terminal anyway, or consider "--output
Warning: <FILE>" to save to a file.
```
```
$ curl -X GET localhost:5000/v2/ubuntu/blobs/sha256:f11b29a9c7306674a9479158c1b4259938af11b97359d9ac02030cc1095e9ed1
Warning: Binary output can mess up your terminal. Use "--output -" to tell
Warning: curl to output it to your terminal anyway, or consider "--output
Warning: <FILE>" to save to a file.
```
```
$ curl -X GET localhost:5000/v2/ubuntu/blobs/sha256:5bed26d33875e6da1d9ff9a1054c5fef3bbeb22ee979e14b72acf72528de007b
Warning: Binary output can mess up your terminal. Use "--output -" to tell
Warning: curl to output it to your terminal anyway, or consider "--output
Warning: <FILE>" to save to a file.
```


一方で候補３を使って実行すると、以下のエラーがでた。
```
# curl -s -X GET localhost:5000/v2/ubuntu/blobs/sha256:bc12321026b5d738dde7bd29ddf7b7330d95623b409597dc5c2ee84cf5ca1c7b |jq
--[実行結果]------------------------------
{
  "errors": [
    {
      "code": "BLOB_UNKNOWN",
      "message": "blob unknown to registry",
      "detail": "sha256:bc12321026b5d738dde7bd29ddf7b7330d95623b409597dc5c2ee84cf5ca1c7b"
    }
  ]
}
```

おそらくだけど、「digest」なるものに関しては、候補１の方を使うべきみたい。
まぁ、コンテナイメージってのは「複数のレイヤーを重ねて一つに見せかけてる」もんなので、これら５つのレイヤーをまとめてやると、期待通りのコンテナイメージになるのかもしれない。

もしかしたら、レイヤー１つで構成されたイメージならば、候補１,２.３が同一の値を取るのかもしれないけれど...そこまで調べてみる気は起きない。
とりあえず、有力そうな候補１を使ってどんなファイルを取得できるか確認してみる。

```
多分BASE -> sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4
多分DIFF -> sha256:78bf9a5ad49e4ae42a83f4995ade4efc096f78fd38299cf05bc041e8cdda2a36
多分DIFF -> sha256:930bda195c84cf132344bf38edcad255317382f910503fef234a9ce3bff0f4dd
多分DIFF -> sha256:f11b29a9c7306674a9479158c1b4259938af11b97359d9ac02030cc1095e9ed1
多分DIFF -> sha256:5bed26d33875e6da1d9ff9a1054c5fef3bbeb22ee979e14b72acf72528de007b
```



```
$ curl -X GET --output layer.tar localhost:5000/v2/ubuntu/blobs/sha256:5bed26d33875e6da1d9ff9a1054c5fef3bbeb22ee979e14b72acf72528de007b
--[実行結果]------------------------------
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 25.4M  100 25.4M    0     0   509M      0 --:--:-- --:--:-- --:--:--  509M
```

ちなみにファイルタイプは `gzip` らしい。  
まぁ、メディアタイプに「application/vnd.docker.image.rootfs.diff.tar.gzip」とあったし、正確には `tar.gz` だろうな...。
```
$ file layer.tar
layer.tar: gzip compressed data
```

拡張子が整合してないのは気に入らないので、やり直す。


```
$ curl -X GET --output layer.tar.gz localhost:5000/v2/ubuntu/blobs/sha256:5bed26d33875e6da1d9ff9a1054c5fef3bbeb22ee979e14b72acf72528de007b
--[実行結果]------------------------------
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 25.4M  100 25.4M    0     0   374M      0 --:--:-- --:--:-- --:--:--  379M
```

とりあえず `tar.gz` だと思って、展開してみる。
以下のコマンドを実行。
```
$ tar -axvf layer.tar.gz && ll
--[実行結果]------------------------------
合計 26152
drwxrwxr-x 21 kanamaru kanamaru     4096  3月 22 23:45 ./
drwxrwxr-x  4 kanamaru kanamaru     4096  3月 22 18:25 ../
drwxr-xr-x  2 kanamaru kanamaru     4096  3月 12 06:05 bin/
drwxr-xr-x  2 kanamaru kanamaru     4096  4月 24  2018 boot/
drwxr-xr-x  2 kanamaru kanamaru     4096  3月 12 06:05 dev/
drwxr-xr-x 29 kanamaru kanamaru     4096  3月 12 06:05 etc/
drwxr-xr-x  2 kanamaru kanamaru     4096  4月 24  2018 home/
-rw-rw-r--  1 kanamaru kanamaru 26690587  3月 22 23:44 layer.tar.gz
drwxr-xr-x  8 kanamaru kanamaru     4096  5月 23  2017 lib/
drwxr-xr-x  2 kanamaru kanamaru     4096  3月 12 06:03 lib64/
drwxr-xr-x  2 kanamaru kanamaru     4096  3月 12 06:03 media/
drwxr-xr-x  2 kanamaru kanamaru     4096  3月 12 06:03 mnt/
drwxr-xr-x  2 kanamaru kanamaru     4096  3月 12 06:03 opt/
drwxr-xr-x  2 kanamaru kanamaru     4096  4月 24  2018 proc/
drwx------  2 kanamaru kanamaru     4096  3月 12 06:05 root/
drwxr-xr-x  4 kanamaru kanamaru     4096  3月 12 06:03 run/
drwxr-xr-x  2 kanamaru kanamaru     4096  3月 12 06:05 sbin/
drwxr-xr-x  2 kanamaru kanamaru     4096  3月 12 06:03 srv/
drwxr-xr-x  2 kanamaru kanamaru     4096  4月 24  2018 sys/
drwxrwxr-x  2 kanamaru kanamaru     4096  3月 12 06:05 tmp/
drwxr-xr-x 10 kanamaru kanamaru     4096  3月 12 06:03 usr/
drwxr-xr-x 11 kanamaru kanamaru     4096  3月 12 06:05 var/
```

あたりっぽい。
他の「DIFF（仮）」も同じ要領で取得できた。  
一方で、「BASE（仮）」は何故か展開できなかったので、失敗だと思う。  
個人調査では限界があるので、コレまでにわかった情報を使って、再び Google 先生に尋ねてみる。


見つけたものの中で有力そうなのは以下。  
っていうか、このシェルスクリプトそのまま流用すればいいんじゃね？
- 参考：https://github.com/moby/moby/blob/master/contrib/download-frozen-image-v2.sh
- 参考：https://knqyf263.hatenablog.com/entry/2019/11/29/052818


以下はシェルスクリプトのコピペ。

```
#!/usr/bin/env bash
set -eo pipefail

# hello-world                      latest              ef872312fe1b        3 months ago        910 B
# hello-world                      latest              ef872312fe1bbc5e05aae626791a47ee9b032efa8f3bda39cc0be7b56bfe59b9   3 months ago        910 B

# debian                           latest              f6fab3b798be        10 weeks ago        85.1 MB
# debian                           latest              f6fab3b798be3174f45aa1eb731f8182705555f89c9026d8c1ef230cbf8301dd   10 weeks ago        85.1 MB

# check if essential commands are in our PATH
for cmd in curl jq go; do
    if ! command -v $cmd &> /dev/null; then
        echo >&2 "error: \"$cmd\" not found!"
        exit 1
    fi
done

usage() {
    echo "usage: $0 dir image[:tag][@digest] ..."
    echo "       $0 /tmp/old-hello-world hello-world:latest@sha256:8be990ef2aeb16dbcb9271ddfe2610fa6658d13f6dfb8bc72074cc1ca36966a7"
    [ -z "$1" ] || exit "$1"
}

dir="$1" # dir for building tar in
shift || usage 1 >&2

[ $# -gt 0 -a "$dir" ] || usage 2 >&2
mkdir -p "$dir"

# hacky workarounds for Bash 3 support (no associative arrays)
images=()
rm -f "$dir"/tags-*.tmp
manifestJsonEntries=()
doNotGenerateManifestJson=
# repositories[busybox]='"latest": "...", "ubuntu-14.04": "..."'

# bash v4 on Windows CI requires CRLF separator
newlineIFS=$'\n'
if [ "$(go env GOHOSTOS)" = 'windows' ]; then
    major=$(echo ${BASH_VERSION%%[^0.9]} | cut -d. -f1)
    if [ "$major" -ge 4 ]; then
        newlineIFS=$'\r\n'
    fi
fi

registryBase='https://registry-1.docker.io'
authBase='https://auth.docker.io'
authService='registry.docker.io'

# https://github.com/moby/moby/issues/33700
fetch_blob() {
    local token="$1"
    shift
    local image="$1"
    shift
    local digest="$1"
    shift
    local targetFile="$1"
    shift
    local curlArgs=("$@")

    local curlHeaders="$(
        curl -S "${curlArgs[@]}" \
            -H "Authorization: Bearer $token" \
            "$registryBase/v2/$image/blobs/$digest" \
            -o "$targetFile" \
            -D-
    )"
    curlHeaders="$(echo "$curlHeaders" | tr -d '\r')"
    if grep -qE "^HTTP/[0-9].[0-9] 3" <<< "$curlHeaders"; then
        rm -f "$targetFile"

        local blobRedirect="$(echo "$curlHeaders" | awk -F ': ' 'tolower($1) == "location" { print $2; exit }')"
        if [ -z "$blobRedirect" ]; then
            echo >&2 "error: failed fetching '$image' blob '$digest'"
            echo "$curlHeaders" | head -1 >&2
            return 1
        fi

        curl -fSL "${curlArgs[@]}" \
            "$blobRedirect" \
            -o "$targetFile"
    fi
}

# handle 'application/vnd.docker.distribution.manifest.v2+json' manifest
handle_single_manifest_v2() {
    local manifestJson="$1"
    shift

    local configDigest="$(echo "$manifestJson" | jq --raw-output '.config.digest')"
    local imageId="${configDigest#*:}" # strip off "sha256:"

    local configFile="$imageId.json"
    fetch_blob "$token" "$image" "$configDigest" "$dir/$configFile" -s

    local layersFs="$(echo "$manifestJson" | jq --raw-output --compact-output '.layers[]')"
    local IFS="$newlineIFS"
    local layers=($layersFs)
    unset IFS

    echo "Downloading '$imageIdentifier' (${#layers[@]} layers)..."
    local layerId=
    local layerFiles=()
    for i in "${!layers[@]}"; do
        local layerMeta="${layers[$i]}"

        local layerMediaType="$(echo "$layerMeta" | jq --raw-output '.mediaType')"
        local layerDigest="$(echo "$layerMeta" | jq --raw-output '.digest')"

        # save the previous layer's ID
        local parentId="$layerId"
        # create a new fake layer ID based on this layer's digest and the previous layer's fake ID
        layerId="$(echo "$parentId"$'\n'"$layerDigest" | sha256sum | cut -d' ' -f1)"
        # this accounts for the possibility that an image contains the same layer twice (and thus has a duplicate digest value)

        mkdir -p "$dir/$layerId"
        echo '1.0' > "$dir/$layerId/VERSION"

        if [ ! -s "$dir/$layerId/json" ]; then
            local parentJson="$(printf ', parent: "%s"' "$parentId")"
            local addJson="$(printf '{ id: "%s"%s }' "$layerId" "${parentId:+$parentJson}")"
            # this starter JSON is taken directly from Docker's own "docker save" output for unimportant layers
            jq "$addJson + ." > "$dir/$layerId/json" <<- 'EOJSON'
                {
                    "created": "0001-01-01T00:00:00Z",
                    "container_config": {
                        "Hostname": "",
                        "Domainname": "",
                        "User": "",
                        "AttachStdin": false,
                        "AttachStdout": false,
                        "AttachStderr": false,
                        "Tty": false,
                        "OpenStdin": false,
                        "StdinOnce": false,
                        "Env": null,
                        "Cmd": null,
                        "Image": "",
                        "Volumes": null,
                        "WorkingDir": "",
                        "Entrypoint": null,
                        "OnBuild": null,
                        "Labels": null
                    }
                }
            EOJSON
        fi

        case "$layerMediaType" in
            application/vnd.docker.image.rootfs.diff.tar.gzip)
                local layerTar="$layerId/layer.tar"
                layerFiles=("${layerFiles[@]}" "$layerTar")
                # TODO figure out why "-C -" doesn't work here
                # "curl: (33) HTTP server doesn't seem to support byte ranges. Cannot resume."
                # "HTTP/1.1 416 Requested Range Not Satisfiable"
                if [ -f "$dir/$layerTar" ]; then
                    # TODO hackpatch for no -C support :'(
                    echo "skipping existing ${layerId:0:12}"
                    continue
                fi
                local token="$(curl -fsSL "$authBase/token?service=$authService&scope=repository:$image:pull" | jq --raw-output '.token')"
                fetch_blob "$token" "$image" "$layerDigest" "$dir/$layerTar" --progress
                ;;

            *)
                echo >&2 "error: unknown layer mediaType ($imageIdentifier, $layerDigest): '$layerMediaType'"
                exit 1
                ;;
        esac
    done

    # change "$imageId" to be the ID of the last layer we added (needed for old-style "repositories" file which is created later -- specifically for older Docker daemons)
    imageId="$layerId"

    # munge the top layer image manifest to have the appropriate image configuration for older daemons
    local imageOldConfig="$(jq --raw-output --compact-output '{ id: .id } + if .parent then { parent: .parent } else {} end' "$dir/$imageId/json")"
    jq --raw-output "$imageOldConfig + del(.history, .rootfs)" "$dir/$configFile" > "$dir/$imageId/json"

    local manifestJsonEntry="$(
        echo '{}' | jq --raw-output '. + {
            Config: "'"$configFile"'",
            RepoTags: ["'"${image#library\/}:$tag"'"],
            Layers: '"$(echo '[]' | jq --raw-output ".$(for layerFile in "${layerFiles[@]}"; do echo " + [ \"$layerFile\" ]"; done)")"'
        }'
    )"
    manifestJsonEntries=("${manifestJsonEntries[@]}" "$manifestJsonEntry")
}

while [ $# -gt 0 ]; do
    imageTag="$1"
    shift
    image="${imageTag%%[:@]*}"
    imageTag="${imageTag#*:}"
    digest="${imageTag##*@}"
    tag="${imageTag%%@*}"

    # add prefix library if passed official image
    if [[ "$image" != *"/"* ]]; then
        image="library/$image"
    fi

    imageFile="${image//\//_}" # "/" can't be in filenames :)

    token="$(curl -fsSL "$authBase/token?service=$authService&scope=repository:$image:pull" | jq --raw-output '.token')"

    manifestJson="$(
        curl -fsSL \
            -H "Authorization: Bearer $token" \
            -H 'Accept: application/vnd.docker.distribution.manifest.v2+json' \
            -H 'Accept: application/vnd.docker.distribution.manifest.list.v2+json' \
            -H 'Accept: application/vnd.docker.distribution.manifest.v1+json' \
            "$registryBase/v2/$image/manifests/$digest"
    )"
    if [ "${manifestJson:0:1}" != '{' ]; then
        echo >&2 "error: /v2/$image/manifests/$digest returned something unexpected:"
        echo >&2 "  $manifestJson"
        exit 1
    fi

    imageIdentifier="$image:$tag@$digest"

    schemaVersion="$(echo "$manifestJson" | jq --raw-output '.schemaVersion')"
    case "$schemaVersion" in
        2)
            mediaType="$(echo "$manifestJson" | jq --raw-output '.mediaType')"

            case "$mediaType" in
                application/vnd.docker.distribution.manifest.v2+json)
                    handle_single_manifest_v2 "$manifestJson"
                    ;;
                application/vnd.docker.distribution.manifest.list.v2+json)
                    layersFs="$(echo "$manifestJson" | jq --raw-output --compact-output '.manifests[]')"
                    IFS="$newlineIFS"
                    layers=($layersFs)
                    unset IFS

                    found=""
                    # parse first level multi-arch manifest
                    for i in "${!layers[@]}"; do
                        layerMeta="${layers[$i]}"
                        maniArch="$(echo "$layerMeta" | jq --raw-output '.platform.architecture')"
                        if [ "$maniArch" = "$(go env GOARCH)" ]; then
                            digest="$(echo "$layerMeta" | jq --raw-output '.digest')"
                            # get second level single manifest
                            submanifestJson="$(
                                curl -fsSL \
                                    -H "Authorization: Bearer $token" \
                                    -H 'Accept: application/vnd.docker.distribution.manifest.v2+json' \
                                    -H 'Accept: application/vnd.docker.distribution.manifest.list.v2+json' \
                                    -H 'Accept: application/vnd.docker.distribution.manifest.v1+json' \
                                    "$registryBase/v2/$image/manifests/$digest"
                            )"
                            handle_single_manifest_v2 "$submanifestJson"
                            found="found"
                            break
                        fi
                    done
                    if [ -z "$found" ]; then
                        echo >&2 "error: manifest for $maniArch is not found"
                        exit 1
                    fi
                    ;;
                *)
                    echo >&2 "error: unknown manifest mediaType ($imageIdentifier): '$mediaType'"
                    exit 1
                    ;;
            esac
            ;;

        1)
            if [ -z "$doNotGenerateManifestJson" ]; then
                echo >&2 "warning: '$imageIdentifier' uses schemaVersion '$schemaVersion'"
                echo >&2 "  this script cannot (currently) recreate the 'image config' to put in a 'manifest.json' (thus any schemaVersion 2+ images will be imported in the old way, and their 'docker history' will suffer)"
                echo >&2
                doNotGenerateManifestJson=1
            fi

            layersFs="$(echo "$manifestJson" | jq --raw-output '.fsLayers | .[] | .blobSum')"
            IFS="$newlineIFS"
            layers=($layersFs)
            unset IFS

            history="$(echo "$manifestJson" | jq '.history | [.[] | .v1Compatibility]')"
            imageId="$(echo "$history" | jq --raw-output '.[0]' | jq --raw-output '.id')"

            echo "Downloading '$imageIdentifier' (${#layers[@]} layers)..."
            for i in "${!layers[@]}"; do
                imageJson="$(echo "$history" | jq --raw-output ".[${i}]")"
                layerId="$(echo "$imageJson" | jq --raw-output '.id')"
                imageLayer="${layers[$i]}"

                mkdir -p "$dir/$layerId"
                echo '1.0' > "$dir/$layerId/VERSION"

                echo "$imageJson" > "$dir/$layerId/json"

                # TODO figure out why "-C -" doesn't work here
                # "curl: (33) HTTP server doesn't seem to support byte ranges. Cannot resume."
                # "HTTP/1.1 416 Requested Range Not Satisfiable"
                if [ -f "$dir/$layerId/layer.tar" ]; then
                    # TODO hackpatch for no -C support :'(
                    echo "skipping existing ${layerId:0:12}"
                    continue
                fi
                token="$(curl -fsSL "$authBase/token?service=$authService&scope=repository:$image:pull" | jq --raw-output '.token')"
                fetch_blob "$token" "$image" "$imageLayer" "$dir/$layerId/layer.tar" --progress
            done
            ;;

        *)
            echo >&2 "error: unknown manifest schemaVersion ($imageIdentifier): '$schemaVersion'"
            exit 1
            ;;
    esac

    echo

    if [ -s "$dir/tags-$imageFile.tmp" ]; then
        echo -n ', ' >> "$dir/tags-$imageFile.tmp"
    else
        images=("${images[@]}" "$image")
    fi
    echo -n '"'"$tag"'": "'"$imageId"'"' >> "$dir/tags-$imageFile.tmp"
done

echo -n '{' > "$dir/repositories"
firstImage=1
for image in "${images[@]}"; do
    imageFile="${image//\//_}" # "/" can't be in filenames :)
    image="${image#library\/}"

    [ "$firstImage" ] || echo -n ',' >> "$dir/repositories"
    firstImage=
    echo -n $'\n\t' >> "$dir/repositories"
    echo -n '"'"$image"'": { '"$(cat "$dir/tags-$imageFile.tmp")"' }' >> "$dir/repositories"
done
echo -n $'\n}\n' >> "$dir/repositories"

rm -f "$dir"/tags-*.tmp

if [ -z "$doNotGenerateManifestJson" ] && [ "${#manifestJsonEntries[@]}" -gt 0 ]; then
    echo '[]' | jq --raw-output ".$(for entry in "${manifestJsonEntries[@]}"; do echo " + [ $entry ]"; done)" > "$dir/manifest.json"
else
    rm -f "$dir/manifest.json"
fi

echo "Download of images into '$dir' complete."
echo "Use something like the following to load the result into a Docker daemon:"
echo "  tar -cC '$dir' . | docker load"
```
