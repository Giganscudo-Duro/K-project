# fedora の場合


## まずインストール
```sh
# yum install -y bash-completion vim screen libvirt virt-manager gnome-tweaks
```


## ssh 接続に必要な設定を実施
```
# firewall-cmd --add-port=22/tcp --permanent
# firewall-cmd --reload
# systemctl enable sshd
# systemctl start sshd
```



















# ubuntu の場合


## まずインストール
```sh
# apt install -y vim screen
```

## ssh 接続に必要な設定を実施
```
# apt install ssh
# systemctl start ssh
```


## docker のインストール
参考：https://qiita.com/iganari/items/fe4889943f22fd63692a

とりあえずパッケージリストのアップデート
```
# apt update
```

HTTPS経由でrepositoryをやりとり出来るようにするためのパッケージをインストール
```
# apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
```


Dockerの公式GPG keyを追加する
```
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

repository( stable ) を追加する
```
# add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
```

docker をインストール
```
# apt install -y docker-ce
```

























