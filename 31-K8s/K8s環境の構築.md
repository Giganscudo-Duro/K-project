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

# 構築準備（共通部）

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
そうしないと、kubelet サービスが起動しない実装になったらしい。  
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






# 構築準備（マスターノード）


## 初期化処理のドライラン
初期化処理する際、以下の環境情報を指定することになる


||||
|--|--|--|
| kubernetes-version            | 1.19.1        | `kubectl version --short  -o json` コマンドで事前に確認 |
| apiserver-advertise-address   |               | `ip a` コマンドで事前に確認 |
| service-cidr                  | 10.96.0.0/12  | サービス用のネットワーク、指定しないとデフォルトで「10.96.0.0/12」が割り当たる |
| pod-network-cidr              | 10.224.0.0/16 | コンテナが利用するオーバレイネットワーク。指定しないとデフォルトで「10.224.0.0/16」が割り当たる |
| token-ttl                     | 0             | 認証トークンの利用期限、「0」を指定すると無期限になる |

ここで、指定してるオーバーレイネットワークの初期値だけど、flannel を利用する場合、flannel インストール時に使う yaml ファイルにデフォルトで書かれてるのが「10.224.0.0/16」。  
だから、下手に書き換えなくても問題ないよう、最初から設定することにした。






上記の諸々を実際に初期化する前にチェックする「ドライラン」を実行する。  
K8s-Master 上で、以下の手順を実行。

まず、IP を取得
```sh
# IP_MASTER=$(ip -f inet -o addr show enp1s0 | cut -d' ' -f 7 | cut -d/ -f 1)
# echo $IP_MASTER
```

次に Kubernetes のバージョンを取得
```sh
# kubectl version --short  -o json
```


```sh
# kubeadm init \
    --kubernetes-version 1.19.1 \
    --apiserver-advertise-address=${IP_MASTER} \
    --service-cidr=10.96.0.0/12 \
    --pod-network-cidr=10.224.0.0/16 \
    --token-ttl 0 \
    --dry-run | tee ./dry-run.log
```

実際に実行するとこんな感じになる。


<details><summary>実行結果</summary><div>

```sh
# kubeadm init \
    --kubernetes-version 1.19.1 \
    --apiserver-advertise-address=${IP_MASTER} \
    --service-cidr=10.96.0.0/12 \
    --pod-network-cidr=10.224.0.0/16 \
    --token-ttl 0 \
    --dry-run | tee ./dry-run.log
--[実行結果]-----------------------------------------------------------
[init] Using Kubernetes version: v1.19.1
[preflight] Running pre-flight checks
[preflight] Would pull the required images (like 'kubeadm config images pull')
[certs] Using certificateDir folder "/etc/kubernetes/tmp/kubeadm-init-dryrun967583171"
[certs] Generating "ca" certificate and key
[certs] Generating "apiserver" certificate and key
[certs] apiserver serving cert is signed for DNS names [k8s-master kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 192.168.122.15]
[certs] Generating "apiserver-kubelet-client" certificate and key
[certs] Generating "front-proxy-ca" certificate and key
[certs] Generating "front-proxy-client" certificate and key
[certs] Generating "etcd/ca" certificate and key
[certs] Generating "etcd/server" certificate and key
[certs] etcd/server serving cert is signed for DNS names [k8s-master localhost] and IPs [192.168.122.15 127.0.0.1 ::1]
[certs] Generating "etcd/peer" certificate and key
[certs] etcd/peer serving cert is signed for DNS names [k8s-master localhost] and IPs [192.168.122.15 127.0.0.1 ::1]
[certs] Generating "etcd/healthcheck-client" certificate and key
[certs] Generating "apiserver-etcd-client" certificate and key
[certs] Generating "sa" key and public key
[kubeconfig] Using kubeconfig folder "/etc/kubernetes/tmp/kubeadm-init-dryrun967583171"
[kubeconfig] Writing "admin.conf" kubeconfig file
[kubeconfig] Writing "kubelet.conf" kubeconfig file
[kubeconfig] Writing "controller-manager.conf" kubeconfig file
[kubeconfig] Writing "scheduler.conf" kubeconfig file
[kubelet-start] Writing kubelet environment file with flags to file "/etc/kubernetes/tmp/kubeadm-init-dryrun967583171/kubeadm-flags.env"
[kubelet-start] Writing kubelet configuration to file "/etc/kubernetes/tmp/kubeadm-init-dryrun967583171/config.yaml"
[control-plane] Using manifest folder "/etc/kubernetes/tmp/kubeadm-init-dryrun967583171"
[control-plane] Creating static Pod manifest for "kube-apiserver"
[control-plane] Creating static Pod manifest for "kube-controller-manager"
[control-plane] Creating static Pod manifest for "kube-scheduler"
[dryrun] Would ensure that "/var/lib/etcd" directory is present
[etcd] Creating static Pod manifest for local etcd in "/etc/kubernetes/tmp/kubeadm-init-dryrun967583171"
[dryrun] Wrote certificates, kubeconfig files and control plane manifests to the "/etc/kubernetes/tmp/kubeadm-init-dryrun967583171" directory
[dryrun] The certificates or kubeconfig files would not be printed due to their sensitive nature
[dryrun] Please examine the "/etc/kubernetes/tmp/kubeadm-init-dryrun967583171" directory for details about what would be written
[dryrun] Would write file "/etc/kubernetes/manifests/kube-apiserver.yaml" with content:

...(snip)...

[addons] Applied essential addon: kube-proxy

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/tmp/kubeadm-init-dryrun967583171/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 192.168.122.15:6443 --token tblh5r.kqgz7uwgzhhycjbz \
    --discovery-token-ca-cert-hash sha256:9a548b31646e1c5657de642118803094c2a9c561b75cbb5b1bd0c002f63c8884
```
</div></details>



