# 参考URL

https://qiita.com/t-sin/items/40c9fef72751de77635a  
https://qiita.com/takeshinoda@github/items/2dec7a72930ec1f658af  
https://qiita.com/matagawa/items/31e26e9cd53c3e61ae07  
https://qiita.com/rururu_kenken/items/5a7b94146cf0a2eb537d  
https://auth0.com/blog/jp-refresh-tokens-what-are-they-and-when-to-use-them/  
https://qiita.com/namikitakeo/items/cfb66928fad8882ea25a  
https://www.keycloak.org/docs-api/5.0/rest-api/index.html  
https://qiita.com/namikitakeo/items/cfb66928fad8882ea25a  

# 構成図

```
       +----------------------------------------------------------+
       |    +----------+        +------------+                    |
       |    | KeyCloak |        | Service    |                    |
       |    |          |        |   Provider |                    |
       |    +----+-----+        +---+--------+                    |
       |         | 172.17.0.3       | 172.17.0.3                  |
       |         |                  |                             |
       |    -----+-------+----------+---------- 172.17.0.0/16     |
       |                 |                                        |
       |                 | 172.17.0.1                             |
       |         +-------+-------+                                |
       |         | Docker engine |                                |
       |         +---------------+                                |
       |                                                          |
       +------------------+---------------------------------------+
                          | 192.168.122.153(KVM 仮想マシン)
                          |
                          |
                          | 192.168.122.1(KVM 仮想化ホスト)
                     +----+-----+
                     | KVM host |
                     +----------+
```



KVM ホストからは、以下のコマンドを実行する。
会社と同じように SSH 経由で X window を飛ばせるようにしておく。
```
$ ssh kanamaru@192.168.122.153 -X
```





# Keycloak をコンテナとして配備

以下のコマンドを実行。  
とりあえず、8080 ポートを使ってポートフォワード。
```
$ docker run -d  \
   -p 8080:8080 \
   -e KEYCLOAK_USER=admin \
   -e KEYCLOAK_PASSWORD=admin \
   --name kana-keycloak \
   jboss/keycloak
```

その後、docker ホスト上で firefox を起動し、アクセスしてみる。



#_Keycloak に SP を設定


ログイン後、clients にて[新規作成]

```
Client ID: test
Valid Redirect URIs: http://172.17.0.1:8081/secure
```



```
OIDCProviderMetadataURL       http://172.17.0.1:8080/auth/realms/master/.well-known/openid-configuration
OIDCClientID                  test
OIDCClientSecret              9f0de788-2c4f-4ae0-a141-405ce4c865e2
OIDCResponseType              code
OIDCScope                     "openid"
OIDCSSLValidateServer         Off
OIDCProviderTokenEndpointAuth client_secret_basic
OIDCRedirectURI               http://172.17.0.1:8081/secure
OIDCCryptoPassphrase          passphrase
OIDCPreservePost              On
<Location /secure>
   AuthType         openid-connect
   Require          valid-user
</Location>
```




# API を叩く

## token を取得する

```sh
$ curl -d "client_id=admin-cli" \
  -d "username=admin" \
  -d "password=admin" \
  -d "grant_type=password" \
  "172.17.0.2:8080/auth/realms/master/protocol/openid-connect/token"
```

<details><summary>実行結果</summary><div>

