# 参考URL


- [TypeScript - JavaScript that scales. (公式サイト)](https://www.typescriptlang.org/)
- [TypeScriptってどんなもの？ プロ生ちゃんと始めてみよう！ - Build Insider](https://www.buildinsider.net/web/pronamatypescript/01)
- [Insider.NET > TypeScriptで学ぶJavaScript入門 - ＠IT](https://www.atmarkit.co.jp/ait/subtop/features/dotnet/typescript_index.html)
- [TypeScript の概要 - Qiita](https://qiita.com/EBIHARA_kenji/items/4de2a1ee6e2a541246f6)
- [TypeScriptの型入門 - Qiita](https://qiita.com/uhyo/items/e2fdef2d3236b9bfe74a)
- [ワイ「いうても型なんて面倒くさいだけやろ？」 - Qiita](https://qiita.com/Yametaro/items/2eaa6fd75255c8c2a2bb)
- [TypeScriptチュートリアル - Qiita](https://qiita.com/ochiochi/items/efdaa0ae7d8c972c8103)
- [【Node.js入門】各OS別のインストール方法まとめ(Windows,Mac,Linux…)](https://www.sejuku.net/blog/72545)

# TypeScript の特徴とは？

参考にさせてもらったサイトによると、以下のような特徴があるらしい。
ただ、Javascript 自体にそれほど明るくないので、ちょっとピンとこない。
他の参考サイトの解説と組み合わせて、特徴を補足していく

- JavaScript のスーパーセット（上方互換）
    - JavaScriptの最新仕様である、"ES2018" の構文仕様が使える。
    - Javascript に便利な機能が追加された言語 っぽい
    - TypeScript で書いたコードはコンパイラによって Javascript に変換される
- 型定義が利用可能(静的型付け)
    - これが Javascript との一番大きな違い
    - Javascript は動的型付け、TypeScript は静的型付け
    - Javascript だと関数実行時に引数のチェック処理を作成者が入れなきゃだが、TypeScript だとコンパイル時にエラーとして検出される
- インターフェース、クラスが利用可能
- null/undefined safe である
- 型定義ファイルがあれば外部ライブラリも型を利用可能
- ジェネリックが利用可能
- エディタによる入力補完が強力。(Visual Studio Code など対応しているエディタ)
    - 俺、Vim 派やねん
    - 型情報があるから



# じゃあ TypeScript を動かせる環境はどうやって作る？
基本的に TypeScript のソースコードは、Javascript にコンパイルした後に実行するになる。  
そのため、まずは TypeScript のコンパイラを導入する必要がある。  

OS を問わず使えるのは node.js に入ってる `npm` コマンドを使って方法する方法。  
ということで、まずは node.js の導入を目指す。  


## Step1: node.js パッケージの導入

ココは OS によって違うので色々試しておくこと。  
（Linuxはかんたんでいいな！！！！）

### Windows 版
まずはインストーラを導入する。  
とりあえず推奨版を公式サイトからとってくる。  

- Windows版：https://nodejs.org/ja/
- その他OS版：https://nodejs.org/ja/download/

あとはインストーラを実行すればいい。  

### Linux 版（Debian 系）
すごく簡単。  
以下のコマンドを実行すればいい。
```sh
# apt install nodejs npm
```
コレで、node.js と、パッケージ管理ルール npm の療法がインストールできる。


細かなバージョンを指定された場合、 NodeSource からインストールできるとのこと
```sh
$ curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash  -
$ sudo apt-get install nodejs npm
```


### Linux 版（RedHat 系）
いつもの色々ある拡張リポジトリ「epel」さんを導入してあげる。  
以下のコマンドを実行。
```sh
# yum install epel-release
```
その後、以下のコマンドで node.js と npm をインストール。
```sh
# yum install nodejs npm
```


## Step2: TypeScript コンパイラの導入
Step1 を実行した環境上で、以下のコマンドを実行する。
```sh
# npm install -g typescript
```

## Step3: インストール内容のチェック
一応インストールに成功したか、どんなバージョンが入ったかを確かめる。  
以下のコマンドを実行。
```sh
$ tsc -v
```
うちの環境だと、こんな感じだった。
```sh
$ tsc -v
Version 3.9.5
```


# とりあえず動かしてみる

実際に TypeScript でコードを書いて、コンパイルしてみる。  
以下のファイルを作成する。  
（手元の Vim だとシンタックスハイライトつかねぇ）  

- helloworld.ts
    ```ts
    const message:string = 'Hello World! This is TypeScript Code !';
    console.log(message);
    ```

そんで、上記をコンパイルしてみる。  
以下のコマンドを実行。
```sh
$ tsc helloworld.ts
```

コンパイルに成功したら、追加で `helloworld.js` というファイルができてるはず。
```sh
$ ls -l
total 8
-rw-rw-r-- 1 kanamaru kanamaru 78 Jun 24 07:43 helloworld.js
-rw-rw-r-- 1 kanamaru kanamaru 87 Jun 24 07:42 helloworld.ts
```
ちなみに中身はこんな感じ。まぁ確かに書き換わってるね。
- helloworld.js
    ```js
    var message = 'Hello World! This is TypeScript Code !';
    console.log(message);
    ```


出来上がった JavaScript の動作確認を行う。  
以下のコマンドを実行。
```sh
$ node helloworld.js
Hello World! This is TypeScript Code !
```
まぁ期待通り。ひとまずコレで色々一応動作確認程度はできるようになった。


とりあえずは、以下のサイトがすごくわかりやすいので、コレをベースに勉強を進める

- [TypeScriptチュートリアル - Qiita](https://qiita.com/ochiochi/items/efdaa0ae7d8c972c8103)











