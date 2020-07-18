# Mock or Stub によるテスト


# 概要
go 言語では単体テストを行うための Mock ツールが用意されている。  
しかし Mock を使えば何でもテストできるかと言うとそうではない。  
「mock 化したい外部関数が Interface 型で実装されている」といった条件があるからだ。

最初から Mock を使うという前提で開発を進めていたのならば問題無いが、「Interface 型で実装していない前任者から開発の引き継ぎ」という場面では大いに困ってしまう。  
そこで、他にやり方が無いか、個人的に調べて記録することにした。


# Mock と Stub の違い
どちらも go 言語において、単体テストを行う際に必要になる「都合のいい戻り値を返してくれる外部関数」を実現するための方法。  
基本的に、両方とも単体テスト(Unit Test)で必要となるパーツを擬似的に再現するための仕組みである。

```txt
Q: なぜ擬似的にパーツを再現する必要性があるの？

A: 全てを「本物」でテストしようとすると、全てが揃わないとテストできない可能性があるから。
   例えば時刻を表すオブジェクトのように「状況によって変化するオブジェクト」がテスト対象に絡むと、
   途端にテストしづらくなる。
```


ただし、その使い方というか考え方は異なっていて、の違いは以下の通り。  
参考：[スタブとモックの違い](https://qiita.com/k5trismegistus/items/10ce381d29ab62ca0ea6)  
参考：[stubとmockについて](https://gitpress.io/c/rails_knowlegde/stub_mock)  

- Mock
    - 送信メッセージのテスト（オブジェクトが副作用のあるメッセージを送信する時、適切な引数・回数で送信してるかチェックする）を行う際に利用する
    - Mock を使ったテストのイメージとしては、「テスト対象とするコードが送信するメッセージの受け手を偽物(モック)にすり替えておき、偽物にメッセージの引数や呼び出し回数が想定通りか検証させる」みたいな感じ

- Stub
    - 受信メッセージのテスト（オブジェクトがメッセージを受け取った時、適切な返事をするかをチェックする）を行う際に利用する
    - Stub を使ったテストのイメージとしては、「テスト対象とするコードの中で実行している外部関数を、決まりきった動きしかしない偽物(スタブ)に置き換えて、コードの実装の正しさだけを確認する」みたいな感じ


とりあえず、以下を理解しておけば戦える。

```txt
Q: Mock さんは、テスト中に何をしてるの？

A: テスト対象のコードが、
    特定のテストケースにおいて外部関数を呼び出す時、
   「テスト対象のコードが、適切な引数を添えて呼び出しているか」
   「テスト対象のコードが、適切な回数だけ呼び出しているか」
   をチェックしてくれてる。
   ついでに、期待通りの戻り値も返してくれてる。
```

```txt
Q: Stub さんは、テスト中に何をしてるの？

A: テスト対象のコードが、
    特定のテストケースにおいて外部関数を呼び出す時、
   別に何のチェックもせず、
   「呼び出された外部関数の代わりに期待通りの戻り値を返す」だけをしている。
```




# Go での Mock と Stub 
## Go での Mock
go 言語での Mock ツールを利用する際の条件は以下。

1. 特別なパッケージの導入："github.com/stretchr/testify/mock" のインポートが必要
    - 参考：[GoDoc package mock](https://godoc.org/github.com/stretchr/testify/mock)
    - mock の仕組みを提供しているパッケージで、こいつをインポートしなければ始まらない。

2. 利用時の注意：Mock 化したい外部関数が、実装ファイルの中で Interface 型として実装されている
    - Mock 利用のための条件なので、避けることはできない。
    - もし「開発の引き継ぎ」をするならば、実装された外部関数全ての書き換えが必要になる
 
すっごく乱暴にまとめると、**Mock を使うならば、Mock 専用のパッケージが必要、Mock 前提で実装された関数が必要** という感じ。  
(Interface 型は、Mock のために用意されてるわけではないけど)

で、メリットとデメリットはというと...

- メリット
    - 外部関数を、期待した通りの返り値を返す Mock にできる。
    - 利用条件さえ満たしていれば、とにかく利用がかんたん。（Mockツール側で色々ヤッてくれる）

- デメリット
    - 利用するならば、最初から計画的な設計をしなければならない。
        - Interface を用いて関数（メソッド）が実装されていなければならない
    - 利用不可な状態から、利用可能な状態に改修するのが面倒くさい
        - 利用条件を満たしていない場合、Mock 化したい外部関数自体に大きな改修が必要。
        - 開発の引き継ぎ等の場合、Mock 化したい外部関数自体に大きな改修が必要。

## Go での Stub

Stub を利用する際の条件は以下。

1. 特別なパッケージの導入：不要。
    - 補足事項は特になし。
    - 必要なのは、パッケージ変数という概念だけ。

2. 利用時の注意：Stub 化したい外部関数が、呼び出し元ファイルの中でパッケージ変数に代入して呼び出されている
    - 早い話が、関数ポインタみたいな感じで呼び出されていることが必要。

すっごく乱暴にまとめると、**Mock を使うならば、Stub 前提で呼び出されている処理が必要** という感じ。
(関数ポインタは、Stub のために用意されてるわけではないけど)

で、メリットとデメリットはというと...

- メリット
    - 外部関数を、期待した通りの返り値を返す Stub に置き換えられる
    - 利用条件が Mock と比べてゆるい
        - 外部関数がどんな方式で実装されていても良い
    - 利用不可な状態から、利用可能な状態に改修するのがかんたん
        - 利用条件を満たしていない場合、Stub 化したい外部関数の呼び出し方法を変えるだけで良い。
        - 開発の引き継ぎ等で、実装済みの関数全てを改修する必要はない。
        - これから自分たちが実装する関数側で呼び出し方を変えれば良い

- デメリット
    - 関数ポインタ等の知識が必要（人力で色々やらなければならん）
        - リザーバの概念が入るメソッドを stub 化するならばちょいと工夫がいる（引数が１つ増える、1番目の引数にリザーバを指定する）
    - 他のパッケージから呼び出すことになるパッケージ変数を定義しなければならない（結局グローバル変数を置くようなことなので）
    - Mock みたいに「適切な引数か」、「適切な回数の呼び出しか」はチェックできない
        - 自分で何か仕組みを入れてやらねばならない
        - どうやりゃいいのか、正直知らん


## まとめると...

調べてみた感じだと、こんな感じかね？  
勿論、mock と stub だと、前述の通り使い方が違うから単純に比較することが見当違いなのかもしれんが


- Mock
    - 最初から Mock を用いたテストを想定してるならば。
    - 開発の引き継ぎであっても、十分な開発期間があるならば。
- Stub
    - 開発の引き継ぎ等で、外部関数が Interface で実装されていないならば。
    - 正直な所、グローバル変数を使うことに抵抗がないならば。
    - テスト時の検証要素は減る（テスト対象コードの正しさしかチェックできない）



# 参考URL
- Mock 関係
    - [[Golang]テストで特定の処理をモックにしたい場合のインターフェイスの使い方](https://ken-aio.github.io/post/2019/10/17/go-test-interface/)
    - [Golangでインターフェースを使いコードを疎結合にする](https://dokupe.hatenablog.com/entry/20181208/1544246322)
    - [testify/mockでgolangのテストを書く](https://qiita.com/muroon/items/f8beec802c29e66d1918)
    - [[Go]interfaceを使ったテスト](https://note.com/kltl/n/n6cd49a233513)
    - [testify/mockでgolangのテストを書く](https://qiita.com/muroon/items/f8beec802c29e66d1918)
- Stub 関係
    - [Golangで関数をグローバル変数に代入してテスト時にスタブする](http://matope.hatenablog.com/entry/2014/08/14/111143)
    - [グローバル変数を使ったGo言語のテクニック](https://qiita.com/yoshinori_hisakawa/items/18b42e9fe8569dc185ba)









# 実践（というか実際に使ってみる）

理論だけ勉強してても面白くないので、実際にコードを書いてみる。


用意したのは以下のファイル。
まぁ [Golangで関数をグローバル変数に代入してテスト時にスタブする](http://matope.hatenablog.com/entry/2014/08/14/111143) のコード丸パクリなんだけど。


ファイル構成は以下の通り。
```sh
$ tree
.
├── kana
│   └── kana-time.go
└── main.go
```



`main..go` の実装は以下の通り。
```go
package main

import (
        "fmt"
                "./kana"
)

func main() {
        fmt.Println(Greet("カナ"))
}

func Greet(n string) string {
        t := kana.GetTime()    // ココで現在時刻を取得する外部関数を呼ぶ

        if 6 <= t.Hour() && t.Hour() <=10 {
                return fmt.Sprintf("朝だぞ！ おはよう%s！ 今は%d時ですよ！", n, t.Hour())
        } else if 11 <= t.Hour() && t.Hour() <= 17 {
                return fmt.Sprintf("昼だぞ！ こんにちは%s！ 今は%d時ですよ！", n, t.Hour())
        } else {
                return fmt.Sprintf("夜だぞ！ こんばんは%s！ 今は%d時ですよ！", n, t.Hour())
        }
}
```


`kana-time.go` の実装は以下の通り。
```go
package kana

import (
        "time"
)

func GetTime() time.Time {
    return time.Now()    // ここで現在時刻を生成して、呼び出し元に返す
}
```


このコードでは、`kana-time.go` 内部で呼び出してる `time.Now()` が現在時刻を取得して、`t` に格納している。  
つまり、特定の時刻(朝、昼、晩)に実行しないと、コードが正しく動いているか確認することができない。  
まぁぶっちゃけ、実行結果を制御できない関数ならば、例は何でも良かった。




## Mock の場合

Interface の実装が必要なので、base を元にしてちょっと作り直した。  
参考：[GoDoc mock](https://godoc.org/github.com/stretchr/testify/mock)


ファイル構成は以下の通り。
```sh
$ tree
.
├── kana
│   └── kana-time.go
├── main.go
└── main_test.go

1 directory, 3 files
```


`main..go` の実装は以下の通り。
```go
package main

import (
        "fmt"
        "./kana"
)

type KTime struct {
    kt kana.KTimer
}

func main() {
        k := new(KTime)
        fmt.Println(k.Greet("カナ"))
}

func (k *KTime) Greet(n string) string {
        t := kana.GetTime()    // ココで現在時刻を取得する外部関数を呼ぶ

        if 6 <= t.Hour() && t.Hour() <=10 {
                return fmt.Sprintf("朝だぞ！ おはよう%s！ 今は%d時ですよ！", n, t.Hour())
        } else if 11 <= t.Hour() && t.Hour() <= 17 {
                return fmt.Sprintf("昼だぞ！ こんにちは%s！ 今は%d時ですよ！", n, t.Hour())
        } else {
                return fmt.Sprintf("夜だぞ！ こんばんは%s！ 今は%d時ですよ！", n, t.Hour())
        }
}
```


`kana-time.go` の実装は以下の通り。
```go
package kana

import (
        "time"
)

type KTimer interface {
    GetTime() time.Time
}

func GetTime() time.Time {
    return time.Now()    // ここで現在時刻を生成して、呼び出し元に返す
}
```

Interface の宣言を増やした。
（Interface を宣言し、そこで宣言した関数名で実装すれば、勝手に Interface として認識される）

ちなみに実行すると、こんな感じ。
```sh
$ go run main.go
夜だぞ！ こんばんはカナ！ 今は5時ですよ！
```


とりあえず上記について、以下のテストコードを用意する

```go
package main

import (
    "fmt"
        "testing"
        "./kana"
    "time"
    "github.com/stretchr/testify/assert"
        "github.com/stretchr/testify/mock"
)

// Mock (今回は Interface の KTimer を mock 化する)
type KTimerMock struct {
    mock.Mock  // mock.Mock を埋め込んでおく
}

// Mock として同名のメソッドを定義
func (mock *KTimerMock) GetTime() time.Time {
    fmt.Println("TEST: Mock start")

        // 呼び出し
        // メソッド内 Called メソッドを実行して、result を取得する
        // mock.Called() の実行結果は、「Mock のメソッドの引数のスライス」である
        // スライスってのは要素の集まりで、インデックス番号でその内容に参照できる
        result := mock.Called()

        // Mock の返り値として result の要素を返却する
        // この部分に関しては、ちょこっと使い分けが必要みたい
        // result.Get()         -> インデックス番号で指定された空インタフェースを返り値を返す
        // result.Int()         -> インデックス番号で指定されたint型の返り値を返す。返り値がなかったり、型が合わないとパニックする
        // result.String()      -> インデックス番号で指定されたstring型の返り値を返す。返り値がなかっ たり、型が合わないとパニックする
        // result.Error()       -> インデックス番号で指定されたerror型の返り値を返す。返り値がなかったり、型が合わないとパニックする
        return result.Get(0)
}

const timeformat = "2006-01-02 15:04:06" // timeのフォーマット指定文字列

// 夜のテスト
func TestGreet_1(t *testing.T) {
    assert := assert.New(t)

    morning, _ := time.Parse(timeformat, "2020-08-14 5:10:00")

    // Mock の宣言(というか初期化)
    GetTimeMock := new(KTimerMock)

    // Mock の動作内容について設定
    // On(メソッド名)という形で呼び出し方を指定
    // Return(返り値) という形で返り値を指定
    GetTimeMock.On("GetTime").Return(morning)

    // テスト実行

    // インタフェース経由でメソッドを呼び出す
    aisatsu := GetTimeMock.GetTime()
    // aisatsu := Greet("カナ")

    // 検証
    assert.Equal(aisatsu, "夜だぞ！ こんばんはカナ！ 今は5時ですよ！")
}
```

実行してみると...エラー。
```sh
$ go test
# _/home/kanamaru/99-work/01-getTime/mock
./main_test.go:32:26: cannot use result.Get(0) (type interface {}) as type time.Time in return argument: need type assertion
FAIL    _/home/kanamaru/99-work/01-getTime/mock [build failed]
```

interface 変数について、型のアサーションが必要らしい...。
（手元の本だと「空インタフェース型の変数にはどんな値も代入可能です」ってのを誤解していたみたい）

とりあえず [interface{} な変数を型が決まっている関数の引数にする](https://qiita.com/umanoda/items/07887d33ef1155b26ed2) を参考に解決を図る。

`return result.Get(0).(time.Time)` という具合にかけばOKだったみたい。
ちなみに、今回は違うけど戻り地が2つあるならば、`return ret.Get(0).(*model.User), ret.Error(1)` という具合にすればいいらしい。


そんで、もう一回実行してみると
```sh
TEST: Mock start
--- FAIL: TestGreet_1 (0.00s)
        main_test.go:58:
                        Error Trace:
                        Error:          Not equal:
                                        expected: time.Time(time.Time{wall:0x0, ext:63101819400, loc:(*time.Location)(nil)})
                                        actual  : string("夜だぞ！ こんばんはカナ！ 今は3時ですよ！")
                        Test:           TestGreet_1
FAIL
exit status 1
FAIL    _/home/kanamaru/99-work/01-getTime/mock 0.004s
```

テストコードに書いた `aisatsu := GetTimeMock.GetTime()` が原因。
どうやって注入すればいいのか...。
普通に `aisatsu := Greet("カナ")` 実行すると、現在の時刻が入ってしまう．．．

とりあえず、mock 注入とやらを調べて、書き直してみた。





ちょっと行き詰まった。













https://qiita.com/nnao45/items/b8edaf82ece4f8114ddb














## Stub の場合

パッケージ変数を用いた呼び出しが必要なので、base を元にしてちょっと作り直した。  


ファイル構成は以下の通り。
```sh
$ tree
.
├── kana
│   └── kana-time.go
├── main.go
└── main_test.go

1 directory, 3 files
```


`main..go` の実装は以下の通り。
```go
package main

import (
        "fmt"
                "./kana"
)

func main() {
        fmt.Println(Greet("カナ"))
}

var StubFunc = kana.GetTime

func Greet(n string) string {
        t := StubFunc()    // ココで現在時刻を取得する外部関数を呼ぶ

        if 6 <= t.Hour() && t.Hour() <=10 {
                return fmt.Sprintf("朝だぞ！ おはよう%s！ 今は%d時ですよ！", n, t.Hour())
        } else if 11 <= t.Hour() && t.Hour() <= 17 {
                return fmt.Sprintf("昼だぞ！ こんにちは%s！ 今は%d時ですよ！", n, t.Hour())
        } else {
                return fmt.Sprintf("夜だぞ！ こんばんは%s！ 今は%d時ですよ！", n, t.Hour())
        }
}
```


`kana-time.go` の実装は以下の通りで変更なし
```go
package kana

import (
        "time"
)

type KTimer interface {
    GetTime() time.Time
}

func GetTime() time.Time {
    return time.Now()    // ここで現在時刻を生成して、呼び出し元に返す
}
```


とりあえず上記について、以下のテストコードを用意する
```go
package main

import (
        //"./kana"
        "fmt"
        "testing"
    "time"
    "github.com/stretchr/testify/assert"
)

const timeformat = "2006-01-02 15:04:06" // timeのフォーマット指定文字列

// StubFunc グローバル変数の関数を入れ替える関数
func changeFunc(t time.Time) {
    StubFunc = func() time.Time {
            fmt.Println("DEBUG: start Stub")   // 一応関数が切り替わったことを確認するため、出力
            return t
    }
}

// 夜のテスト
func TestGreet_1(t *testing.T) {
    assert := assert.New(t)

    time, _ := time.Parse(timeformat, "2020-08-14 5:10:00")
    changeFunc(time)

    // テスト実行
    // インタフェース経由でメソッドを呼び出す
    aisatsu := Greet("カナ")

    // 検証
    assert.Equal("夜だぞ！ こんばんはカナ！ 今は4時ですよ！", aisatsu)
}

// 朝のテスト
func TestGreet_2(t *testing.T) {
    assert := assert.New(t)

    time, _ := time.Parse(timeformat, "2020-08-14 9:10:00")
    changeFunc(time)

    // テスト実行
    // インタフェース経由でメソッドを呼び出す
    aisatsu := Greet("カナ")

    // 検証
    assert.Equal("朝だぞ！ おはようカナ！ 今は9時ですよ！", aisatsu)
}

// 昼のテスト
func TestGreet_3(t *testing.T) {
    assert := assert.New(t)

    time, _ := time.Parse(timeformat, "2020-08-14 13:10:00")
    changeFunc(time)

    // テスト実行
    // インタフェース経由でメソッドを呼び出す
    aisatsu := Greet("カナ")

    // 検証
    assert.Equal("昼だぞ！ こんにちはカナ！ 今は13時ですよ！", aisatsu)
}
```

実行してみると、
```sh
$ go test -v
=== RUN   TestGreet_1
DEBUG: start Stub
--- PASS: TestGreet_1 (0.00s)
=== RUN   TestGreet_2
DEBUG: start Stub
--- PASS: TestGreet_2 (0.00s)
=== RUN   TestGreet_3
DEBUG: start Stub
--- PASS: TestGreet_3 (0.00s)
PASS
ok      _/home/kanamaru/99-work/01-getTime/stub 0.004s
```