```sh
kanamaru@vm-ubuntu18:~$ curl -d "client_id=admin-cli"   -d "username=admin"   -d "password=admin"   -d "grant_type=password"   "172.17.0.2:8080/auth/realms/master/protocol/openid-connect/token" | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1791  100  1722  100    69  14231    570 --:--:-- --:--:-- --:--:-- 14801
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJORXJzWmE0VWk4eVVoaEs2UVVaZWR6UXp0LWQ5Tmp3ZkJUbXhnSFVxRTBZIn0.eyJleHAiOjE1OTgxOTkxOTEsImlhdCI6MTU5ODE5OTEzMSwianRpIjoiZmFiN2ZmYzYtYmQwOS00Y2FiLThkODEtNGFlMjBkMzhmNjY5IiwiaXNzIjoiaHR0cDovLzE3Mi4xNy4wLjI6ODA4MC9hdXRoL3JlYWxtcy9tYXN0ZXIiLCJzdWIiOiI3NzRhYjM4Yy1kNmE0LTQ5NTQtYjAyNy0xOGIxMTkzYjMyNDgiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJhZG1pbi1jbGkiLCJzZXNzaW9uX3N0YXRlIjoiYjk3Yjg2OGUtNTI2YS00YjVjLTkxMTItY2VkOGZmN2NjNWM3IiwiYWNyIjoiMSIsInNjb3BlIjoiZW1haWwgcHJvZmlsZSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWRtaW4ifQ.il3nzWbpkACDeCZJumtqV755Q_U1pmhhkTGfzEd7skYhBCgqcq7QZXdraCwJqEssq7nrPRmO_mDSBVrF1Haq8Px_zyWmEhalsFZe6GYed8V7444FWs7PvP1QddaWKN5fmYEc1X6HmW8cx2RdB0_dXE8KkSdL88SvOC2Bknt8vtQAQ6gSWvo4sTnj5stRmyqElV0LP97PC-nAQoqzUAVpmphDhLOi6SZZ6EeHdykKssIkZR5NKyG0ijUUtZVO0kGGWpm3Luk5PiFjw8Q5wjcVjTc4x0Ik0WWtvNkLU8SV7NgYTR8BhKnhdP2xuOoY2NRV-PZMI5hyvsCF8oEjQrXiBA",
  "expires_in": 60,
  "refresh_expires_in": 1800,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI0NzNlZDc0YS1jOWU1LTRiM2YtYjI2Mi1kNGY1OTZlY2VmZWQifQ.eyJleHAiOjE1OTgyMDA5MzEsImlhdCI6MTU5ODE5OTEzMSwianRpIjoiM2NiMjdiZDctMjdiNi00ZGI2LTkzYmQtNjIyOGM3YTg4NzFjIiwiaXNzIjoiaHR0cDovLzE3Mi4xNy4wLjI6ODA4MC9hdXRoL3JlYWxtcy9tYXN0ZXIiLCJhdWQiOiJodHRwOi8vMTcyLjE3LjAuMjo4MDgwL2F1dGgvcmVhbG1zL21hc3RlciIsInN1YiI6Ijc3NGFiMzhjLWQ2YTQtNDk1NC1iMDI3LTE4YjExOTNiMzI0OCIsInR5cCI6IlJlZnJlc2giLCJhenAiOiJhZG1pbi1jbGkiLCJzZXNzaW9uX3N0YXRlIjoiYjk3Yjg2OGUtNTI2YS00YjVjLTkxMTItY2VkOGZmN2NjNWM3Iiwic2NvcGUiOiJlbWFpbCBwcm9maWxlIn0.38aqrH2jpeooG72Lpn8TOeiDATj9esGiXAvL2uDIgI4",
  "token_type": "bearer",
  "not-before-policy": 0,
  "session_state": "b97b868e-526a-4b5c-9112-ced8ff7cc5c7",
  "scope": "email profile"
}
```
</div></details>




## ユーザ一覧を取得する

```sh
$ curl   -H "Authorization: bearer <ACCESS_TOKEN>" \
  "172.12.0.2:8080/auth/admin/realms/master/users"
```


<details><summary>実行結果</summary><div>

面倒なので、トークンやらなんやらを設定して実行
```sh
KEYCLOAK_URL=http://localhost:8080/auth
KEYCLOAK_REALM=master
KEYCLOAK_CLIENT_ID=admin
KEYCLOAK_CLIENT_SECRET=admin

export TOKEN=$(curl -X POST "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token" \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -d "username=${KEYCLOAK_CLIENT_ID}" \
 -d "password=${KEYCLOAK_CLIENT_SECRET}" \
 -d 'grant_type=password' \
 -d 'client_id=admin-cli' | jq -r '.access_token')

curl -X GET \
-H "Accept: application/json" \
-H "Authorization: Bearer ${TOKEN}" \
"${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/users" | jq
```
</div></details>





## 特定のユーザ情報を取得する

```sh
$ curl   -H "Authorization: bearer <ACCESS_TOKEN>" \
  "172.12.0.2:8080/auth/admin/realms/master/users/<USERID>"
```


<details><summary>実行結果</summary><div>

