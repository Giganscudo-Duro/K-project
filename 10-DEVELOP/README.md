# vim を使いながら、ターミナルを利用可能にする。

- https://mongonta.com/f275-howto-use-vim-terminal/
- https://vim-jp.org/vimdoc-ja/terminal.html

基本的には Vim 上ではいかを実行すればよい。
```
:terminal
```

詳しい使い方はマニュアルを見ましょう。とりあえず使う分には下記のコマンドを覚えればいいと思います。
```
機能	コマンド
ウィンドウの切り替え	Ctrl+w Ctrl+w
Exコマンドを使う	Ctrl+w :
ウィンドウを閉じる。
※ジョブ実行中は不可	　Ctrl+w :quit
Terminal Normalモードに移行	Ctrl+w N
またはCtrl+\ Ctrl+n
ジョブを停止する	Ctrl+w Ctrl+c
Terminal Jobモードに戻る	iやaなど、挿入モードに入る操作
現在カーソルがあるウィンドウと１つ前のウィンドウを入れ替える。	Ctrl+w x

★TerminalNormalモード
　Vimのノーマルモードの操作ができるようになり、出力結果のコピー等が行えます。


```






