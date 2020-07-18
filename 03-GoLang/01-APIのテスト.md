# 参考URL
- はじめてのGo言語 HTTP通信（ http://cuto.unirita.co.jp/gostudy/post/http/ ）
- gormとgo-json-restを使ってDBからのデータを返すAPIサーバを作る（ https://qiita.com/hirokiseiya/items/8a2c9d6f6e0fb5db329f ）
- Goでhttpリクエストを送信する方法 （ https://qiita.com/taizo/items/c397dbfed7215969b0a5 ）
- Go言語のHTTPサーバのテスト事始め（ https://qiita.com/theoden9014/items/ac8763381758148e8ce5 ）
- Golangのtestify/assert 使えそうな関数まとめ（ https://qiita.com/JpnLavender/items/21b4574a7513472903ea ）
- curlコマンドでapiを叩く（https://qiita.com/bunty/items/758425773b2239feb9a7 ）




# とりあえずお勉強

## 必要なパッケージをインストール
```
$ go get github.com/jinzhu/gorm
$ go get github.com/ant0ine/go-json-rest/rest
```


## 勉強用のソースコード


用意したコード
```go
package main

import (
    "net/http"
    "github.com/labstack/echo"
)

const helloMessage = "Hello, World!"

func main() {
    router := NewRouter()

    router.Start(":8080")
}

func NewRouter() *echo.Echo {
    e := echo.New()

    e.GET("/hello", helloHandler)

    return e
}

func helloHandler(c echo.Context) error {
    return c.String(http.StatusOK, helloMessage)
}
```

この子を実行してみると...
```sh
$ go run main.go

   ____    __
  / __/___/ /  ___
 / _// __/ _ \/ _ \
/___/\__/_//_/\___/ v4.1.16
High performance, minimalist Go web framework
https://echo.labstack.com
____________________________________O/_______
                                    O\
⇨ http server started on [::]:8080
```

そして、上記について `curl` を叩いてみると...
```sh
$ curl -v http://localhost:8080/hello
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 8080 (#0)
> GET /hello HTTP/1.1
> Host: localhost:8080
> User-Agent: curl/7.58.0
> Accept: */*
>
< HTTP/1.1 200 OK
< Content-Type: text/plain; charset=UTF-8
< Date: Mon, 08 Jun 2020 20:54:46 GMT
< Content-Length: 13
<
* Connection #0 to host localhost left intact
Hello, World!
```

まぁこんな感じで、`http://localhost:8080/hello` にアクセスすると、文字列が返ってくる。
動作確認が完了したら `Ctrl-C` でとりあえずサーバを止める。


上記に対して、テストするため `net/http/httptest` なるものを使ってみる。  
基本的な使い方は、テストしたいハンドラ関数を `ServeHTTP(w ResponseWriter, r *Request)` を使って呼び出すだけ。  
コレによって、実際にサーバを立ち上げること無くリクエストをシミュレートすることができるようになっている。  
説明をメモしておくと、以下のようになっているらしい。  
`httptest.NewRequest(method, target string, body io.Reader)` で、クライアント側をシミュレート。  
`httptest.NewRecorder()` で、レスポンスを記録するレコーダーを生成。  

テストコード
```go
package main

import (
    "fmt"
    "net/http"
    "net/http/httptest"
    "testing"
    "github.com/stretchr/testify/assert"
)

func TestHelloHandler1(t *testing.T) {
    router := NewRouter()

    // クライアント側をシミュレート
    // method -> メソッドとして "GET" を指定
    // target -> API の "/hello" を指定
    // body   -> 今回は何も指定しない
    req := httptest.NewRequest("GET", "/hello", nil)

    // 独自ヘッダを追加する場合は、こんな感じで追加する
    // req.Header.Set("Authorization", "Bearer access-token")

    // レスポンスを記録するレコーダを生成
    rec := httptest.NewRecorder()

    // ServeHTTP(w ResponseWriter, r *Request) という形式で呼び出し
    router.ServeHTTP(rec, req)

    // 内容確認用
    fmt.Println("DEBUG: rec.Code =", rec.Code)
    fmt.Println("DEBUG: rec.Body.String() =", rec.Body.String())

    // 検証：rec オブジェクトについて、その内容を比較
    assert.Equal(t, http.StatusOK, rec.Code)
    assert.Equal(t, "Hello, World!", rec.Body.String())
}


func TestHelloHandler2(t *testing.T) {
    router := NewRouter()

    req := httptest.NewRequest("GET", "/hello", nil)
    rec := httptest.NewRecorder()
    router.ServeHTTP(rec, req)

    // 検証 rec オブジェクトについて、その内容を比較
    // 敢えて、エラーになるよう文字列を比較する
    assert.Equal(t, http.StatusOK, rec.Code)
    assert.Equal(t, "Hello, KANAMARU", rec.Body.String())
}
```


実際に実行してみると...

```sh
$ go test -v
=== RUN   TestHelloHandler1
-----------------------------------------------
DEBUG: req = &{GET /hello HTTP/1.1 1 1 map[] {} <nil> 0 [] false example.com map[] map[] <nil> map[] 192.0.2.1:1234 /hello <nil> <nil> <nil> <nil>}
DEBUG: rec = &{200 map[Content-Type:[text/plain; charset=UTF-8]] Hello, World! false <nil> map[Content-Type:[text/plain; charset=UTF-8]] true}
DEBUG: rec.Code = 200
DEBUG: rec.Body.String() = Hello, World!
-----------------------------------------------
--- PASS: TestHelloHandler1 (0.00s)
=== RUN   TestHelloHandler2
--- FAIL: TestHelloHandler2 (0.00s)
        main_test.go:71:
                        Error Trace:    main_test.go:71
                        Error:          Not equal:
                                        expected: "Hello, KANAMARU"
                                        actual  : "Hello, World!"

                                        Diff:
                                        --- Expected
                                        +++ Actual
                                        @@ -1 +1 @@
                                        -Hello, KANAMARU
                                        +Hello, World!
                        Test:           TestHelloHandler2
FAIL
exit status 1
FAIL    _/home/kanamaru/01-study-go-API 0.011s
```



