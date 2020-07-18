# Nuxt で「動くwebアプリ」を作ってみる

# 参考 URL

- [Nuxt.js使ってみた - Qiita](https        //qiita.com/_takeshi_24/items/224d00e5a026dbb76716)
- [Nuxt.jsを使ってTodoリストを作ってみる - BOEL](https        //www.boel.co.jp/tips/vol107_todoLists-with-Nuxt-js.html)



# 環境準備
とりあえず以下のコマンドを実行して、動作環境を整える
```sh
# apt install nodejs npm
# npm aache clean
# npm install -g n
# n stable
# npm update -g npm
```

# 手順１：まずは Nuxt のプロジェクトを作る
以下のコマンドを実行して、プロジェクトを作成する。  
```sh
$ npx create-nuxt-app KANA-SAMPLE
```

設定内容は以下の通り。


| 項目名               | 設定内容 | 備考 |
|----------------------|----------------------------------------------------|--|
| Project name         | KANA-SAMPLE                                        |  |
| Programming language | TypeScript                                         |  |
| Package manager      | Npm                                                |  |
| UI framework         | None                                               |  |
| Nuxt.js modules      | Axios, Progressive Web App (PWA), Content          |  |
| Linting tools        | ESLint, Prettier, Lint staged files, StyleLint     |  |
| Testing framework    | None                                               |  |
| Rendering mode       | Universal (SSR / SSG)                              |  |
| Deployment target    | Server (Node.js hosting)                           |  |
| Development tools    |                                                    |  |


いつもの手順で動作してるかどうかを確認する。
```sh
$ ssh -X <UserName>@<IP-Address>
$ firefox localhost:3000
```
































