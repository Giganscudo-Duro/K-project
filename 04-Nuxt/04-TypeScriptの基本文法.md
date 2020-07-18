# TypeScript の基本文法

基本と言いつつ、必要となった書き方をタラタラと書き殴っただけ。  
JavaScript との違いも一緒にまとめたいが...ちょっとまだ良くわからんので混ざってるかもしれん。



## デバッグ用のコメントを記述（なにか文字列を記述）
参考にした URL は、以下。
- [TypeScriptでconsole.log()を使うときの便利メソッド - Qiita](https://qiita.com/tonkotsuboy_com/items/7443ffb6351e6bd2526b)
- [console.log()を使うときのおすすめ記述方法 - Qiita](https://qiita.com/tonkotsuboy_com/items/27e20373d4fd16406622)

注意事項としては、以下の２つ
- 対応していないブラウザがある
- ハードコーディングなので、忘れずに消すこと（デバッグレベルの設定とかは...まだ知らん）


まぁとりあえずもっと書き方がわからないうちは、コレをいっぱい挟んで動作を確認していきましょう。  
書き方は以下の通り。
- 記述例
    ```ts
    console.log("文字列")
    ```


## 様々な配列を表示（処理）する場合の記法
参考にした URL は、以下。
- [忘れやすい、複雑なJSONの要素をfor...in分で取り出す方法 - Feel Physics Backyard](https://www.weed.nagoya/entry/2016/05/11/105145)


配列と言っても色々ある。  
例えば、API を叩いた結果として返ってくる JSON とかも表示する必要があるかもしれない。  
そういう時に使う。


- 記述例(showDogList.ts)
    ```ts
    // ただの配列
    var list = ['Taro', 'Bon', 'Kuro', 'RIRI'];
    
    // 連想配列
    var hash = {name: 'RIRI', species: 'dog', sex: 'female'}
    
    // JSON
    var json = {
        Taro: {
            species: 'Beagle',
            sex: 'male'
        },
        Bon: {
            species: 'Beagle',
            sex: 'male'
        },
        Kuro: {
            species: 'mutt',
            sex: 'male'
        },
        RIRI: {
            species: 'mutt',
            sex: 'female'
        }
    };
    
    // 表示させるための記法
    
    console.log("「ただの配列」")
    // 「ただの配列」を表示させる３パターン
    console.log("DEBUG: pattern1")
    for (var i = 0; i < list.length; i++) {
        console.log(list[i])
    }
    
    console.log("DEBUG: pattern2")
    for (var item in list) {
        console.log(item)
    }
    
    console.log("DEBUG: pattern3")
    for (var n in list) {
        console.log(list[n])
    }
    
    console.log("DEBUG: pattern4")
    for (var item of list) {
        console.log(item)
    }
    
    console.log("「連想配列」")
    // 「連想配列」
    for (var key in hash) {
        console.log(key + ': ' + hash[key])
    }
    
    console.log("「JSON」")
    // 「JSON」
    for (var item in json) {
        console.log(item)
    }
    
    for (var item in json) {
        console.log(json[item])
    }
    
    for (var item in json) {
        console.log(item + ': ' + json[item]['species'])
    }
    ```


- 実行結果
    ```sh
    $ tsc showDogList.ts
    $ node showDogList.js
    「ただの配列」
    DEBUG: pattern1
    Taro
    Bon
    Kuro
    RIRI
    DEBUG: pattern2
    0
    1
    2
    3
    DEBUG: pattern3
    Taro
    Bon
    Kuro
    RIRI
    DEBUG: pattern4
    Taro
    Bon
    Kuro
    RIRI
    「連想配列」
    name: RIRI
    species: dog
    sex: female
    「JSON」
    Taro
    Bon
    Kuro
    RIRI
    { species: 'Beagle', sex: 'male' }
    { species: 'Beagle', sex: 'male' }
    { species: 'mutt', sex: 'male' }
    { species: 'mutt', sex: 'female' }
    Taro: Beagle
    Bon: Beagle
    Kuro: mutt
    RIRI: mutt
    ```





















































## API を叩く

参考にした URL は、以下。
- [【Ajax】axiosを使って簡単にHTTP通信 - Willstyle](https://www.willstyle.co.jp/blog/2751/)
- [2010年代も終わるのでaxiosについて確認しておきたい - Qiita](https://qiita.com/Ryusou/items/8b7d239819e3a3874638)
- [HTTPリクエストを型安全にする手法とNuxt TSでの実装例 - Qiita](https://qiita.com/m_mitsuhide/items/c0cce7f3a79907c6e75c)
- [axiosの使い方まとめ (GET/POST/例外処理) - スケ郎のお話 ](https://www.sukerou.com/2019/05/axios.html)


使うのは axios というやつ。  
コレはブラウザだとか、 node.js 上で動作する HTTP クライアント。  
非同期に HTTP 通信を実行したい場合に簡単に実装できるので、Vue.js ではコレを使うのがスタンダードらしい。

axios をインストールする手順は、以下のコマンドを実行するだけ。
```sh
$ npm install axios
```


### GET 通信の基本

基本的な使い方は以下の通り。
```ts
import axios from 'axios';

axios.get('/user')
.then(function (response) {
  // 成功した場合に実行する処理
  console.log(response);
})
.catch(function (error) {
  // 失敗した場合に実行する処理
  console.log(error);
})
.finally(function () {
  // 成功・失敗問わずに必ず実行する処理
});
```

その他にも、クエリパラメータを添える場合は、以下の２パターンを使い分ける。
（さっきはパラメータを渡していなかった）
- パターン１：叩く URL に直接記述する
    ```ts
    axios.get('/user?ID=12345')
    ```
- パターン２：第二引数としてオプション指定する
    ```ts
    axios.get('/user', {params: {ID: 12345}})
    ```
    だとか
    ```ts
    axios.get('/user', {
        params: {
            ID: 12345
        }
    })
    ```

そんで返ってくるレスポンス（response）の情報は以下の通り
| データ              | 説明               |個人メモ|
|---------------------|--------------------|--------|
| response.data       | レスポンスデータ   | 成功時は、ココから情報を取り出す |
| response.status     | ステータスコード   | 失敗時は、ココからエラーコードを取り出す |
| response.statusText | ステータステキスト | どういう時に使うんだろうね |
| response.headers    | レスポンスヘッダ   | どういう時に使うんだろうね |
| response.config     | コンフィグ         | どういう時に使うんだろうね |



### POST 通信の基本
基本的な使い方は以下の通りで、GET 同じっぽい。
```ts
import axios from 'axios';

axios.post('/user', {
    id: 12345,
    name: 'kana-chang'
})
.then(function (response) {
  // 成功した場合に実行する処理
  console.log(response);
})
.catch(function (error) {
  // 失敗した場合に実行する処理
  console.log(error);
})
.finally(function () {
  // 成功・失敗問わずに必ず実行する処理
});
```

ただ、上記のように JSON 形式で送るに、`x-www-form-urlencoded` 形式で POST する方法もあるみたい。  
URLSearchParams インターフェイスを使うと、 URL のクエリパラメータの操作に役立つメソッドを利用できるようになる。  
参考→ [URLSearchParams - MDN web docs](https://developer.mozilla.org/ja/docs/Web/API/URLSearchParams)
```ts
var params = new URLSearchParams()  //------------- URLSearchParams オブジェクトを生成した
params.append('id', 12345)  //--------------------- 指定されたキーと値のペアを検索パラメータとして追加した
params.append('name', 'kana-chang')
const res = await axios.post('/user', params)
```


そんで返ってくるレスポンス（response）も同じっぽい。
| データ              | 説明               |個人メモ|
|---------------------|--------------------|--------|
| response.data       | レスポンスデータ   | 成功時は、ココから情報を取り出す |
| response.status     | ステータスコード   | 失敗時は、ココからエラーコードを取り出す |
| response.statusText | ステータステキスト | どういう時に使うんだろうね |
| response.headers    | レスポンスヘッダ   | どういう時に使うんだろうね |
| response.config     | コンフィグ         | どういう時に使うんだろうね |























