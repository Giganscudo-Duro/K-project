# go 言語での mock

使うのは以下の2パターンのよう。

- gomock と mockgen の組み合わせ
- testify/mock



# 学習環境
VM番号は 153
OS は Ubuntu18.04






# 最新のgoをインストール












# gomock と mockgen の組み合わせ

## 参考 URL
https://qiita.com/tenntenn/items/24fc34ec0c31f6474e6d

## インストール方法
以下のコマンドを実行。
```sh
# apt install golang
# go get github.com/golang/mock/gomock
# go get github.com/golang/mock/mockgen
```











# testify/mock


## 参考 URL
https://qiita.com/takeshi_miyajim/items/d2fe1ed3c2e85b014b02
https://www.yoheim.net/blog.php?q=20170903
## インストール方法
以下のコマンドを実行。
```sh
# apt install golang
# go get github.com/stretchr/testify
```


## 前提条件
テストする際は mock に置き換えられるようにコードを実装しておく必要がある。

ファイルの命名規則があり、テスト用のコードは「XXXXX_test.go」とする必要がある。
（逆に言うと、XXXX_test.go は `go run` で実行できないようになっている）





## 利用方法チュートリアル
実例を用いてテストを実行してみる。
参考URL：https://qiita.com/takeshi_miyajim/items/d2fe1ed3c2e85b014b02


テストする際の順番としては以下の通り。
(TDD だと、テストが最初だろうね)
1. テスト用のディレクトリ `go-test` を作成する
2. 上記ディレクトリに、テスト対象となる `main.go` を作成する
3. 上記ディレクトリに、テストコード `main_test.go` を作成する
4. 上記ディレクトリで、コマンド `#go test` を実行する。




今回テストする対象は、以下。
```go
package main
import (
    "fmt"
)

// お天気クライアントのinterface
type WeatherClient interface {
    RequestWeather() string
}

// お天気クライアントの実態の構造体
type WeatherClientImpl struct{}

// お天気をリクエストする関数
func (c WeatherClientImpl) RequestWeather() string {
    fmt.Println("DEBUG: Start RequestWeather Func")
    fmt.Println("DEBUG:    外部サイトに天気を確認する処理を実装予定")
    fmt.Println("DEBUG:    今回は問答無用で「晴れ」を返す")
    return "晴れ"
}

// お天気を扱うサービスの構造体(interfaceの実態)
type WeatherService struct {
    client WeatherClient
}

// お天気取得関数
func (w WeatherService) GetWeather() string {
    fmt.Println("DEBUG: Start GetWeather Func")
    return w.client.RequestWeather()
}

func main() {
    fmt.Println("DEBUG: Start main Function")
    weatherClient := WeatherClientImpl{}
    weatherService := WeatherService{client: weatherClient}
    weather := weatherService.GetWeather()
    fmt.Printf("天気は「%s」です\n", weather)
}
```


上記を実際に実行してみると
```sh
# go run main.go
-----------------------------------------------------------------------
DEBUG: Start main Function
DEBUG: Start GetWeather Func
DEBUG: Start RequestWeather Func
DEBUG:    外部サイトに天気を確認する処理を実装予定
DEBUG:    今回は問答無用で「晴れ」を返す
天気は「晴れ」です
```


上記について、まだ処理が実装できていない `RequestWeather` を Mock 化し、それ以外の処理が正しく動作しているかを確認する。

テスト用のコードは以下。

```go
package main

import (
    "fmt"
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

// Mock (今回の場合は TokyoWeatherClient の Mock)
type weatherClientMock struct {
    mock.Mock
}


// Mock 関数定義
func (mock *weatherClientMock) RequestWeather() string {
    fmt.Println("TEST: Mock 実行")

    // 呼び出し
    result := mock.Called()

    // モックの返却値 Returnの引数を返却する
    return result.String(0)
}


// くもりの時のテスト
func TestRequestWeather1(t *testing.T) {
    assert := assert.New(t)

    // モック準備
    weatherClientMock := new(weatherClientMock)

    // 今回のテストでは、Mock の戻り値として「くもり」を指定している
    weatherClientMock.On("RequestWeather").Return("くもり")

    // テスト実行
    weatherService := WeatherService{client: weatherClientMock}
    weather := weatherService.GetWeather()

    // 検証
    // 天気サービスが「くもり」を受け取って処理しているかを検証させる
    assert.Equal(weather, "くもり")
}


// 雨の時のテスト
func TestRequestWeather2(t *testing.T) {
    assert := assert.New(t)

    // モック準備
    weatherClientMock := new(weatherClientMock)

    // 今回のテストでは、Mock の戻り値として「雨」を指定している
    weatherClientMock.On("RequestWeather").Return("雨")

    // テスト実行
    weatherService := WeatherService{client: weatherClientMock}
    weather := weatherService.GetWeather()

    // 検証
    // 天気サービスが「雨」を受け取って処理しているかを検証させる
    assert.Equal(weather, "雨")
}



// 晴れの時のテスト(NG Pattern)
// func TestRequestWeather3(t *testing.T) {
//     assert := assert.New(t)
//
//     // モック準備
//     weatherClientMock := new(weatherClientMock)
//
//     // 今回のテストでは、Mock の戻り値として「雨」を指定している
//     weatherClientMock.On("RequestWeather").Return("雨")
//
//     // テスト実行
//     weatherService := WeatherService{client: weatherClientMock}
//     weather := weatherService.GetWeather()
//
//     // 検証
//     // 天気サービスが「晴れ」を受け取って処理しているかを検証させる
//     assert.Equal(weather, "晴れ")
// }
```


