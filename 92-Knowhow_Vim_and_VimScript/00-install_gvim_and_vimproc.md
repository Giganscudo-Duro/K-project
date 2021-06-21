# 実行環境
Ubuntu




# neobundle インストール

neobundle を利用する場合は以下の手順を踏むことになる。
（まぁ正直、今から使うならば dein の方がいい気もするが...）

0. 各種下準備
1. git から neobundle のソースコードを入手
2. neobundle をビルド＆インストール



## 0. 事前準備

git 利用に必要なパッケージ、neobundle のビルドに必要なパッケージをインストールする。
[参考URL - make時に「/bin/sh: cc: コマンドが見つかりません」と怒られた時の対処法]( https://sujico.net/2019/03/27/make%E6%99%82%E3%81%AB%E3%80%8C-bin-sh-cc-%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%81%8C%E8%A6%8B%E3%81%A4%E3%81%8B%E3%82%8A%E3%81%BE%E3%81%9B%E3%82%93%E3%80%8D%E3%81%A8%E6%80%92%E3%82%89%E3%82%8C/ )
```
$ sudo apt install git
$ sudo apt install make gcc
```





## 1. git から neobundle のソースコードを入手

先ずは neobundle 用のディレクトリを用意し、そこに github からソースコードを取得して格納する。
```
$ mkdir -p ~/.vim/bundle
$ git clone https://github.com/Shougo/neobundle.vim ~/.vim/bundle/neobundle.vim
```




## 2. neobundle をビルド＆インストール

`.vimrc` に対し、以下の記述を追加する。

```
"---------------------------
" Start Neobundle Settings.
"---------------------------
" bundleで管理するディレクトリを指定
set runtimepath+=~/.vim/bundle/neobundle.vim/

" Required:
call neobundle#begin(expand('~/.vim/bundle/'))

" neobundle自体をneobundleで管理
NeoBundleFetch 'Shougo/neobundle.vim'

" ここから下に、追加のプラグインを書き加えていく

NeoBundle 'Shougo/vimproc', {
      \ 'build' : {
      \     'windows' : 'make -f make_mingw32.mak',
      \     'cygwin' : 'make -f make_cygwin.mak',
      \     'mac' : 'make -f make_mac.mak',
      \     'unix' : 'make -f make_unix.mak',
      \    },
      \ }


" ここまで
call neobundle#end()

" Required:
filetype plugin indent on

" 未インストールのプラグインがある場合、インストールするかどうかを尋ねてくれるようにする設定
" 毎回聞かれると邪魔な場合もあるので、この設定は任意です。
NeoBundleCheck

"-------------------------
" End Neobundle Settings.
"-------------------------
```






### 補足1）


```
NeoBundle 'Shougo/vimproc', {
      \ 'build' : {
      \     'windows' : 'make -f make_mingw32.mak',
      \     'cygwin' : 'make -f make_cygwin.mak',
      \     'mac' : 'make -f make_mac.mak',
      \     'unix' : 'make -f make_unix.mak',
      \    },
      \ }
```






# その他
https://satoru739.hatenadiary.com/entry/20111007/1318086532
https://packages.ubuntu.com/ja/xenial/ppc64el/packagekit-gtk3-module/filelist
```
$ sudo apt install packagekit-gtk3-module
```


