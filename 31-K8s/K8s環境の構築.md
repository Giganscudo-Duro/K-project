# 参考URL
- [Creating a cluster with kubeadm - Kubernetes](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- [Ubuntu 18.04 LTS にDocker環境をインストールする - Qiita](https://qiita.com/soumi/items/5b01d88c187b678c0474)
- [Ubuntu 18.04 LTS にKubernetes環境をインストールする [Master / Worker] - Qiita](https://qiita.com/soumi/items/7736ac3aabbbe4fb474a)
- [防火壁の中の Docker - Qiita](https://qiita.com/jeffi7/items/3e40c59744b5801fd40a)
- [Ubuntu 18.04 に kubernetes をインストールする - Qiita](https://qiita.com/ysaito8015@github/items/26a208f9c482b2d2d24a)
- [kubeadmのインストール - Kubernetes](https://kubernetes.io/ja/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
- []()
- []()
# 参考書籍
- [Docker実践ガイド]



# お試し環境

## 実施環境
基本的に、KVM 環境上に作成する。

- KVM ホスト
    |項目|概要|
    |--|--|
    |OS| fedora32 |
    |CPU|4コア|
    |メモリ|16GB|

- クラスタを構成するノード
    |項目|概要|
    |--|--|
    |OS| Ubuntu18.04 |
    |vCPU|2|
    |メモリ|4GB|




## ネットワーク構成
```
             +------------+            +-------------+           +-------------+
             | K8s-Master |            | K8s-Worker1 |           | K8s-Worker2 |
             +------+-----+            +------+------+           +------+------+
                    | 192.168.122.15           | 192.168.122.91         | 192.168.122.
 ---------+---------+--------------------------+------------------------+----------- 192.168.122.0/24
          |
    +-----+-----+
    |   HIEMS   |
    | (KVMhost) |
    +-----------+
```

# 構築手順

## hosts ファイルへの追記
クラスタを構成するマスターノードとワーカーノードについて名前解決する。  
K8s-Master、K8s-Worker それぞれの /etc/hosts` を編集する。

- `/etc/hosts
    ```
    192.168.122.15 k8s-master k8s-master.kana.com
    192.168.122.91 k8s-worker1 k8s-worker1.kana.com
    ```



## ファイアウォールの無効化＆ SELinux の無効化
どうせ閉じたプライベートネットワークなので、Firewall と SELinux を無効化し、構築手順を簡単にする。  
と思ったけど、Ubuntu だと、そういうのないみたいなので、割愛。


## カーネルパラメータの設定
ネットワークプラグインを使ってコンテナ(Pod) が通信をする際、iptables プロキシにルーティングされるよう、カーネルパラメータを設定する。  
また、IPVS による負荷分散機能を有効にするため、カーネルモジュールをロードする。
K8s-Master、K8s-Worker それぞれにおいて、以下の手順を実行。

1. `/etc/sysctl.d/k8s.conf` を作成
    ```
    net.bridge.bridge-nf-call-ip6tables = 1
    net.bridge.bridge-nf-call-iptables = 1
    net.ipv4.ip_forward = 1
    ```
2. 以下のコマンドを実行して、カーネルパラメータを読み込む
    ```sh
    # sysctl --system
    ```
3. カーネルモジュールをロードするため、以下のコマンドを実行。
    ```sh
    modprobe -v ip_vs
    modprobe -v ip_vs_rr
    modprobe -v ip_vs_sh
    modprobe -v ip_vs_wrr
    ```
4. 設定ファイルを書き換えるため、`/etc/modules-load.d/ip_vs.conf` を編集。
    ```
    ip_vs
    ip_vs_rr
    ip_vs_sh
    ip_vs_wrr
    ```

## スワップの無効化
K8s クラスタでは、全ノードの スワップ領域を無効化しておく必要がある。  
K8s-Master、K8s-Worker それぞれにおいて、以下の手順を実行。

1. スワップパーティションを確認するため、以下のコマンドを実行
    ```sh
    # cat /proc/swaps
    ```
2. ファイルシステム上の swap 領域を無効とする設定にするため、`/etc/fstab` を編集
    ```
    # /etc/fstab
    # Created by anaconda on Wed Sep  2 14:28:16 2020
    #
    # Accessible filesystems, by reference, are maintained under '/dev/disk/'.
    # See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info.
    #
    # After editing this file, run 'systemctl daemon-reload' to update systemd
    # units generated from this file.
    #
    /dev/mapper/hiems-root  /                       ext4    defaults        1 1
    UUID=52bd7de7-e137-4b6c-b969-876aed01fbfa /boot                   ext4    defaults        1 2
    UUID=2274-6E0B          /boot/efi               vfat    umask=0077,shortname=winnt 0 2
    /dev/mapper/hiems-home  /home                   ext4    defaults        1 2
    /dev/mapper/hiems-swap  none                    swap    defaults        0 0     <----- swap に関してコメントアウト
    ```
3. 実際にスワップを無効にするため、以下のコマンドを実行
    ```sh
    # swapoff -a
    ```
4. 実際に swap 領域が無効になっていることを確認するため、以下のコマンドを実行
    ```sh
    # cat /proc/swaps
    Filename                                Type            Size    Used    Priority
    
    # free -h
                  total        used        free      shared  buff/cache   available
    Mem:           1.9G        381M        310M        1.5M        1.3G        1.4G
    Swap:            0B          0B          0B
    ```


## Docker エンジンのインストール

ちょっと Docker 公式の Repository から Docker をインストールすることにする。  
まぁ Kubernetes で利用可能な Docker はバージョンが決まってるし、公式のほうが選択肢が多いと思う。  
K8s-Master、K8s-Worker それぞれにおいて、以下の手順を実行。

1. 必要なパッケージをインストールするため、以下のコマンドを実行
    ```sh
    # apt update
    # apt install apt-transport-https curl
    ```
2. GPG 公開鍵をインストールするため、以下のコマンドを実行
    ```sh
    # curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    ```
3. Docker 公式の Repository を設定するため、以下のコマンドを実行
    ```sh
    # add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
       $(lsb_release -cs) \
       stable"
    ```
4. Docker-ce をインストールするため、以下のコマンドを実行
    ```sh
    # apt install docker-ce
    ```

## Docker デーモンの設定変更
Docker デーモンに関する設定ファイルを編集する。  
Kubernetes では Docker と kubelete において、使用する cgroup ドライバが一致していなければならない。  
K8s-Master、K8s-Worker それぞれにおいて、以下の手順を実行。
```sh
# vim /etc/docker/daemon.json
-----
{
    "exec-opts": ["native.cgroupdriver=systemd"],
    "storage-driver": "overlay2"
}
```


## Docker エンジンが利用するプロキシサーバの編集
ここでプロキシサーバの設定をする必要があるが、今回は無視。
やる場合は、K8s-Master、K8s-Worker それぞれにおいて、以下の手順を実行。

```sh
#  mkdir -p /usr/lib/systemd/system/docker.service.d/
# vim /usr/lib/systemd/system/docker.service.d/http-proxy.conf
-----
[Service]
Environment="HTTP_PROXY=http://proxy.my.site.com:8080"
Environment="HTTPS_PROXY=http://proxy.my.site.com:8080"
Environment="NO_PROXY=127.0.0.1,localhost,.kana.com"
```


## 設定のロードと Docker デーモンのリスタート
K8s-Master、K8s-Worker それぞれにおいて、以下の手順を実行。



## Kubernetes をインストール
K8s-Master、K8s-Worker それぞれにおいて、以下の手順を実行。

1. Kubernetes の GPG 鍵とRepositoryを登録するため、以下のコマンドを実行
    ```sh
    # curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
    # apt-add-repository "deb https://apt.kubernetes.io/ kubernetes-xenial main"
    ```

2. kubeadm をインストールするため、以下のコマンドを実行
    ```sh
    # apt update
    # apt install kubeadm
    ```

3. サービス自動起動を有効にするため、以下のコマンドを実行
```sh
# systemctl enable kubelet
```












