
# 参考URL

- [postgres - dockerhub](https://hub.docker.com/_/postgres)
- [Docker で作る postgres 環境 - Crudzoo](https://crudzoo.com/blog/docker-postgres)


- [Golang で PostgreSQL のデータを読む (Read) - Qiita](https://qiita.com/ekzemplaro/items/5d804a60a11ce046344a)
- [Golang で PostgreSQL のデータを作成 (Create) - Qiita](https://qiita.com/ekzemplaro/items/54a83c130a5b62e2e88b)
- [【Golang】Go言語からPostgreSQLを使う【sql, lib/pq】 - くどはむと猫の窓](http://kudohamu.hatenablog.com/entry/2014/11/29/121328)



# postgreSQL のコンテナを起動

基本的に以下のコマンドを実行すれば良い


```sh
# docker run -d \
    --name kana-postgres \
    -e POSTGRES_USER=kanamaru \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=kana-db \
    postgres
```

用意されてる環境変数は以下の通り
| 環境変数                  | 備考 |
|---------------------------|------|
| POSTGRES_USER             | DB を利用するユーパーユーザを設定する。設定しなかった場合「postgres」が設定される         |
| POSTGRES_PASSWORD         | スーパーユーザが DB にアクセスする際のパスワードを設定する         |
| POSTGRES_DB               | デフォルトのデータベース名を設定する。設定しなかった場合、「POSTGRES_USER」と同じ値が設定される |
| POSTGRES_INITDB_ARGS      |          |
| POSTGRES_INITDB_WALDIR    |          |
| POSTGRES_HOST_AUTH_METHOD |          |
| PGDATA                    | データベースを差k末井するディレクトリを設定する。設定しなかった場合 `/var/lib/postgresql/data`になる         |





















