# 概要
基本的に Linux 環境を構築する際に、毎回設定するのが面倒になる。  
だからとりあえず自分用のドットファイルをすぐに導入できるような仕組みが欲しかった。  


# CentOS 系の場合
```sh
curl https://raw.githubusercontent.com/Giganscudo-Duro/K-project/develop/99-Knowhow_DotFile/00-Linux/vimrc -o ~/.vimrc
curl https://raw.githubusercontent.com/Giganscudo-Duro/K-project/develop/99-Knowhow_DotFile/00-Linux/screenrc -o ~/.screenrc

sudo dnf install -y epel-release
sudo dnf --enablerepo=epel install -y screen
```
