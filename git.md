# git の環境構築

## git のインストール

### windows 編

[ここから](https://gitforwindows.org/)ダウンロードする。  
ダウンロードしたら実行し、インストーラーの指示にしたがって進めていく。

### ubuntu 編

apt コマンドを使えば簡単にインストールすることができる。

```
sudo apt install git
```

インストールしたら、次のコマンドでバージョンを見ることができる。

```
git --version
```

## git の初期設定

git をインストールしたら、ユーザー名と Email アドレスを必ず設定する。

```
git config --global user.name "<任意のユーザー名>"
git config --global user.email "<任意のメールアドレス>"
```

なお、ここで設定するユーザー名とメールアドレスは github で登録したユーザー名とメールアドレスでなくても良い。誰が push したかを確認するための設定だからだ。
設定内容を確認するには、次のコマンドを実行すれば良い。

```
git config --global --list
```

## コードを保存するディレクトリを作る

ローカルリポジトリを作るために、コードを保存するディレクトリを作る必要がある。

```
cd <作るディレクトリ>
mkdir <保存するディレクトリ名>
```

ドキュメントに作っても良いが、project ディレクトリを作って、そこに保存するほうが良い。

## initilaize する

github で使うファイルであることを定義するために、以下のコマンドをたたく。

```
git init
```

これだけ。

## リモートリポジトリを追加する

これまでは、ローカルリポジトリの中での作業だったので、次のコマンドでリモートリポジトリと紐づける。

```
git remote add origin <自分のgithubのURL>
```

自分の github の url ぐらいは覚えておいた方がいいらしい。以下参考に。

```
git remote add origin git@github.com:<user名>/<リモートリポジトリ名>.git
```

以上のコマンドを打つとリモートリポジトリが登録されているはずである。次のコマンドをたたいて確かめよう。

```
git remote -v
```

ちゃんと登録されていれば次のように表示される。

```
origin git@github.com:<ユーザー名>/<リモートリポジトリ名>.git (fetch)
origin git@github.com:<ユーザー名>/<リモートリポジトリ名>.git (push)
```

登録したリモートリポジトリを消したいときは、次のようにたたく。

```
git remote rm origin
```

## ssh の認証

これが一番めんどい。

### ubuntu 編

### windows 編

ssh の鍵を入れておくためのディレクトリに移動する。

```
cd C:/Users/<ユーザー名>/.ssh
```

キーを作成する。

```
ssh-keygen -t rsa
```

うまく行けばカレントディレクトリに"id_rsa"と"id_rsa.pub"ができていると思う。
"id_rsa"は秘密鍵で絶対に公開しないように。
"id_rsa.pub"が公開鍵なので、こちらを github に登録する。

[github](https://github.co.jp/)にアクセスして、ssh の認証を通す。ログインして、アカウントのなかにある「setting」から ssh を追加する。

さあ、push してみよう！