とりあえず、成功してるっぽい。




## 初期化処理の実行

ドライランで大したエラーも出なかったので、実際に初期化を行う。
先程のコマンドから、「--dry-run」オプションを除いた以下のコマンドを実行する。
```sh
# kubeadm init \
    --kubernetes-version 1.19.1 \
    --apiserver-advertise-address=${IP_MASTER} \
    --service-cidr=10.96.0.0/12 \
    --pod-network-cidr=10.224.0.0/16 \
    --token-ttl 0 \
    | tee ./kubeadm_init.log
```

実際に実行するとこんな感じになる。


<details><summary>実行結果</summary><div>

```sh
# kubeadm init \
    --kubernetes-version 1.19.1 \
    --apiserver-advertise-address=${IP_MASTER} \
    --service-cidr=10.96.0.0/12 \
    --pod-network-cidr=10.224.0.0/16 \
    --token-ttl 0 \
    | tee ./dry-run.log
--[実行結果]-----------------------------------------------------------

[init] Using Kubernetes version: v1.19.1
[preflight] Running pre-flight checks
[preflight] Pulling images required for setting up a Kubernetes cluster
[preflight] This might take a minute or two, depending on the speed of your internet connection
[preflight] You can also perform this action in beforehand using 'kubeadm config images pull'
[certs] Using certificateDir folder "/etc/kubernetes/pki"
[certs] Generating "ca" certificate and key
[certs] Generating "apiserver" certificate and key
[certs] apiserver serving cert is signed for DNS names [k8s-master kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 192.168.122.15]
[certs] Generating "apiserver-kubelet-client" certificate and key
[certs] Generating "front-proxy-ca" certificate and key
[certs] Generating "front-proxy-client" certificate and key
[certs] Generating "etcd/ca" certificate and key
[certs] Generating "etcd/server" certificate and key
[certs] etcd/server serving cert is signed for DNS names [k8s-master localhost] and IPs [192.168.122.15 127.0.0.1 ::1]

...(snip)...

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 192.168.122.15:6443 --token a0hrht.5ut19mrs3y56dg0o \
    --discovery-token-ca-cert-hash sha256:a5e5b9e6ed9c15a8a6c0446e6a970e5a9c44b5e91dc6da163d5d15f49234c5f2
```
</div></details>

`Your Kubernetes control-plane has initialized successfully!` が出力されれば、だいたいおk。


そんで、実行結果に含まれるシェルスクリプトをとりあえず、以下のように書き出しておく。  
これは後でノード追加に使う。