作成したテストコードは `go test` で実行することができる。
実際に実行した場合、以下が出力される。

```sh
# go test
-----------------------------------------------------------------------
DEBUG: Start GetWeather Func
TEST: Mock 実行
DEBUG: Start GetWeather Func
TEST: Mock 実行
PASS
ok      _/home/kanamaru/golang/testify  0.005s
```

仮に「NGとなってしまうテスト」が含まれていた場合も確認する。
テストコード中の `TestRequestWeather3` のコメントアウトを外す。
コレは、実行して「晴れ」が返されることを期待しているが、Mock 内で「雨」を返すよう定義している。

```sh
# go test
-----------------------------------------------------------------------
DEBUG: Start GetWeather Func
TEST: Mock 実行
DEBUG: Start GetWeather Func
TEST: Mock 実行
DEBUG: Start GetWeather Func
TEST: Mock 実行
--- FAIL: TestRequestWeather3 (0.00s)
        main_test.go:85:
                        Error Trace:    main_test.go:85
                        Error:          Not equal:
                                        expected: "雨"
                                        actual  : "晴れ"

                                        Diff:
                                        --- Expected
                                        +++ Actual
                                        @@ -1 +1 @@
                                        -雨
                                        +晴れ
                        Test:           TestRequestWeather3
FAIL
exit status 1
FAIL    _/home/kanamaru/golang/testify  0.005s
```

実際に実行すると、上記のように「どこで予期せぬ挙動をとったか」、「期待していた値は何か」、「実際に返された値は何か」、「どのテストケースでそれが起きたか」を報告してくれる。







# ginkgo & gomega


## インストール方法
参考URL：https://onsi.github.io/ginkgo/
```sh
# go get github.com/onsi/ginkgo/ginkgo
# go get github.com/onsi/gomega/...
```
もしくは
```sh
# apt install golang-ginkgo-dev
```
(家の環境だと `apt install` でなければインストールできなんだ...)






## 利用方法チュートリアル


テストする際の順番としては以下の通り。
(BDD なので、テストファースト)
1. テスト用のディレクトリ `ginkgo` を作成する（任意）
2. パッケージを格納するディレクトリを作成する
3. 上記ディレクトリで、コマンド `# ginkgo bootstrap` を実行し、テストスイートファイルを作成する。
4. 上記ディレクトリで、コマンド `# ginkgo generate [2のディレクトリ名]` を実行し、テストファイルを作成する。
5. 上記ディレクトリ内に、テスト対象とするファイルを作成する


まずはテスト用のディレクトリと、テスト用のフィルを作成する。
```sh
# mkdir Person && cd Person
# ginkgo bootstrap
# ginkgo generate Person
```


とりあえず Person_test.go を実装する

```go
package Person_test

import (
    . "github.com/onsi/ginkgo"
    . "github.com/onsi/gomega"
    "errors"

    // Person.go と同じディレクトリで実行するため、カレントディレクトリをインポート
    . "."
)

var _ = Describe("Person", func() {

    // Nameに関するテスト．文字列は変更できます
    Context("Test for Name", func() {

        /* Person.SetNameメソッドのテスト */
        It("Test for SetName", func() {
            p := &Person{} // 構造体 Person の作成

            p.SetName("Alice") // SetNameメソッドをただ実行している
            // エラーは発生しないため、このテストでは何も検証していない
        })

        /* Person.GetNameメソッドのテスト(正常系) */
        It("Test for GetName (Normal)", func() {
            p := &Person{}
            p.SetName("Bob") // SetName メソッドで name に Bob をセット
            name, err := p.GetName()      // GetName メソッドで name を読み出す
            Expect(err).To(BeNil())       // 期待は、「エラーが発生しない(nil)こと」
            Expect(name).To(Equal("Bob")) // 期待は、「name が Bob であること」
        })
        /* Person.GetNameメソッドのテスト(エラー系) */
        It("Test for GetName (Error)", func() {
            p := &Person{}
            // エラーを期待し、名前をセットしない
            _, err := p.GetName()
            // nameが設定されていないので，エラーが返る
            Expect(err).NotTo(BeNil())                           // 期待は、「エラーが発生していること」
            Expect(err).To(Equal(errors.New("Name is not set"))) // 期待は、「エラー内容が"Name is not set"であること」
        })
    })
})
```



そして、テスト対象となる `Person.go` を作成する
```go
package Person

import "errors"

type Person struct{
    name string
}


// 成功パターン
func (p *Person) GetName() (string, error) {
    if p.name == "" {
        return "", errors.New("Name is not set")
    }
    return p.name, nil
}


// // エラーパターン
// func (p *Person) GetName() (string, error) {
//     if p.name == "" {
//         return "", errors.New("Name is not set")
//     }
//     // 返り値にnilでない値を設定している
//     return p.name, errors.New("No Error")
//     // return p.name, nil
// }


func (p *Person) SetName(in_name string) {
    p.name = in_name
}
```


テストを実際に実行する場合は、以下のコマンドを実行する。
```sh
$ ginkgo -v -cover -coverprofile=./cover.out
```




















