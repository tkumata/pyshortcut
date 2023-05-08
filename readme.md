# キーボードのショートカットキーで Slack に定型文を送る
これはスクリプトで提供する機能も非常に単調なため、可読性は犠牲にしてコピペで導入できる簡易性を重視して実行ファイルは一つにしたかったのです。

## 前提 1: ライブラリのインストール
```
python3 -m pip install pynput
or
pip3 install pynput
```

## 前提 2: Slack の情報
- Slack App の `statusChanger` から Token を取得する。
- Slack の自分の Member ID を取得する。
- post したい Slack のチャンネルの Channel ID を取得する。

## 設定

```
vi config.json

{
    "token": "xoxp-xxx-xxx-xxx-xxxxxx",
    "member_id": "Uxxxxxxxx",
    "channel": "Cxxxxxxxx"
}
```

## 使い方
本番 (Slack に投げる)

```
python3 -O slack-hotkey.py
```

デバッグ (Slack に投げない)

```
python3 slack-hotkey.py
```

- `ctrl + shift + alt + h` = punch in to slack
- `ctrl + shift + alt + j` = punch out to slack
- `ctrl + shift + alt + k` = away from keyboard to slack
- `ctrl + shift + alt + l` = come back to slack
- `ctrk + c` = quit
