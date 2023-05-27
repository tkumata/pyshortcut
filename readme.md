# キーボードのショートカットキーで Slack に定型文を送る
特定のキーコンビネーションが押下されたら Slack に定型文を送信しかつ Slack ステータスを変更する python スクリプトです。PyInstaller でバイナリ化することを想定しています。

なお挙動としては、例えば iTerm でこのプログラムを実行すると iTerm 上で特定のキーコンビネーションが押下された時だけ発火します。他のアプリ上で特定キーコンビネーションを押下しても反応しません。

macOS の場合、Input Monitoring に認識されるので Security & Privacy で許可が必要です。


## 前提 1: モジュールのインストール
python モジュールの `pynput` をインストールします。

```
python3 -m pip install pynput
```

or

```
pip3 install pynput
```


## 前提 2: Slack の情報
Slack から以下の情報を取得しておきます。

- Slack App の `statusChanger` から Token を取得する。
- Slack の自分の Member ID を取得する。
- post したい Slack のチャンネルの Channel ID を取得する。


## 設定
上記 Slack 情報を json ファイルにして保存します。

```
vi ~/.slack-hotkey/config.json
```

記述内容。

```
{
    "token": "xoxp-xxx-xxx-xxx-xxxxxx",
    "member_id": "Uxxxxxxxx",
    "channel": "Cxxxxxxxx"
}
```


## ビルド
本番ビルドは実際に Slack に送信します。

```
make
```

デバッグビルドは logger でログを残すだけです。

```
make debug
```


## 使い方
```
slack-hotkey
```

特定キーコンビネーションは以下のとおりです。

- `ctrl + shift + alt + h` = 業務開始メッセージ
- `ctrl + shift + alt + j` = 業務終了メッセージ
- `ctrl + shift + alt + k` = 離席メッセージ
- `ctrl + shift + alt + l` = 戻りメッセージ
- `esc` = プログラム終了