- `kubeadm_join.sh`
    ```sh
    #!/bin/bash
    kubeadm join 192.168.122.15:6443 --token a0hrht.5ut19mrs3y56dg0o \
      --discovery-token-ca-cert-hash sha256:a5e5b9e6ed9c15a8a6c0446e6a970e5a9c44b5e91dc6da163d5d15f49234c5f2
    ```

あと、各種設定ファイルを保存するため、実行結果中にある以下のコマンドを実行。

```sh
# mkdir -p $HOME/.kube
# cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
# chown $(id -u):$(id -g) $HOME/.kube/config
```


## flannel をインストール
CNI（Container Network Interface）プラグインをインストールする。  
今回は、Kubernetes 界隈でよく使われてるという flannel を利用する。  

とりあえず、flannel の yaml ファイルを入手する。

社内で実行するならば、とりあえず環境変数としてプロキシ情報を設定する。
```sh
# export http_proxy=http://hogehoge.com:8080
# export https_proxy=http://hogehoge.com:8080
```

とりあえず yaml 入手するため、以下のコマンドを追加。
```sh
# curl -sSL -O https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

まぁファイルを見たらわかるけど、ネットワークアドレスとして「10.244.0.0/16」が埋め込まれてる。

それでは、このファイルを使って、flannel をクラスタに配備する。

社内で実行するならば、プロキシ情報を無効化するため、以下のコマンドを実行する
```sh
# unset http_proxy
# unset https_proxy
```

インストールのために、以下のコマンドを実行。
```sh
# kubectl create -f ./kube-flannel.yml
```


## 現時点での状態を確認

ノードの状態を確認するため、以下のコマンドを実行。
```sh
# kubectl get nodes
--[実行結果]-----------------------------------------------------------
NAME         STATUS   ROLES    AGE   VERSION
k8s-master   Ready    master   28m   v1.19.1
```

サービスの状態を確認するため、以下のコマンドを実行。
```sh
# kubectl get pods --all-namespaces
--[実行結果]-----------------------------------------------------------
NAMESPACE     NAME                                 READY   STATUS    RESTARTS   AGE
kube-system   coredns-f9fd979d6-m6s79              1/1     Running   0          30m
kube-system   coredns-f9fd979d6-rjn86              1/1     Running   0          30m
kube-system   etcd-k8s-master                      1/1     Running   0          30m
kube-system   kube-apiserver-k8s-master            1/1     Running   0          30m
kube-system   kube-controller-manager-k8s-master   1/1     Running   0          30m
kube-system   kube-flannel-ds-amd64-c726b          1/1     Running   0          2m58s
kube-system   kube-proxy-klxlf                     1/1     Running   0          30m
kube-system   kube-scheduler-k8s-master            1/1     Running   0          30m
```

一通り動いてるっぽい。  
念の為、OS を再起動してもOKか、確認しておく。


# 構築準備（Worker）

さきほど、作成したシェルスクリプトを、Worker ノードに複製する。

- `kubeadm_join.sh`
    ```sh
    #!/bin/bash
    kubeadm join 192.168.122.15:6443 --token a0hrht.5ut19mrs3y56dg0o \
      --discovery-token-ca-cert-hash sha256:a5e5b9e6ed9c15a8a6c0446e6a970e5a9c44b5e91dc6da163d5d15f49234c5f2
    ```

そんで、そのシェルスクリプトを実行する。

```sh
# ./kubeadm_join.sh
--[実行結果]-----------------------------------------------------------
[preflight] Running pre-flight checks
[preflight] Reading configuration from the cluster...
[preflight] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -oyaml'
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Starting the kubelet
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap...

This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the control-plane to see this node join the cluster.
```

これで、ノードがクラスタに追加されたはず。  

Master ノード上で以下のコマンドを実行し、確認してみる。

```sh
root@K8s-Master:~# kubectl get nodes
--[実行結果]-----------------------------------------------------------
NAME          STATUS   ROLES    AGE     VERSION
k8s-master    Ready    master   54m     v1.19.1
k8s-worker1   Ready    <none>   2m21s   v1.19.1
```

同じ要領でノードをいっぱい増やせる。  
ひとまずコレで環境構築はおしまい。



























