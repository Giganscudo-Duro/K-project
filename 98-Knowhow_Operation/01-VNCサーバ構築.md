# 参考URL

- [CentOS7にWindowsからVNCで接続する方法 - Qiita](https://qiita.com/SkyLaptor/items/48f1bd38f728199ed485)



# 構築手順(RHEL系)

## VNC関連パッケージのインストール
```sh
# yum install -y tigervnc-server
```

## VNCサーバ用のパスワード設定
vnc接続させたいユーザにログインした状態で、以下のコマンドを実行。
```sh
$ vncpasswd
--[result]---
Password:
Verify:
Would you like to enter a view-only password (y/n)? y
Password:
Verify:
```


## ファイアウォールの設定を変更
基本的に VNC は TCP の「5900＋セッション番号」のポートを利用する。
今回はセッション１しか使わないので「5901番ポート」を使うことにあるので、そこを開ける。
```sh
# firewall-cmd --add-port=5901/tcp --permanent
# firewall-cmd --reload
```

設定が反映されたかチェックするため、以下のコマンドを実行
```sh
# firewall-cmd --list-all
--[result]---
FedoraWorkstation (active)
  target: default
  icmp-block-inversion: no
  interfaces: wlp2s0
  sources:
  services: dhcpv6-client mdns samba-client ssh
  ports: 1025-65535/udp 1025-65535/tcp 5901/tcp
  protocols:
  masquerade: no
  forward-ports:
  source-ports:
  icmp-blocks:
  rich rules:
```

## VNCサーバを起動
セッション番号１を指定して、一時的にサーバを起動する。
```sh
$ vncserver :1
```







