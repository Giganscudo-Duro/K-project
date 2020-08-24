
# 参考URL

- [postgres - dockerhub](https://hub.docker.com/_/postgres)
- [Docker で作る postgres 環境 - Crudzoo](https://crudzoo.com/blog/docker-postgres)


- [Golang で PostgreSQL のデータを読む (Read) - Qiita](https://qiita.com/ekzemplaro/items/5d804a60a11ce046344a)
- [Golang で PostgreSQL のデータを作成 (Create) - Qiita](https://qiita.com/ekzemplaro/items/54a83c130a5b62e2e88b)
- [【Golang】Go言語からPostgreSQLを使う【sql, lib/pq】 - くどはむと猫の窓](http://kudohamu.hatenablog.com/entry/2014/11/29/121328)

- [postgreSQLテーブルからjson形式でSELECTする小ネタ - Solutionware開発ブログ](https://solutionware.jp/blog/2016/06/23/postgresql%E3%83%86%E3%83%BC%E3%83%96%E3%83%AB%E3%81%8B%E3%82%89json%E5%BD%A2%E5%BC%8F%E3%81%A7select%E3%81%99%E3%82%8B%E5%B0%8F%E3%83%8D%E3%82%BF/)


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


必要なパッケージを予め導入しておく。
```sh
# apt install vim
# apt install docker.io
# apt install golang
$ go get github.com/lib/pq
```


今回題材として扱うのは、以下のテーブル。  
意味は特に無いね。てきとー。

テーブル：contracts
| ID  | name       | description      | product   | Access |
|-----|------------|------------------|-----------|--------|
| 001 | かなまる   | 男性、大分出身   | PS3       | full   |
| 002 | まつむら   | 男性、福岡出身   | Xpox360   | full   |
| 003 | こばやかわ | 女性、宮崎出身   | PSP       | DLonly |
| 004 | もりした   | 女性、熊本出身   | 3DS       | ULonly |



## DB を作成する

ひとまず参考サイトを参考にソースコードを作成。

```go
package main

import (
    "fmt"
    "database/sql"
    _ "github.com/lib/pq"
)

// ----------------------------------------------------------------
func main() {
    fmt.Println ("*** 開始 ***")

    dict_aa := data_prepare_proc ()
        user := "kanamaru"
    dbname := "kana-db"
        password := "password"

    str_connect := "user=" + user + " dbname=" + dbname + " password=" + password + " sslmode=disable"
    db, err := sql.Open("postgres", str_connect)
    defer db.Close ()

    _, err = db.Exec ("drop table contracts")
    if err != nil {
        fmt.Println (err)
        }

    sql_str := "create table contracts (id varchar(10), name varchar(20), description varchar(20),product varchar(10))"
    fmt.Println (sql_str)

    _, err = db.Exec (sql_str)
    if err != nil {
        fmt.Println (err)
        }

    for key,_ := range dict_aa {
        name := dict_aa[key]["name"].(string)
        description := dict_aa[key]["description"].(string)
        product := dict_aa[key]["product"].(string)
        sql_str :="insert into contracts values ('" + key + "','" + name + "','" + description + "','" + product + "')"
        fmt.Println (sql_str)
        _, err = db.Exec (sql_str)
        if err != nil {
            fmt.Println (err)
            }
        }

    fmt.Println ("*** 終了 ***")
}

// ----------------------------------------------------------------
func data_prepare_proc () map[string](map[string]interface{}) {
    dict_aa := make (map[string](map[string]interface{}))

    dict_aa["001"] = unit_gen_proc ("かなまる", "男性、大分出身", "PS3")
    dict_aa["002"] = unit_gen_proc ("まつむら", "男性、福岡出身", "Xbox360")
    dict_aa["003"] = unit_gen_proc ("こばやかわ", "女性、宮崎出身", "PSP")
    dict_aa["004"] = unit_gen_proc ("もりした", "女性、熊本出身", "3DS")

    return (dict_aa)
}

// ----------------------------------------------------------------
func unit_gen_proc (name string, description string, product string) map[string]interface{} {
    unit_aa := make (map[string]interface{})
    unit_aa["name"] = name
    unit_aa["description"] = description
    unit_aa["product"] = product

    return (unit_aa)
}

// ----------------------------------------------------------------
```



<details><summary>実行結果</summary><div>

```sh
$ go run ./create_DB.go
*** 開始 ***
pq: table "contracts" does not exist
create table contracts (id varchar(10), name varchar(20), description varchar(20),product varchar(10))
insert into contracts values ('001','かなまる','男性、大分出身','PS3')
insert into contracts values ('002','まつむら','男性、福岡出身','Xbox360')
insert into contracts values ('003','こばやかわ','女性、宮崎出身','PSP')
insert into contracts values ('004','もりした','女性、熊本出身','3DS')
*** 終了 ***
```
</div></details>






## DB を読み出す



ひとまず参考サイトを参考にソースコードを作成。


```go
package main

import (
    "fmt"
    "database/sql"
    _ "github.com/lib/pq"
    "os"
)

// ----------------------------------------------------------------
func main() {
    fmt.Fprintln (os.Stderr,"*** 開始 ***")

    user := "kanamaru"
    dbname := "kana-db"
    password := "password"

    //db, err := sql.Open("postgres", "user=scott dbname=city password=tiger123 sslmode=disable")
    db, err := sql.Open("postgres", "user=" + user + " dbname=" + dbname + " password=" + password + " sslmode=disable")
    defer db.Close()

    sql_str := "select id,name,description,product from contracts order by id"

    rows, err := db.Query(sql_str)
    if err != nil {
        fmt.Println(err)
        }
    defer rows.Close()

    for rows.Next() {
        var id string
        var name string
        var description string
        var product string
        if err := rows.Scan(&id,&name,&description,&product); err != nil {
            fmt.Println(err)
        }
        fmt.Printf ("%s\t%s\t%s\t%s\n",id, name, description, product)
    }

    if err := rows.Err(); err != nil {
        fmt.Println(err)
        }

    fmt.Fprintln (os.Stderr,"*** 終了 ***")
}

// ----------------------------------------------------------------
```





<details><summary>実行結果</summary><div>

```sh
$ go run ./read_DB.go
*** 開始 ***
001     かなまる        男性、大分出身  PS3
002     まつむら        男性、福岡出身  Xbox360
003     こばやかわ      女性、宮崎出身  PSP
004     もりした        女性、熊本出身  3DS
*** 終了 ***
```
</div></details>

まぁ一応呼び出せた。



# PostgresSQL からテーブルを読み出し、JSON 形式にする


参考サイト「[postgreSQLテーブルからjson形式でSELECTする小ネタ - Solutionware開発ブログ](https://solutionware.jp/blog/2016/06/23/postgresql%E3%83%86%E3%83%BC%E3%83%96%E3%83%AB%E3%81%8B%E3%82%89json%E5%BD%A2%E5%BC%8F%E3%81%A7select%E3%81%99%E3%82%8B%E5%B0%8F%E3%83%8D%E3%82%BF/)」によると、以下の書き方だけでOKらしい。

```
select to_json(テーブル名) from テーブル名
```







