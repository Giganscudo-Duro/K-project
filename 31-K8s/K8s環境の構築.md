# 参考URL






# お試し環境









                 +------------+            +-------------+           +-------------+
                 | K8s-Master |            | K8s-Worker1 |           | K8s-Worker2 |
                 +------+-----+            +------+------+           +------+------+
                        | 192.168.122.15           | 192.168.122.91         | 192.168.122.
 ---------+-------------+--------------------------+------------------------+----------- 192.168.122.0/24
          |
    +-----+-----+
    |   HIEMS   |
    | (KVMhost) |
    +-----------+


# 構築手順

## hosts ファイルへの追記
クラスタを構成するマスターノードとワーカーノードについて名前解決する。  
K8s-Master、K8s-Worker それぞれの /etc/hosts` を編集する。

- `/etc/hosts
    ```
    192.168.122.15 k8s-master
    192.168.122.91 k8s-worker1
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