今回は実行者自身の情報を取得する。
面倒なので、トークンやらなんやらを設定して実行
```sh
KEYCLOAK_URL=http://localhost:8080/auth
KEYCLOAK_REALM=master
KEYCLOAK_CLIENT_ID=admin
KEYCLOAK_CLIENT_SECRET=admin

export TOKEN=$(curl -X POST "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token" \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -d "username=${KEYCLOAK_CLIENT_ID}" \
 -d "password=${KEYCLOAK_CLIENT_SECRET}" \
 -d 'grant_type=password' \
 -d 'client_id=admin-cli' | jq -r '.access_token')

export USERID=$(curl -X GET "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/users" \
-H "Accept: application/json" \
-d "username=${KEYCLOAK_CLIENT_ID}" \
-H "Authorization: Bearer ${TOKEN}" | jq '.[].id')



curl -X GET "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/users" \
-H "Accept: application/json" \
-d "username=${KEYCLOAK_CLIENT_ID}" \
-H "Authorization: Bearer ${TOKEN}" | jq '.[].id'


curl -X GET \
-H "Accept: application/json" \
-H "Authorization: Bearer ${TOKEN}" \
"${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/users/${USERID}" | jq
```
</div></details>




## グループ一覧を取得する

```sh
$ curl   -H "Authorization: bearer <ACCESS_TOKEN>" \
  "172.12.0.2:8080/auth/admin/realms/master/groups"
```


<details><summary>実行結果</summary><div>

面倒なので、トークンやらなんやらを設定して実行
```sh
KEYCLOAK_URL=http://localhost:8080/auth
KEYCLOAK_REALM=master
KEYCLOAK_CLIENT_ID=admin
KEYCLOAK_CLIENT_SECRET=admin

export TOKEN=$(curl -X POST "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token" \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -d "username=${KEYCLOAK_CLIENT_ID}" \
 -d "password=${KEYCLOAK_CLIENT_SECRET}" \
 -d 'grant_type=password' \
 -d 'client_id=admin-cli' | jq -r '.access_token')

curl -X GET \
-H "Accept: application/json" \
-H "Authorization: Bearer ${TOKEN}" \
"${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/groups" | jq
```
</div></details>


## 特定のグループ情報を取得する

```sh
$ curl   -H "Authorization: bearer <ACCESS_TOKEN>" \
  "172.12.0.2:8080/auth/admin/realms/master/groups"
```


<details><summary>実行結果</summary><div>

面倒なので、トークンやらなんやらを設定して実行
```sh
KEYCLOAK_URL=http://localhost:8080/auth
KEYCLOAK_REALM=master
KEYCLOAK_CLIENT_ID=admin
KEYCLOAK_CLIENT_SECRET=admin

export TOKEN=$(curl -X POST "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token" \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -d "username=${KEYCLOAK_CLIENT_ID}" \
 -d "password=${KEYCLOAK_CLIENT_SECRET}" \
 -d 'grant_type=password' \
 -d 'client_id=admin-cli' | jq -r '.access_token')

export GROUPID=$(curl -X GET "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/groups" \
-H "Accept: application/json" \
-d "username=${KEYCLOAK_CLIENT_ID}" \
-H "Authorization: Bearer ${TOKEN}" | jq '.[].id.value')

curl -X GET \
-H "Accept: application/json" \
-H "Authorization: Bearer ${TOKEN}" \
"${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/groups/${GROUPID}" | jq
```
</div></details>




















ちなみに、admin ユーザのユーザIDを取得する場合
```sh
KEYCLOAK_URL=http://localhost:8080/auth
KEYCLOAK_REALM=master
KEYCLOAK_CLIENT_ID=admin
KEYCLOAK_CLIENT_SECRET=admin

export TOKEN=$(curl -X POST "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token" \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -d "username=${KEYCLOAK_CLIENT_ID}" \
 -d "password=${KEYCLOAK_CLIENT_SECRET}" \
 -d 'grant_type=password' \
 -d 'client_id=admin-cli' | jq -r '.access_token')


curl -X GET \
-H "Accept: application/json" \
-H "Authorization: Bearer ${TOKEN}" \
"${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/users" | jq


curl -X GET "${KEYCLOAK_URL}/admin/realms/${KEYCLOAK_REALM}/users" \
-H "Accept: application/json" \
-d "username=${KEYCLOAK_CLIENT_ID}" \
-H "Authorization: Bearer ${TOKEN}" | jq ".[] |select(.username == \"admin\")" | jq .id
```


