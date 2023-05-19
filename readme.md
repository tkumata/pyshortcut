# キーボードのショートカットキーで Slack に定型文を送る
キー入力を待ち受けて特定のキーコンビネーションが押下されたら、特定の関数を実行します。今回は特定のキーコンビネーションが押下されたら Slack に定型文を送信しかつ Slack ステータスを変更するようにしています。

なお挙動としては、例えば iTerm でこのスクリプトを実行したら iTerm 上で特定のキーコンビネーションが押下された時だけ発火します。他のアプリ上で押下しても反応しません。macOS の場合、Input Monitoring に認識されるので Security & Privacy で許可が必要です。


## 前提 1: ライブラリのインストール
`pynput` が必要です。
```
python3 -m pip install pynput
```
or
```
pip3 install pynput
```


## 前提 2: Slack の情報
- Slack App の `statusChanger` から Token を取得する。
- Slack の自分の Member ID を取得する。
- post したい Slack のチャンネルの Channel ID を取得する。


## 設定
上記 Slack 情報を json ファイルにして保存します。
```
vi config.json
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

- `ctrl + shift + alt + h` = punch in to slack
- `ctrl + shift + alt + j` = punch out to slack
- `ctrl + shift + alt + k` = away from keyboard to slack
- `ctrl + shift + alt + l` = come back to slack
- `esc` = quit
