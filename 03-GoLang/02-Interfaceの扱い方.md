# インタフェースを使った場合と使わなかった場合

## 参考URL
- [Golangでインターフェースを使いコードを疎結合にする](https://dokupe.hatenablog.com/entry/20181208/1544246322)
- [testify/mockでgolangのテストを書く](https://qiita.com/muroon/items/f8beec802c29e66d1918)

## 比較

とりあえず、「２つの数字を変数として受け取り、返り値として１つの数字を返す」場合を考えてみる

### 試しにかき分けてみる

まずはインタフェースを利用する場合

- sample1.go
```go
package main

import "fmt"

// 演算インタフェース型
type Calculator interface {
    // 関数の定義
    Calculate(a int, b int) int
}

// 足し算型
type Add struct{
    // フィールドは持たせない
}

// 引き算型
type Sub struct{
    // フィールドは持たせない
}

// Add 型に Calculator インタフェースのメソッド Calculate を実装する
func (x Add) Calculate(a int, b int) int {
    // 足し算した結果を返す
        return a + b
}

// Sub 型に Calculator インタフェースのメソッド Calculate を実装する
func (x Sub) Calculate(a int, b int) int {
    // 足し算した結果を返す
        return a - b
}

func main() {
    // Calculator インタフェースを実装した型の変数を宣言
        var add Add
        var sub Sub

    // Calculator インタフェース型の変数を宣言
        var cal Calculator

    // Add 型の値を代入
        cal = add

        // インタフェース経由でメソッドを呼び出す
        fmt.Println("和 = ", cal.Calculate(1, 2))

    // Sub 型の値を代入
        cal = sub

        // インタフェース経由でメソッドを呼び出す
        fmt.Println("差 = ", cal.Calculate(1, 2))
}
```

次に、インタフェースを使わなかった場合


- sample2.go
```go
package main

import "fmt"


// 足し算型
type Add struct{
    // フィールドは持たせない
}

// 引き算型
type Sub struct{
    // フィールドは持たせない
}

// Add 型にメソッド AddNum を実装する
func (x Add) AddNum(a int, b int) int {
    // 足し算した結果を返す
        return a + b
}

// Sub 型にメソッド SubNum を実装する
func (x Sub) SubNum(a int, b int) int {
    // 足し算した結果を返す
        return a - b
}

func main() {
    // 型の変数を宣言
        var add Add
        var sub Sub

        // メソッドを呼び出す
        fmt.Println("和 = ", add.AddNum(1, 2))

        // メソッドを呼び出す
        fmt.Println("差 = ", sub.SubNum(1, 2))
}

```

### Mock を使ったテストコードを書いてみる
書いてみたのは、以下の通り


- sample1_test.go
```go
package main

import (
        "fmt"
        "testing"
        "github.com/stretchr/testify/assert"
        "github.com/stretchr/testify/mock"
)


// Mock (今回は Calculator が該当)
// mock.Mock を埋め込んでおく
type CalculatorMock struct {
    mock.Mock
}


// Mock としてメソッドを定義
func (mock *CalculatorMock) Calculate(a int, b int) int {
    fmt.Println("TEST: Mock start")

        // 呼び出し
        // メソッド内 Called メソッドを実行して、result を取得する
        // mock.Called() の実行結果は、「Mock のメソッドの引数のスライス」である
        // スライスってのは要素の集まりで、インデックス番号でその内容に参照できる
        result := mock.Called()

        // Mock の返り値として result の要素を返却する
        // この部分に関しては、ちょこっと使い分けが必要みたい
        // result.Get()         -> インデックス番号で指定された返り値を返す
        // result.Int()         -> インデックス番号で指定されたint型の返り値を返す。返り値がなかったり、型が合わないとパニックする
        // result.String()      -> インデックス番号で指定されたstring型の返り値を返す。返り値がなかっ たり、方が合わないとパニックする
        // result.Error()       -> インデックス番号で指定されたerror型の返り値を返す。返り値がなかったり、方が合わないとパニックする
        return result.Int(0)
}

// 足し算のテスト
func TestAddCalculator1(t *testing.T) {
    assert := assert.New(t)

        // Mock の宣言(というか初期化)
        CalculatorMock := new(CalculatorMock)

        // Mock の動作内容について設定
        // On(メソッド名)という形で呼び出し方を指定
        // Return(返り値) という形で返り値を指定
        CalculatorMock.On("Calculate").Return(3)

        // テスト実行

    // インタフェース経由でメソッドを呼び出す
    numadd := CalculatorMock.Calculate(1, 2)

        // 検証
        assert.Equal(numadd, 3)
}

// 足し算のテスト
func TestAddCalculator2(t *testing.T) {
    assert := assert.New(t)

        // Mock の宣言(というか初期化)
        CalculatorMock := new(CalculatorMock)

        // Mock の動作内容について設定
        // On(メソッド名)という形で呼び出し方を指定
        // Return(返り値) という形で返り値を指定
    // とりあえず嘘っぱちの返り値を返すよう設定する
        CalculatorMock.On("Calculate").Return(11)

        // テスト実行

    // インタフェース経由でメソッドを呼び出す
    numadd := CalculatorMock.Calculate(1, 2)

        // 検証
    // Mock が嘘っぱちの１１という値を返せば成功
        assert.Equal(numadd, 11)
}

```


### 所感
書いてみて思ったのは、以下。

- 記述の差異
    - Interface 型の宣言を新規に追加する必要がある
    - 宣言した Interface 型メソッドを必ず実装する必要がある
    - 呼び出し方が変わる

Interface を使うことで単体テスト時に Mock を使えるようになるわけだけど、正直それだけのためにわざわざ Interface を実装するというのは変な話。  

一方で便利な点としては、以下がある
- 便利そうな所
    - ファイル内で独自に作成したインタフェースを用いて、コードを実行でき点
        - 早い話、テストのときだけ挙動が異なる実装を用意して、差し替えることができる
    - インタフェースを用意してあげることで、別の型であっても適宜処理が分けられる？
        - 言い表し方が微妙ではあるけど、インタフェースで実装されたメソッドは、呼び出すときの方に応じてその処理内容を変えられるというか...
        - 今回の例だと「Calculator インタフェース」を受け取ることにより、Add 型であろうが、Sub 方であろうが、それぞれの型に応じた処理がなされている
        - だから、掛け算を意味する Mul 型とか、割り算を意味する Div 型とかを追加したとしても、そのメソッドをしっかり実装してあげれば同じ要領で処理を行うことができる

















