# 参考
- [【Nuxt.js】Vue.jsをより効果的に使えるフレームワークのメリットや利用シーンを紹介！- Udemy](https://udemy.benesse.co.jp/development/web/nuxt-js.html)
- [Nuxt.jsを使ったTodoリストを作ってみる - BOEL](https://www.boel.co.jp/tips/vol107_todoLists-with-Nuxt-js.html)
- [NUXT 公式](https://ja.nuxtjs.org)
- [はじめに - NUXTJS 公式](https://ja.nuxtjs.org/guide/)
- [Nuxt.js使ってみた - Qiita](https://qiita.com/_takeshi_24/items/224d00e5a026dbb76716)
- [Nuxt.jsに飛びつく前に~Nuxt.jsを習得するための前提技術と、その勉強方法の紹介~ - Qiita](https://qiita.com/kyohei_ai/items/763b0c228a8451c68865)
- [SSR（サーバーサイドレンダリング）とは - Qiita](https://qiita.com/negi524/items/40166176a8fb7186c9b2)

- [とりあえずUbuntuで新しいNode.js, npmをインストール - Qiita](https://qiita.com/kerupani129/items/60ee8c8becc2fe9f0d28)
- [知らないのは損！npmに同梱されているnpxがすごい便利なコマンドだった- Developpers.IO](https://dev.classmethod.jp/articles/node-npm-npx-getting-started/)
- [npm 5.2.0の新機能！ 「npx」でローカルパッケージを手軽に実行しよう - Qiita](https://qiita.com/tonkotsuboy_com/items/8227f5993769c3df533d)



# Nuxt.js とは？
参考にしたサイトで説明されていることをまとめると以下のような感じらしい。

- Web アプリ開発の機能が最初から組み込まれた Vue.js ベースの JavaScript フレームワーク
    - ちなみに読み方は「ナクスト」
    - React.js ベースのサーバサイドレンダリング用フレームワーク「Next.js」に触発されて作られたとのこと
        - サーバサイドレンダリングってのは、本来 Javascript とかで行う画面の書き換え処理をサーバ側で実行させて、利用者の待機時間を短くすること
        - クライアント側でヤッちゃうと、サイトにアクセスした際に画面が一瞬とは言えど表示されない状態に陥る


- UI 以外の部分で Web アプリケーション開発に必要な機能が最初から組み込まれてる
    - ベースになった Vue.js は UI 等のフロントエンド向けのフレームワーク
    - 「UI に特化してる Vue.js」 ＋ 「UI 以外の Ajax やサーバサイドレンダリング」を利用できる

- 強力なモジュールエコシステムなるものがあり、拡張が容易
    - REST、GraphQL エンドポイント、CSS フレームワーク に簡単に接続可能
    - PWA や AMP をサポート


# 利用・習得の前提となる知識
必要な要素はこんな感じらしい。  
- Vue.js
    - コンポーネント、テンプレートとかの基本を知っておいたほうがいいらしい
    - この前記録を残したのでそれを参考に。
- JavaScript
    - Java の拡張である TypeScript をこの前記録したのでそれを参考に。
- JSON
- HTML
- CSS



# お試しで使ってみる

TypeScript の基本で node.js を導入した環境を作ってると思うので、それを使う。

今回は `npx` なるコマンドを使うことになる。  
コレは何かというと、「ローカルにインストールした npm パッケージを npx コマンドだけで実行できる」ようにするもの。  
他にも、以下のような機能がある。
- run-scriptを使用せずにローカルインストールしたコマンドを実行する
- グローバルインストールせずに一度だけコマンドを実行する
- GitHubやGistで公開されているスクリプトを実行する

コレまでは 以下に示す「ユーザが一手間かける方法3つ」のどれかをとっていたらしく、簡素なコマンド一つで実行できるようになったのは素晴らしいこと。
- 方法1: `./node_modules/.bin/(パッケージ名)` で実行する
- 方法2: `$(npm bin)/(パッケージ名)`で実行する
- 方法3: package.json に npm-scripts を記述して実行する

ちなみに、コレは前回の環境にはまだ入っていない...。  
なのでまずはとりあえず環境構築からやってみる。


## 環境の構築(`npx` の導入)

まずは、nodejs と npm をインストールするため、以下のコマンドを実行。
```sh
# apt install nodejs npm
```
インストールしたらバージョンを確認。
```sh
$ node -v
v8.10.0
$ npm -v
3.5.2
```
Ubuntu のリポジトリからとってきた npm はバージョンが古いようなので、別途 `npx` をインストールする。
TypeScript インストールと同じように、以下のコマンドを実行。
```sh
# npm install -g npx
```


## Nuxt のプロジェクトを作る

無事 `npx` が入ったので Nuxt.js 用のプロジェクトを作ってみる  
Nuxt.js に用意されてるプロジェクト作成ツール「create-nuxt-app」を今回は使って、今回はプロジェクトを作る。  
ちなみにこのコマンドは、対話式でプロジェクトを作るみたいなので、問われる設定項目等を記録した。

1. まずは、create-nuxt-app を実行する
    プロジェクトを作りたいディレクトリに移動して、以下のコマンドを実行
    ```sh
    cd /home/kanamaru/03-Nuxt
    $ npx create-nuxt-app KANA-SAMPLE
    ```
    対話形式で、以降に示す項目の設定が始まったら成功。

2. プロジェクト名を設定する
    以下の画面が出力されるので、プロジェクト名を入力する。
    ```sh
    $ npx create-nuxt-app KANA-SAMPLE

    create-nuxt-app v3.1.0
    ✨  Generating Nuxt.js project in KANA-SAMPLE
    ? Project name: (KANA-SAMPLE)
    ```
    （）の中にデフォルト値として、さっき指定した「KANA-SAMPLE」が入力されていた。
    なので、特に何も入力せずに Enter キーを押下。

3. 使うスクリプト言語を設定する
    プロジェクト名を設定したら、以下が出力される。
    ```sh
    $ npx create-nuxt-app KANA-SAMPLE

    create-nuxt-app v3.1.0
    ✨  Generating Nuxt.js project in KANA-SAMPLE
    ? Project name: KANA-SAMPLE
    ? Programming language: (Use arrow keys)
    ❯ JavaScript
      TypeScript
    ```
    今回は TypeScript を使いたいので、矢印キーで TypeScript を選択して、Enter キーを押下。

4. 利用するパッケージマネージャを設定する
    スクリプト言語を設定したら、以下が出力される。
    ```sh
    $ npx create-nuxt-app KANA-SAMPLE
    create-nuxt-app v3.1.0
    ✨  Generating Nuxt.js project in KANA-SAMPLE
    ? Project name: KANA-SAMPLE
    ? Programming language: TypeScript
    ? Package manager: (Use arrow keys)
    ❯ Yarn
      Npm
    ```
    どっちがいいのかなんてよくわからんので、使ったことのある Npm を選択して、Enter キーを押下。



5. UI のフレームワークを設定する
    パッケージマネージャを設定したら、以下が出力される。
    ```sh
    $ npx create-nuxt-app KANA-SAMPLE
    create-nuxt-app v3.1.0
    ✨  Generating Nuxt.js project in KANA-SAMPLE
    ? Project name: KANA-SAMPLE
    ? Programming language: TypeScript
    ? Package manager: Npm
    ? UI framework: (Use arrow keys)
    ❯ None
      Ant Design Vue
      Bootstrap Vue
      Buefy
      Bulma
      Element
      Framevuerk
      iView
      Tachyons
      Tailwind CSS
      Vuesax
      Vuetify.js
    ```
    よくわからんので、None を選択して、Enter キーを押下。
    (Vue.js がアレば、迷うこと無くそれを選択したのだが...)


6. Nuxt.js のモジュールを設定する
    フレームワークを設定したら、以下が出力される。
    ```sh
    $ npx create-nuxt-app KANA-SAMPLE
    create-nuxt-app v3.1.0
    ✨  Generating Nuxt.js project in KANA-SAMPLE
    ? Project name: KANA-SAMPLE
    ? Programming language: TypeScript
    ? Package manager: Npm
    ? UI framework: None
    ? Nuxt.js modules: (Press <space> to select, <a> to toggle all, <i> to invert selection)
    ❯◯ Axios
     ◯ Progressive Web App (PWA)
     ◯ Content
    ```
    よくわからんな、発狂しそう。
    Axios とかだと API 叩くやつだったはず。必要か。  
    ちなみに [公式ページ](Nuxt.js 公式モジュール一覧) によるとこんな感じらしいが、テストなので今回は何も選択せずに、Enter キーを押下。
    |モジュール名|説明|備考|
    |------------|-----------------|----------|
    | Axios      |セキュアかつ簡単に Axios と Nuxt.js とを統合し、HTTP リクエストを送ります|外部 API を叩く時に使う|
    | PWA        |十分にテストされアップデートされた安定した PWA ソリューションを Nuxt に提供します | Web アプリをモバイルアプリみたいに使うために必要なもの |
    | Content    |ディレクトリへの書き込みや、MongoDB のような API を通した Markdown や JSON、YAML、CSV ファイルの取得をします|ファイルの取得に使う？|

7. 静的検証ツールを設定する
    モジュールを設定したら、以下が出力される。
    ```sh
    $ npx create-nuxt-app KANA-SAMPLE
    create-nuxt-app v3.1.0
    ✨  Generating Nuxt.js project in KANA-SAMPLE
    ? Project name: KANA-SAMPLE
    ? Programming language: TypeScript
    ? Package manager: Npm
    ? UI framework: None
    ? Nuxt.js modules:
    ? Linting tools: (Press <space> to select, <a> to toggle all, <i> to invert selection)
    ❯◯ ESLint
     ◯ Prettier
     ◯ Lint staged files
     ◯ StyleLint
    ```
    コードを実行する前に色々バグを見つけられるのは素敵だけど、今回はてすと。  
    何も選択せずに、Enter キーを押下。

8. テストフレームワークを設定する
    検証ツールを設定したら、以下が出力される。
    ```sh
    $ npx create-nuxt-app KANA-SAMPLE
    create-nuxt-app v3.1.0
    ✨  Generating Nuxt.js project in KANA-SAMPLE
    ? Project name: KANA-SAMPLE
    ? Programming language: TypeScript
    ? Package manager: Npm
    ? UI framework: None
    ? Nuxt.js modules:
    ? Linting tools: (Press <space> to select, <a> to toggle all, <i> to invert selection)
    ? Testing framework: (Use arrow keys)
    ❯ None
      Jest
      AVA
      WebdriverIO
    ```
    今回はテスト(お試し)なので、何も選択せずに、Enter キーを押下。

9. レンダリングモードを設定する
テストフレームワークを設定したら、以下が出力される。
```sh
$ npx create-nuxt-app KANA-SAMPLE
create-nuxt-app v3.1.0
✨  Generating Nuxt.js project in KANA-SAMPLE
? Project name: KANA-SAMPLE
? Programming language: TypeScript
? Package manager: Npm
? UI framework: None
? Nuxt.js modules:
? Linting tools: (Press <space> to select, <a> to toggle all, <i> to invert selection)
? Testing framework: None
? Rendering mode: (Use arrow keys)
❯ Universal (SSR / SSG)
  Single Page App
```
ちなみに各項目の意味は以下の通りだが、VM がクソ雑魚なので、SPA を選択し、Enter キーを押下。
    |モード名|説明|備考|
    |------------|-----------------|----------|
    | Universal (SSR / SSG)  |サーバサイドレンダリング |冒頭で説明済み|
    | Single Page App        | シングルページアプリケーション| 上に同じ |

10. デプロイターゲットを設定する。
レンダリングモードを設定したら、以下が出力される。
```sh
$ npx create-nuxt-app KANA-SAMPLE
create-nuxt-app v3.1.0
✨  Generating Nuxt.js project in KANA-SAMPLE
? Project name: KANA-SAMPLE
? Programming language: TypeScript
? Package manager: Npm
? UI framework: None
? Nuxt.js modules:
? Linting tools: (Press <space> to select, <a> to toggle all, <i> to invert selection)
? Testing framework: None
? Rendering mode: Single Page App
? Deployment target: (Use arrow keys)
❯ Server (Node.js hosting)
  Static (Static/JAMStack hosting)
```
まぁよくわからんけど、Server を選択し、Enter キーを押下。



11. デプロイメントツールを設定する。
デプロイターゲットを設定したら、以下が出力される。
```sh
$ npx create-nuxt-app KANA-SAMPLE
create-nuxt-app v3.1.0
✨  Generating Nuxt.js project in KANA-SAMPLE
? Project name: KANA-SAMPLE
? Programming language: TypeScript
? Package manager: Npm
? UI framework: None
? Nuxt.js modules:
? Linting tools: (Press <space> to select, <a> to toggle all, <i> to invert selection)
? Testing framework: None
? Rendering mode: Single Page App
? Deployment target: Server (Node.js hosting)
? Development tools: (Press <space> to select, <a> to toggle all, <i> to invert selection)
❯◯ jsconfig.json (Recommended for VS Code)
 ◯ Semantic Pull Requests
```
開発時に使うツールの選択が求められてるが、今回はお試しなので何も選択せずに、Enter キーを押下。

12. ひとまずココまでやると、プロジェクトの生成が始まる。


### 発生したエラー１
エラーが起きやがった。
```sh
$ npx create-nuxt-app KANA-SAMPLE
create-nuxt-app v3.1.0
✨  Generating Nuxt.js project in KANA-SAMPLE
? Project name: KANA-SAMPLE
? Programming language: TypeScript
? Package manager: Npm
? UI framework: None
? Nuxt.js modules:
? Linting tools: (Press <space> to select, <a> to toggle all, <i> to invert selection)
? Testing framework: None
? Rendering mode: Single Page App
? Deployment target: Server (Node.js hosting)
? Development tools: (Press <space> to select, <a> to toggle all, <i> to invert selection)
Warning: name can no longer contain capital letters
WARN engine nuxt@2.13.1: wanted: {"node":">=8.9.0","npm":">=5.0.0"} (current: {"node":"8.10.0","npm":"
3.5.2"})
WARN engine @nuxt/opencollective@0.3.0: wanted: {"node":">=8.0.0","npm":">=5.0.0"} (current: {"node":"
8.10.0","npm":"3.5.2"})
WARN engine semver@7.3.2: wanted: {"node":">=10"} (current: {"node":"8.10.0","npm":"3.5.2"})
WARN engine @nuxt/friendly-errors-webpack-plugin@2.5.0: wanted: {"node":">=8.0.0","npm":">=5.0.0"} (cu
rrent: {"node":"8.10.0","npm":"3.5.2"})
npm WARN deprecated core-js@2.6.11: core-js@<3 is no longer maintained and not recommended for usage d
ue to the number of issues. Please, upgrade your dependencies to the actual version of core-js@3.
npm ERR! Linux 5.3.0-59-generic
npm ERR! argv "/usr/bin/node" "/usr/bin/npm" "install"
npm ERR! node v8.10.0
npm ERR! npm  v3.5.2
npm ERR! code EMISSINGARG
npm ERR! typeerror Error: Missing required argument #1
npm ERR! typeerror     at andLogAndFinish (/usr/share/npm/lib/fetch-package-metadata.js:31:3)
npm ERR! typeerror     at fetchPackageMetadata (/usr/share/npm/lib/fetch-package-metadata.js:51:22)
npm ERR! typeerror     at resolveWithNewModule (/usr/share/npm/lib/install/deps.js:456:12)
npm ERR! typeerror     at /usr/share/npm/lib/install/deps.js:457:7
npm ERR! typeerror     at /usr/share/npm/node_modules/iferr/index.js:13:50
npm ERR! typeerror     at /usr/share/npm/lib/fetch-package-metadata.js:37:12
npm ERR! typeerror     at addRequestedAndFinish (/usr/share/npm/lib/fetch-package-metadata.js:82:5)
npm ERR! typeerror     at returnAndAddMetadata (/usr/share/npm/lib/fetch-package-metadata.js:117:7)
npm ERR! typeerror     at pickVersionFromRegistryDocument (/usr/share/npm/lib/fetch-package-metadata.j
s:134:20)
npm ERR! typeerror     at /usr/share/npm/node_modules/iferr/index.js:13:50
npm ERR! typeerror This is an error with npm itself. Please report this error at:
npm ERR! typeerror     <http://github.com/npm/npm/issues>
npm ERR! Please include the following file with any support request:
npm ERR!     /home/kanamaru/03-Nuxt/KANA-SAMPLE/npm-debug.log
/home/kanamaru/.npm/_npx/16646/lib/node_modules/create-nuxt-app/node_modules/sao/lib/installPackages.js:108
        throw new SAOError(`Failed to install ${packageName} in ${cwd}`)
Error: Failed to install packages in /home/kanamaru/03-Nuxt/KANA-SAMPLE
    at ChildProcess.ps.on.code (/home/kanamaru/.npm/_npx/16646/lib/node_modules/create-nuxt-app/node_modules/sao/lib/installPackages.js:108:15)
    at emitTwo (events.js:126:13)
    at ChildProcess.emit (events.js:214:7)
    at maybeClose (internal/child_process.js:925:16)
    at Process.ChildProcess._handle.onexit (internal/child_process.js:209:5)
```
何かパッケージのインストールに失敗してるっぽい。  
```sh
WARN engine nuxt@2.13.1: wanted: {"node":">=8.9.0","npm":">=5.0.0"} (current: {"node":"8.10.0","npm":"3.5.2"})
WARN engine @nuxt/opencollective@0.3.0: wanted: {"node":">=8.0.0","npm":">=5.0.0"} (current: {"node":"8.10.0","npm":"3.5.2"})
WARN engine semver@7.3.2: wanted: {"node":">=10"} (current: {"node":"8.10.0","npm":"3.5.2"})
WARN engine @nuxt/friendly-errors-webpack-plugin@2.5.0: wanted: {"node":">=8.0.0","npm":">=5.0.0"} (current: {"node":"8.10.0","npm":"3.5.2"})
npm WARN deprecated core-js@2.6.11: core-js@<3 is no longer maintained and not recommended for usage due to the number of issues. Please, upgrade your dependencies to the actual version of core-js@3.
```
バージョンが古いみたい。
sudo 使えば無理やり行けたりするのか。だめだ。同じエラーが出る。

ちょっとアップデートしてみる。  
[ココ](https://qiita.com/kerupani129/items/60ee8c8becc2fe9f0d28) を参考に、以下のコマンドを実行。
```sh
$ sudo npm cache clean
$ sudo npm install -g n
$ sudo n stable

  installing : node-v12.18.1
       mkdir : /usr/local/n/versions/node/12.18.1
       fetch : https://nodejs.org/dist/v12.18.1/node-v12.18.1-linux-x64.tar.xz
   installed : v12.18.1 (with npm 6.14.5)

Note: the node command changed location and the old location may be remembered in your current shell.
         old : /usr/bin/node
         new : /usr/local/bin/node
To reset the command location hash either start a new shell, or execute PATH="$PATH"
```
次は、npm の番。  
以下のコマンドを実行。
```sh
$ sudo npm update -g npm
```
バージョンを確認。
```sh
$ node -v
v12.18.1
$ npm -v
6.14.5
```
コレで再度実行してみる。
```sh
$ npx create-nuxt-app KANA-SAMPLE
🎉  Successfully created project KANA-SAMPLE

  To get started:

        cd KANA-SAMPLE
        npm run dev

  To build & start for production:

        cd KANA-SAMPLE
        npm run build
        npm run start


  For TypeScript users.

  See : https://typescript.nuxtjs.org/cookbook/components/
```

OK!!!!!!!!!!!!!!!!  
今気づいたけど、`/home` 直下じゃなかったのが問題だったりする？  そんなバカな。


## 実際に作られたプロジェクトを確認する
とりあえず、以下のコマンドを実行して、作成されたプロジェクトのディレクトリを確認する。
```sh
$ LANG=C tree -L 1 KANA-SAMPLE/
KANA-SAMPLE/
|-- README.md
|-- assets  ------------------------ CSSやSass、フォントなど、コンパイルされないファイルを入れるディレクトリ
|-- components  -------------------- Vue.jsのコンポーネント(部品)を入れるディレクトリ，全ページで使用するヘッダーやフッターなどをコンポーネントとして分けて放り込む
|-- layouts  ----------------------- 画面全体の基本的なレイアウトを定義するvueファイルを置くディレクトリ
|-- middleware  -------------------- アプリケーションのミドルウェアを入れるディレクトリ，ミドルウェアを使用することで、ページやレイアウトをレンダリングするより前に実行されるカスタム関数を定義できる
|-- node_modules
|-- nuxt.config.js  ---------------- Nuxt.jsのカスタム設定を記述するファイル
|-- package-lock.json
|-- package.json  ------------------ インストールしたパッケージやスクリプトの一覧とバージョンが記載されているファイル
|-- pages  ------------------------- アプリケーションのビュー及びルーティングファイルを入れるディレクトリ
|-- plugins  ----------------------- Vue.jsアプリケーションをインスタンス化する前に実行したいJavaScriptプラグインを入れるディレクトリ
|-- static  ------------------------ 変更される可能性が低い静的ファイルを置くディレクトリ，ここに配置されたファイルは直接サーバーのルートに配置される
|-- store  ------------------------- 全てのページで利用するデータをまとめて管理するディレクトリ
`-- tsconfig.json

9 directories, 5 files
```

## 実際に作られたプロジェクトを動かして、確認してみる

プロジェクトのディレクトリに移動して、`npm run dev`を実行。

実際に実行してみると
```sh
$ cd KANA-SAMPLE/
$ npm run dev

> KANA-SAMPLE@1.0.0 dev /home/kanamaru/KANA-SAMPLE
> nuxt


ℹ NuxtJS collects completely anonymous data about usage.              07:56:06
  This will help us improving Nuxt developer experience over the time.
  Read more on https://git.io/nuxt-telemetry

? Are you interested in participation? Yes


   ╭───────────────────────────────────── ──╮
   │                                       │
   │   Nuxt.js @ v2.13.1                   │
   │                                       │
   │   ▸ Environment: development          │
   │   ▸ Rendering:   client-side          │
   │   ▸ Target:      server               │
   │                                       │
   │   Listening: http://localhost:3000/   │
   │                                       │
   ╰───────────────────────────────────── ──╯

ℹ Preparing project for development                                   07:56:12
ℹ Initial build may take a while                                      07:56:12
✔ Builder initialized                                                 07:56:12
✔ Nuxt files generated                                                07:56:12
ℹ Starting type checking service...                   nuxt:typescript 07:56:16

✔ Client
  Compiled successfully in 7.55s

ℹ Type checking in progress...                                                                                                                                                           nuxt:typescript 07:56:23
ℹ Waiting for file changes                                                                                                                                                                               07:56:23
ℹ Memory usage: 311 MB (RSS: 398 MB)                                                                                                                                                                     07:56:23
ℹ Listening on: http://localhost:3000/                                                                                                                                                                   07:56:23
ℹ No type errors found                                                                                                                                                                   nuxt:typescript 07:56:27
ℹ Version: typescript 3.8.3                                                                                                                                                              nuxt:typescript 07:56:27
ℹ Time: 11546 ms                                                                                                                                                                         nuxt:typescript 07:56:27
```

次にブラウザでチェックしてみる。
該当の仮想マシンに接続して、firefox を起動してみる。


```sh
$ ssh -X kanamaru@<VMのIP>
$ firefox
```









