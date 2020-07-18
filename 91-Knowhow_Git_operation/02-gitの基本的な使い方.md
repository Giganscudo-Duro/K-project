

# 参考 URL

- [【 git add 】コマンド――変更内容をインデックスに追加してコミット対象にする - @IT](https://www.atmarkit.co.jp/ait/articles/2003/13/news031.html)
- [【Git】基本コマンド - Qiita](https://qiita.com/konweb/items/621722f67fdd8f86a017)
- [リモートブランチをローカルに持ってきてチェックアウト - Qiita](https://qiita.com/megu_ma/items/26799c89f593a2414333)
- [GitでPushしたらfatal: The current branch ブランチ名 has no upstream branch.となった時の対応方法 - Qiita](https://qiita.com/ponsuke0531/items/410735b544795506fdc5)
- [Git で「追跡ブランチ」って言うのやめましょう - Qiita](https://qiita.com/uasi/items/69368c17c79e99aaddbf)
- [GitHubを使うなら最低限知っておきたい、プルリクエストの送り方とレビュー、マージの基本 (1/2) - @IT](https://www.atmarkit.co.jp/ait/articles/1702/27/news022.html)






# ものすげー略式
基本はこれだけ知ってれば戦える。

## リモートリポジトリを手元にクローンして開発を始める
以下のコマンドを実行。
```sh
$ git clone <URL>
$ git checkout -b <ローカルブランチ名> <リモートにあるブランチ名>
```
あとは、開発を進めればOK。

## 開発内容をリモートリポジトリに反映させる
以下のコマンドを実行。
```sh
$ git pull
$ git status
$ git add <変更したファイル>
$ git commit -m "コメント"
$ git push --set-upstream origin <ローカルブランチ名>
```



# ちょっと詳しく書いた場合


## 基本的な作業の流れ

| 手番 | 作業内容 |
|------|----------|
| 1    | リーダが、GitHub 上でプロジェクトを立ち上げる                       |
| 2    | GitHub が、Master ブランチを作成する                                |
| 3    | リーダが、開発用の develop ブランチを作成する                       |
| 4    | チーム内で開発担当の割当が行われる                                  |
| 5    | 開発者が、ローカルマシン上に git を clone する<br>(2回目以降は、ローカルマシン上に git の最新版を pull する)  |
| 6    | 開発者が、ローカルマシン上で自分用ブランチを作成する                |
| 7    | 開発者が、ローカルマシン上で開発を行う                              |
| 8    | 開発者が、ローカルマシン上での開発内容を git に push する           |
| 9    | 各開発者が、自分用ブランチで色々開発する                            |
| 10   | 開発者が、GitHub 上で PullRequest を発行する                        |
| 11   | 開発メンバによるレビューが行われる                                  |
| 12   | マージをコンプリートさせる                                          |
| 13   | 開発者全員の担当がマージされたら、手順 4 に戻る                     |




## 手順 0：Git Hub のアカウントを取得する
とりあえずアカウントを取得したら、開発マシン上で以下のコマンドを実行しておく。
```sh
$ git config --global user.email "<GitHubに登録したメルアド>"
$ git config --global user.name "<コミット時に表示させたいユーザ名（適当でいい）>"
```


## 手順 1：リーダが、GitHub 上でプロジェクトを立ち上げる
Web ブラウザ上で実施することになる。  
プロジェクトを作成したときに、master ブランチが作成される。  
まぁ普通に自分のアカウントで GitHub にログインし、 [New] ボタンを押し、以下の項目を入力して [Create Repository] ボタンをクリックすれば完了。

| 項目 | 入力内容 |
|------|----------|
| Repository name   | 適当なリポジトリ名を入力 |
| Description       | リポジトリの説明。入力は省いてもOK |
| Public            | Private にするとお金が必要なので Public で。 |

今回はお試しで「study-git-command」というリポジトリを作った。



## 手順 2：リーダが、Master ブランチを作成＆ README.md を配置する
自分がリーダならば、この手順を実行する。

まずは自分の開発マシン上に、先程作成した git をクローン。
```sh
$ git clone https://github.com/Giganscudo-Duro/study-git-command.git
Cloning into 'study-git-command'...
warning: You appear to have cloned an empty repository.
```

空っぽの git がクローンされたはずなので、`test-git-command` ディレクトリに移動する。
```sh
$ cd study-git-command/
```

`test-git-command` ディレクトリ内で README.md ファイルを作成する。
```sh
$ echo "This is README file." > README.md
$ echo "This is master branch." >> README.md
$ cat ./README.md
This is README file.
This is master branch.
```

master ブランチの作成 ＆ README.md をリモートリポジトリに push するため、以下の３つのステップを実行する。

1. `git add` コマンドで、変更を加えたファイルをインデックスに追加  
    開発マシン上で、以下のコマンドを実行する。
    ```sh
    $ git add ./README.md
    ```

2. `git commit` コマンドで、ローカルリポジトリにコミット  
    開発マシン上で、以下のコマンドを実行する。  
    指定する文字列部には、「変更内容」を入力する（今回は test とした）。
    ```sh
    $ git commit -m "Create master branch"
    [master (root-commit) 94f2ff4] Create master branch
     1 file changed, 2 insertions(+)
     create mode 100644 README.md
    ```
    実行結果確認のため `git branch` コマンドを実行する。
    ```sh
    $ git branch -a
    * master    ← ローカルリポジトリに `master` ブランチが作られている
    ```

3. `git push` コマンドで、ローカルリポジトリの内容をリモートリポジトリに反映  
    開発マシン上で、以下のコマンドを実行する。
    ```sh
    $ git push
    Username for 'https://github.com': <E-mail>
    Password for 'https://<E-mail>@github.com':
    Counting objects: 3, done.
    Writing objects: 100% (3/3), 262 bytes | 262.00 KiB/s, done.
    Total 3 (delta 0), reused 0 (delta 0)
    To https://github.com/Giganscudo-Duro/study-git-command.git
     * [new branch]      master -> master
    ```

最後に `git branch` コマンドを実行し、リモートリポジトリに master ブランチが作成されたことを確認できたら、手順２は完了。
```sh
$ git branch -a
* master
  remotes/origin/master  ← リモートリポジトリに `remotes/origin/master` ブランチが作られている
```



## 手順 3：リーダが、開発用の develop ブランチを作成する
自分がリーダならば、この手順を実行する。

今のブランチを確認するため、以下のコマンドを実行。
```sh
$ git branch -a
* master
  remotes/origin/master
```

develop ブランチの作成＆そこに移動するため、以下のコマンドを実行。
```sh
$ git checkout -b develop
Switched to a new branch 'develop'
```

develop ブランチに移動してることを確認するため、以下のコマンドを実行。
```sh
$ git branch -a
* develop
  master
  remotes/origin/master
```
これで、ローカルリポジトリ上に `develop` ブランチが作成され、そこに移動していることが確認できた。


とりあえず develop ブランチだという説明を README.md に追加。
```sh
$ echo "This is develop branch." >> ./README.md
$ cat ./README.md
This is README file.
This is master branch.
This is develop branch.  ← NEW
```

develop ブランチの作成 ＆ リモートリポジトリに反映させるため、以下の４つのステップを実行。

1. `git status` コマンドで、今回の開発で変更を加えたファイルを確認  
    開発マシン上で、以下のコマンドを実行する。
    ```sh
    $ git status
    ブランチ develop
    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)
    
            modified:   README.md
    
    no changes added to commit (use "git add" and/or "git commit -a")
    ```

2. 変更した README.md をインデックスに追加  
    開発マシン上で、以下のコマンドを実行。
    ```sh
    $ git add ./README.md
    ```

3. ローカルリポジトリの develop ブランチにコミット  
    開発マシン上で、以下のコマンドを実行。
    ```sh
    $ git commit -m "Create develop branch"
    [develop 4938f30] Create develop branch
     1 file changed, 1 insertion(+)
    ```

4. リモートリポジトリに新規作成した develop ブランチを反映  
    開発マシン上で、以下のコマンドを実行。  
    (今回はリモートリポジトリに無いブランチを反映するので origin ってのを指定する必要がある)
    ```sh
    $ git push --set-upstream origin develop
    Username for 'https://github.com': <E-mail>
    Password for 'https://<E-mail>@github.com':
    Counting objects: 3, done.
    Delta compression using up to 2 threads.
    Compressing objects: 100% (2/2), done.
    Writing objects: 100% (3/3), 304 bytes | 304.00 KiB/s, done.
    Total 3 (delta 0), reused 0 (delta 0)
    remote:
    remote: Create a pull request for 'develop' on GitHub by visiting:
    remote:      https://github.com/Giganscudo-Duro/study-git-command/pull/new/develop
    remote:
    To https://github.com/Giganscudo-Duro/study-git-command.git
     * [new branch]      develop -> develop
    Branch 'develop' set up to track remote branch 'develop' from 'origin'.
    ```

最後に、`git branch` コマンドを実行して、リモートリポジトリにも develop ブランチが作成されたことを確認できたら、手順３は完了。
```sh
$ git branch -a
* develop
  master
  remotes/origin/develop  ← リモートリポジトリにも develop ブランチができてる
  remotes/origin/master
```



## 手順 4：チーム内で開発担当の割当が行われる
まぁココは自分が何の開発を担当するかなので、個々人によって違う。  
どう割り振るかはチーム次第なので、割愛。



## 手順 5：各開発者が、ローカルマシン上に git を clone する
`git clone` コマンドを実行し、自分の開発マシン上にリポジトリをクローン。
```sh
$ git clone https://github.com/Giganscudo-Duro/study-git-command.git
Cloning into 'study-git-command'...
remote: Enumerating objects: 6, done.
remote: Counting objects: 100% (6/6), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 6 (delta 0), reused 6 (delta 0), pack-reused 0
Unpacking objects: 100% (6/6), done.
```

`git branch` コマンドを実行してブランチの状態を確認できたら、手順５は完了。
```sh
$ cd study-git-command
$ git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/develop
  remotes/origin/master
```

ちなみに README.md をチェックすると、以下が表示される。
```sh
$ cat README.md
This is README file.
This is master branch.  ← 今は master ブランチにいることがわかる
```

## 手順 6：各開発者が、ローカルマシン上で自分用ブランチを作成する
今回の開発用ブランチは develop 。  
まずはそれをローカルリポジトリに取り込む必要がある。

リモートリポジトリの develop ブランチを、ローカルリポジトリに取り込むため、以下のコマンドを実行。
```sh
$ git checkout -b develop remotes/origin/develop
Branch 'develop' set up to track remote branch 'develop' from 'origin'.
Switched to a new branch 'develop'
```

`git branch` コマンドを実行し、ローカルリポジトリのブランチが切り替わったことを確認する。
```sh
$ git branch -a
* develop  ← さっきまでなかったブランチが出来上がっている
  master
  remotes/origin/HEAD -> origin/master
  remotes/origin/develop
  remotes/origin/master
```

ちなみに README.md をチェックすると、以下が表示される。
```sh
$ cat README.md
This is README file.
This is master branch.
This is develop branch.  ← develop ブランチにいるので、コイツが表示される
```

この develop ブランチをベースにして自分用のブランチ「kana-develop」を作成するため、以下のコマンドを実行。
```sh
$ git checkout -b kana-develop
Switched to a new branch 'kana-develop'
```

`git branch` コマンドを実行し、ローカルリポジトリの kana-develop に切り替わってることを確認したら、手順６は完了。
```sh
$ git branch -a
  develop
* kana-develop  ← さっきまでなかったブランチに切り替わっている
  master
  remotes/origin/HEAD -> origin/master
  remotes/origin/develop
  remotes/origin/master
```


## 手順 7：各開発者が、ローカルマシン上で開発を行う
どんな開発をするかは人によって違うので、割愛。  
今回は README.md を少し更新するため、以下のコマンドを実行。
```sh
$ echo "This is kana-develop branch." >> ./README.md
```
README.md が更新されたら、今回の手順７は完了。
```sh
$ cat ./README.md
This is README file.
This is master branch.
This is develop branch.
This is kana-develop branch.  ← これを追加した
```


## 手順 8：各開発者が、ローカルマシン上での開発内容を git に push する
各開発者が push するときは、以下に挙げる４つの手順を順番に実行する。

1. `git status` コマンドで、今回の開発で変更を加えたファイルを確認  
    開発マシン上で、以下のコマンドを実行する。
    ```sh
    $ git status
    ブランチ kana-develop
    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)
    
            modified:   README.md
    
    no changes added to commit (use "git add" and/or "git commit -a")
    ```

2. `git add` コマンドで、変更を加えたファイルをインデックスに追加  
    開発マシン上で、以下のコマンドを実行する。
    ```sh
    $ git add ./README.md  ← 今回は README.md ファイル
    ```

3. `git commit` コマンドで、ローカルリポジトリにコミット  
    開発マシン上で、以下のコマンドを実行する。  
    指定する文字列部には、「変更内容」を入力する。
    ```sh
    $ git commit -m "Create kana-develop branch"
    [kana-develop 3bcbb14] Create kana-develop branch
     1 file changed, 1 insertion(+)
    ```

4. `git push` コマンドで、ローカルリポジトリの内容をリモートリポジトリに反映  
    開発マシン上で、以下のコマンドを実行する。
    ```sh
    $ git push --set-upstream origin kana-develop
    Username for 'https://github.com': <E-mail>
    Password for 'https://<E-mail>@github.com':
    Counting objects: 3, done.
    Delta compression using up to 2 threads.
    Compressing objects: 100% (2/2), done.
    Writing objects: 100% (3/3), 311 bytes | 311.00 KiB/s, done.
    Total 3 (delta 0), reused 0 (delta 0)
    remote:
    remote: Create a pull request for 'kana-develop' on GitHub by visiting:
    remote:      https://github.com/Giganscudo-Duro/study-git-command/pull/new/kana-develop
    remote:
    To https://github.com/Giganscudo-Duro/study-git-command.git
     * [new branch]      kana-develop -> kana-develop
    Branch 'kana-develop' set up to track remote branch 'kana-develop' from 'origin'.
    ```

`git branch` コマンドを実行し、リモートリポジトリに kana-develop が追加されたことを確認できたら、手順8は完了。
```sh
$ git branch -a
  develop
* kana-develop
  master
  remotes/origin/HEAD -> origin/master
  remotes/origin/develop
  remotes/origin/kana-develop  ← リモートリポジトリにも kana-develop が追加されている
  remotes/origin/master
```


## 手順 9：各開発者が、自分用ブランチで色々開発する
まぁ開発対象の規模次第と、各開発者の考え方次第では、一回の開発において push を複数回行うことがあるかもしれない。  
その時の対応を一応記録しておく。  
今回は kana-develop ブランチ上で、色々ファイルを新規作成したと仮定する。

`git branch` コマンドを実行し、どのブランチに自分がいるのかを確認する。
```sh
$ git branch -a
  develop
* kana-develop  ← ローカルリポジトリの kana-develop にいる
  master
  remotes/origin/HEAD -> origin/master
  remotes/origin/develop
  remotes/origin/kana-develop  ← すでにリモートリポジトリに kana-develop を作成してる
  remotes/origin/master
```

この状態で、色々ファイルを新規作成し、開発が一通り完了したと仮定する。
```sh
$ touch new-develop
$ mkdir yobikata
$ touch yobikata/kana-chan
$ touch yobikata/kana-kun
$ touch yobikata/kana-san
$ touch yobikata/kana-sama
```

開発内容をリモートリポジトリに反映させるため、以下の４つのステップを実行。

1. `git status` コマンドで、今回の開発で変更を加えたファイルを確認  
    開発マシン上で、以下のコマンドを実行する。
    ```sh
    $ git status
    ブランチ kana-develop
    Your branch is up to date with 'origin/kana-develop'.
    
    追跡されていないファイル:
      (use "git add <file>..." to include in what will be committed)
    
            new-develop
            yobikata/
    
    nothing added to commit but untracked files present (use "git add" to track)
    ```

2. `git add` コマンドで、変更を加えたファイルをインデックスに追加  
    開発マシン上で、以下のコマンドを実行する。
    ```sh
    $ git add new-develop
    $ git add yobikata/
    ```
    ちなみに、今のステータスはこんな感じ。
    ```sh
    $ git status
    ブランチ kana-develop
    Your branch is up to date with 'origin/kana-develop'.
    
    コミット予定の変更点:
      (use "git reset HEAD <file>..." to unstage)
    
            new file:   new-develop
            new file:   yobikata/kana-chan
            new file:   yobikata/kana-kun
            new file:   yobikata/kana-sama
            new file:   yobikata/kana-san
    ```

3. `git commit` コマンドで、ローカルリポジトリにコミット  
    開発マシン上で、以下のコマンドを実行する。  
    指定する文字列部には、「変更内容」を入力する。
    ```sh
    $ git commit -m "Update kana-develop branch"
    [kana-develop da96920] Update kana-develop branch
     5 files changed, 0 insertions(+), 0 deletions(-)
     create mode 100644 new-develop
     create mode 100644 yobikata/kana-chan
     create mode 100644 yobikata/kana-kun
     create mode 100644 yobikata/kana-sama
     create mode 100644 yobikata/kana-san
    ```

4. `git push` コマンドで、ローカルリポジトリの内容をリモートリポジトリに反映  
    開発マシン上で、以下のコマンドを実行する。
    ```sh
    $ git push
    Username for 'https://github.com': <E-mail>
    Password for 'https://<E-mail>@github.com':
    Counting objects: 4, done.
    Delta compression using up to 2 threads.
    Compressing objects: 100% (3/3), done.
    Writing objects: 100% (4/4), 395 bytes | 197.00 KiB/s, done.
    Total 4 (delta 0), reused 0 (delta 0)
    To https://github.com/Giganscudo-Duro/study-git-command.git
       3bcbb14..da96920  kana-develop -> kana-develop
    ```

ここまで実施したら、手順9は完了。

## 手順 10：各開発者が、GitHub 上で PullRequest を発行する
今回は「kana-develop」ブランチの変更内容を、「develop」ブランチにマージする。

1. Git Hub 上で [Pull requests] タブをクリックして画面を切り替える。
2. [New pull request] ボタンをクリックし、Compare changes の画面を表示する。
3. Compare changes 画面で以下の情報を入力し、[Create pull request] ボタンをクリックする。
    | 項目 | 作業内容 |
    |------|----------|
    | base    | マージ先。今回は develop ブランチを指定する。             |
    | compare | マージ対象。今回は kana-develop ブランチを指定する。      |
4. Open a pull request 画面で変更内容の説明を記述し、[Create pull request] ボタンをクリックする。

ここまで実施したら、手順10は完了。


## 手順 11：開発メンバによるレビューが行われる
各開発者や、レビュー担当者がレビューを行う。

## 手順 12：マージをコンプリートさせる
今回は、私一人のチームなので、自分でやる。

1. Git Hub 上で [Pull requests] タブをクリックして画面を切り替える。
2. 画面上に一覧で表示されてるプルリクエストをクリックする。
3. クリックしたプルリクエストの内容を確認し、問題なければ [Merge pull request] ボタンをクリックする。
4. ホントにマージしてよいかの確認が求められるので [Confirm merge] ボタンをクリックする。

これで手順１２は完了。


## 手順 13：開発者全員の担当がマージされたら、手順 4 に戻る
まぁ特に言うことは無い。




















# トラブルシューティング




## `git push` を実行したら「fatal: The current branch <ブランチ名> has no upstream branch.」
何の指定もなしに `git push` コマンドだけを実行する場合、成功するときと失敗する時がある。  
結論から言うとこれは、**`push` しようとしたブランチに「上流ブランチ（upstream branch）」が無い** のが原因。  
解決策は、*push する際に`git push --set-upstream` といった具合にオプションを付けて、上流ブランチを設定する* こと。

ちなみに原因確認の鍵である 上流ブランチ は `git branch -vv` コマンドで確認する事ができる。

- 成功するパターン
    まずは、`git brach -vv` を実行する。
    ```sh
    $ git branch -vv
    * develop d1c749e [origin/develop] gitの使い方を更新
      master  0cadf77 [origin/master] first commit
    ```
    そんで push してみると...
    ```sh
    $ git push
    Username for 'https://github.com': <E-mail>
    Password for 'https://<E-mail>@github.com':
    Everything up-to-date
    ```
    エラーは起きない。


- 失敗するパターン
    まずは、`git brach -vv` を実行する。
    ```sh
    $ git branch -vv
      develop      c7b415d [origin/develop] create develop branch
    * kana-develop 35a3d79 Update kana-develop branch
      master       40857fc [origin/master] Create master branch
    ```
    そんで push してみると...
    ```sh
    $ git push
    fatal: The current branch kana-develop has no upstream branch.
    To push the current branch and set the remote as upstream, use
    
        git push --set-upstream origin kana-develop
    ```
    エラーが起きた。

何が違うのかというと、`[origin/XXXXX]` という形式で表示された上流ブランチがあるかないか、という点。
```sh
$ git branch -vv
  develop      c7b415d [origin/develop] create develop branch
* kana-develop 35a3d79 Update kana-develop branch  ← [origin/XXXXX] という記述が存在してない
  master       40857fc [origin/master] Create master branch
```

上流ブランチの簡単な説明は、以下で確認できる。
```sh
$ git push -h
...(snip)...
       -u, --set-upstream
           For every branch that is up to date or successfully pushed, add upstream (tracking)
           reference, used by argument-less git-pull(1) and other commands. For more information,
           see branch.<name>.merge in git-config(1).
```

まぁ何というか、「引数なしで `git pull` などのコマンドを実行するために必要な upstream branch を設定する」というオプションみたい。
毎回オプションを指定するのは面倒なので、素直にオプションつけて `git push` を実行し、上流ブランチを設定すれば OK。
```sh
$ git push --set-upstream origin kana-develop
Username for 'https://github.com': <E-mail>
Password for 'https://<E-mail>@github.com':
Counting objects: 4, done.
Delta compression using up to 2 threads.
Compressing objects: 100% (3/3), done.
Writing objects: 100% (4/4), 395 bytes | 395.00 KiB/s, done.
Total 4 (delta 0), reused 0 (delta 0)
To https://github.com/Giganscudo-Duro/test-git-command.git
   34d60d8..35a3d79  kana-develop -> kana-develop
Branch 'kana-develop' set up to track remote branch 'kana-develop' from 'origin'.
```
はい、これで上流ブランチが kana-develop にも追加されました。
```sh
$ git branch -vv
  develop      c7b415d [origin/develop] create develop branch
* kana-develop 35a3d79 [origin/kana-develop] Update kana-develop branch
  master       40857fc [origin/master] Create master branch
```











