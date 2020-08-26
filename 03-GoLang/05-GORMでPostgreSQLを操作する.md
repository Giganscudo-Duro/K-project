# 参考URL

- [GORMでデータベースを操作してみる - Qiita](https://qiita.com/lycoris_r/items/48d341d36147adb8f5cf)

























# 参考URL

- [GORMでデータベースを操作してみる - Qiita](https://qiita.com/lycoris_r/items/48d341d36147adb8f5cf)
- [素晴らしいGolangようORMライブラリ - GORM](http://gorm.io/ja_JP/)


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
| ID  | name       | description      | product   | Access | Created_at |
|-----|------------|------------------|-----------|--------|------------|
| 001 | かなまる   | 男性、大分出身   | PS3       | full   | 2018/04/01 |
| 002 | まつむら   | 男性、福岡出身   | Xpox360   | full   | 2020/11/07 |
| 003 | こばやかわ | 女性、宮崎出身   | PSP       | DLonly | 2019/12/16 |
| 004 | もりした   | 女性、熊本出身   | 3DS       | ULonly | 2020/06/28 |



## 操作用のデータを作成する


構造体の名称をテーブル名と同じ「Contracts」にする。  
各フィールド変数を、`{変数名} {型名} {gormの定義}` の形式で 定義する。  
公式サイトによると、gorm の定義として、下記のように構造体のタグを設定する事ができる。  

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



```go
//構造体を定義
type Employee struct {
    EmpNum       int            `gorm:"primary_key" "column:emp_num"`
    EmpName      string         `gorm:"column:emp_name"`
    EmpNameKana  sql.NullString `gorm:"column:emp_name_kana"`
    Age          sql.NullInt64  `gorm:"column:age"`
    HireDate     time.Time      `gorm:"column:hire_date"`
    InsertedDate time.Time      `gorm:"column:inserted_date"`
}
```







