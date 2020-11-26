" 折り畳みを有効に {{{XXXXX}}}
set foldmethod=marker

" カラースキームの設定
colorscheme torte


" vimによる自動改行を止める
set tw=0

" tab 数を4文字で
set tabstop=4	


" 行番号を出力する
set nu
" set nonu


" 現在の行を強調表示
set cursorline
" 現在の行を強調表示（縦）
" set cursorcolumn

" 自動改行を有効に
set autoindent


" vimgrep をより便利に
autocmd QuickFixCmdPost *grep* cwindow
map <C-n> :cn<CR>
map <C-p> :cp<CR>


" 検索時の文字列をハイライトするか否か
" set nohlsearch	" ハイライトしない
set hlsearch	" ハイライトする
nnoremap <ESC><ESC> :nohlsearch<CR>	" ESCを２回叩くとハイライト解除


" 全角野スペースをハイライト
highlight ZenkakuSpace cterm=underline ctermfg=lightblue guibg=#666666
au BufNewFile,BufRead * match ZenkakuSpace /　/


" 入力中のコマンドをステータスに表示する
set showcmd


" 検索語が画面の真ん中に来るようにする
nmap n nzz 
nmap N Nzz 
nmap * *zz 
nmap # #zz 
nmap g* g*zz 
nmap g# g#zz


" タブ利用時のショートカット
nnoremap <C-l> :tabnext<CR>
nnoremap <C-h> :tabprevious<CR>


" ファイル名を表示する
set statusline+=%F
set statusline+=%m
set statusline+=%r
set statusline+=%h
set statusline+=%w
set statusline+=%=
set statusline+=(^o^)
set statusline+=\ 
set statusline+=[ENC=%{&fileencoding}]
set statusline+=[%l/%L]
set laststatus=2
