# 参考URL

- [GORMでデータベースを操作してみる - Qiita](https://qiita.com/lycoris_r/items/48d341d36147adb8f5cf)
- [【GORM】Go言語でORM触ってみた - Qiita](https://qiita.com/chan-p/items/cf3e007b82cc7fce2d81)
- [Go言語のGORMを使ってみた① - Qiita](https://qiita.com/gorilla0513/items/27cd34433a48fc8b65db)
- [テーブルのカラムの値をnullかゼロ値かを判別する - Qiita](https://qiita.com/taizo/items/3e0b1ca583d8fe2a62a5)
- [素晴らしいGolangようORMライブラリ - GORM](http://gorm.io/ja_JP/)
- [Package sql - golang](https://golang.org/pkg/database/sql/)
- [package sql - GoDoc](https://godoc.org/database/sql)
- [package gorm - GoDoc](https://godoc.org/github.com/jinzhu/gorm)
- [package postgres - GoDoc](https://godoc.org/github.com/jinzhu/gorm/dialects/postgres)



# GORM とは

「Golang の ORM (Object-Relational Mapping)」という意味で、GORM らしい。  
要は、オブジェクト言語からデータベースにデータを渡す際の仲介役 らしい。

正直この存在を知らなかったので、私は `github.com/lib/pq` を使って PostgreSQL の操作を試みてた。  
それぞれに長所と短所があるとは思うが、それはおいおい勉強する。




# 事前準備

必要なパッケージを予め導入しておく。
```sh
# apt install vim
# apt install docker.io
# apt install golang
$ go get github.com/lib/pq
$ go get github.com/jinzhu/gorm
$ go get github.com/jinzhu/gorm/dialects/postgres
```




# postgreSQL のコンテナを起動

基本的に以下のコマンドを実行すれば良い


```sh
# docker run -d \
    --name kana-postgres \
    -e POSTGRES_USER=kanamaru \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=kana-db \
    -p 5432:5432 \
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
| PGDATA                    | データベースを作成するディレクトリを設定する。設定しなかった場合 `/var/lib/postgresql/data`になる         |






# とりあえず Go で PostgreSQL を操作してみる


今回題材として扱うのは、以下のテーブル。  
意味は特に無いね。てきとー。  
主キーは「ID」。

テーブル：contracts
| contract_id | user_name  | description      | product   | access_auth | created_date |
|-------------|------------|------------------|-----------|-------------|--------------|
|   1         | かなまる   | 男性、大分出身   | PS3       | full        | 2018/04/01   |
|   2         | まつむら   | 男性、福岡出身   | Xpox360   | full        | 2020/11/07   |
|   3         | こばやかわ | 女性、宮崎出身   | PSP       | DLonly      | 2019/12/16   |
|   4         | もりした   | 女性、熊本出身   | 3DS       | ULonly      | 2020/06/28   |



## 操作用のデータを作成する


構造体の名称をテーブル名と同じ「Contracts」にする。  
各フィールド変数を、`{変数名} {型名} {gormの定義}` の形式で 定義する。  
公式サイトによると、gorm の定義として、下記のように構造体のタグを設定する事ができる。  
参考：http://gorm.io/ja_JP/docs/models.html


| タグ            | 説明                                                         |
|-----------------|--------------------------------------------------------------|
| PRIMARY_KEY     | カラムを主キーに指定します                                                                    |
| Column          | カラム名を指定します                                                                          |
| Type            | カラムのデータ型を指定します                                                                  |
| Size            | カラムサイズのサイズを指定します。デフォルトは255です                                         |
| UNIQUE          | カラムにユニーク制約を指定します                                                              |
| DEFAULT         | カラムのデフォルト値を指定します                                                              |
| PRECISION       | カラムの精度を指定します                                                                      |
| NOT NULL        | カラムにNOT NULL制約を指定します                                                              |
| AUTO_INCREMENT  | カラムに自動インクリメントかそうでないかを指定します                                          |
| INDEX           | 名前有りか名前無しでインデックスを作成します。同名のインデックスは複合インデックスになります。|
| UNIQUE_INDEX    | INDEXと同様にユニークインデックスを作成します                                                 |
| EMBEDDED        | 埋め込み構造体に設定します                                                                    |
| EMBEDDED_PREFIX | 埋め込み構造体のプレフィックス名を設定します                                                  |
| -               | このフィールドを無視します                                                                    |


あと、変数に NULL が格納されることがある場合、それに対応した変数型を宣言して上げる必要がある。  
詳細は GoDoc 等で `database/sql` を見ればわかる。  
参考：https://godoc.org/database/sql#NullString
- varchar型がNULL　→　sql.NullString型
- timestamp型がNULL　→　pq.NullTime型　



とりあえず書いてみた
```go
package main

import (
    "fmt"
    "time"
    _ "database/sql"
    _ "github.com/jinzhu/gorm"
    - "github.com/jinzhu/gorm/dialects/postgres"
)

//構造体を定義
type Contract struct {
    ID            int         `gorm:"primary_key" "column:contract_id"`
    Name          string      `gorm:"column:user_name"`
    Description   string      `gorm:"column:description"`
    Product       string      `gorm:"column:product"`
    Access        string      `gorm:"column:access_auth"`
    Created_date  time.Time   `gorm:"column:created_date"`
}

func main(){
    fmt.Println("DEBUG: Start main")
    fmt.Println("DEBUG: Finish main")
}
```


## データベースへの接続処理を追加してみる
```go
package main

import (
    "fmt"
    "time"
    _ "database/sql"
    "github.com/jinzhu/gorm"
    _ "github.com/jinzhu/gorm/dialects/postgres"
)

//構造体を定義
type Contract struct {
    ID            int         `gorm:"primary_key" "column:contract_id"`
    Name          string      `gorm:"column:user_name"`
    Description   string      `gorm:"column:description"`
    Product       string      `gorm:"column:product"`
    Access        string      `gorm:"column:access_auth"`
    Created_date  time.Time   `gorm:"column:created_date"`
}

func main(){
    fmt.Println("DEBUG: Start main")

    // データベースへのコネクションを取得する
    //db, err := gorm.Open("postgres", "kanamaru:password@tcp(localhost:5432)/kana-db")
    db, err := gorm.Open("postgres", "host=localhost port=5432 user=kanamaru dbname=kana-db passwo    rd=password sslmode=disable")


    if err != nil {
        fmt.Println("ERROR: Fail -> executing gorm.Open")
        fmt.Println(err)
    }

    // 一通りの処理が終了したらクローズ
    defer db.Close()

    // Contract に従ったテーブル生成(一回実行すれば十分)
    db.AutoMigrate(&Contract{})

    // 作成したテーブルに書き込む情報を設定
    // （挿入したい情報でContract構造体を初期化して、インスタンス化）
    contracts := Contract{
                        ID: 1,
                        Name: "かなまる",
                        Description: "男性、大分出身",
                        Product: "PS3",
                        Access: "full",
                        Created_date: time.Now(),
                    }
    // INSERTを実行
    db.Create(&contracts)

    fmt.Println("DEBUG: Finish main")
}
```

まぁこういった情報は、`pq` 使ってたときと同じか。



実行してみると...

```sh
kanamaru@vm-ubuntu18:~$ go run Create_DB.go
DEBUG: Start main
DEBUG: Finish main
```

まぁ特にエラーもなく終わった。

試しにもう一回実行してみる。

```sh
kanamaru@vm-ubuntu18:~$ go run Create_DB.go
DEBUG: Start main

(/home/kanamaru/Create_DB.go:49)
[2020-08-27 06:38:56]  pq: duplicate key value violates unique constraint "contracts_pkey"
DEBUG: Finish main
```

ほう、重複してると報告が来てるので、確かに情報は登録されたっぽい



### psql コマンドで直接アクセスして、きちんとできたか確認してみる
http://t-ohtsuka.hatenablog.com/entry/2015/07/07/024315
```sh
apt-get install postgresql-client
```
で、確認してみる。
https://www.dbonline.jp/postgresql/

```sh
kanamaru@vm-ubuntu18:~$ psql -d kana-db -U kanamaru -h 127.0.0.1
Password for user kanamaru:
psql (10.14 (Ubuntu 10.14-0ubuntu0.18.04.1), server 12.4 (Debian 12.4-1.pgdg100+1))
WARNING: psql major version 10, server major version 12.
         Some psql features might not work.
Type "help" for help.

kana-db=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges
-----------+----------+----------+------------+------------+-----------------------
 kana-db   | kanamaru | UTF8     | en_US.utf8 | en_US.utf8 |
 postgres  | kanamaru | UTF8     | en_US.utf8 | en_US.utf8 |
 template0 | kanamaru | UTF8     | en_US.utf8 | en_US.utf8 | =c/kanamaru          +
           |          |          |            |            | kanamaru=CTc/kanamaru
 template1 | kanamaru | UTF8     | en_US.utf8 | en_US.utf8 | =c/kanamaru          +
           |          |          |            |            | kanamaru=CTc/kanamaru
(4 rows)

kana-db=# \dt
           List of relations
 Schema |   Name    | Type  |  Owner
--------+-----------+-------+----------
 public | contracts | table | kanamaru
(1 row)

kana-db=# select * from contracts;
 id | user_name |  description   | product | access_auth |         created_date
----+-----------+----------------+---------+-------------+-------------------------------
  1 | かなまる  | 男性、大分出身 | PS3     | full        | 2020-08-26 21:31:12.266413+00
(1 row)

kana-db=#
```

まえに pq で頑張りまくってたときと比べると、かんたんにしっかり登録されてるっぽい。  
gorm ってすごいね。


## テーブル情報を取得してみる

```go
package main

import (
    "fmt"
    "time"
    _ "database/sql"
    "github.com/jinzhu/gorm"
    _ "github.com/jinzhu/gorm/dialects/postgres"
)

//構造体を定義
type Contract struct {
    ID            int         `gorm:"primary_key" "column:contract_id"`
    Name          string      `gorm:"column:user_name"`
    Description   string      `gorm:"column:description"`
    Product       string      `gorm:"column:product"`
    Access        string      `gorm:"column:access_auth"`
    Created_date  time.Time   `gorm:"column:created_date"`
}

func main(){
    fmt.Println("DEBUG: Start main")

    // データベースへのコネクションを取得する
    //db, err := gorm.Open("postgres", "kanamaru:password@tcp(localhost:5432)/kana-db")
    db, err := gorm.Open("postgres", "host=localhost port=5432 user=kanamaru dbname=kana-db passwo    rd=password sslmode=disable")

    if err != nil {
        fmt.Println("ERROR: Fail -> executing gorm.Open")
        fmt.Println(err)
    }

    // 一通りの処理が終了したらクローズ
    defer db.Close()

    // 受け入れ口の作成
    contract := []Contract{}

    // 全てのレコードを取得
    db.Find(&contract)

    //表示
    for _, cont := range contract {
        fmt.Println(cont.ID)
        fmt.Println(cont.Name)
        fmt.Println(cont.Description)
        fmt.Println(cont.Product)
        fmt.Println(cont.Access)
        fmt.Println(cont.Created_date)
    }

    fmt.Println("DEBUG: Finish main")
}
```

実行してみると

```sh
kanamaru@vm-ubuntu18:~$ go run ./Select_DB.go
DEBUG: Start main
1
かなまる
男性、大分出身
PS3
full
2020-08-26 21:31:12.266413 +0000 UTC
DEBUG: Finish main
```


