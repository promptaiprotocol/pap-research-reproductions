# Test-Firstで変更の受入条件を確かめる

[PAP Researchの記事](https://promptaiprotocol.jp/articles/test-first-agent-acceptance-scope/)に掲載した、リストから指定件数を選ぶ最小例です。`limit=0` で0件になることと、既存の並び順・件数上限・入力の扱いをテストします。

Python 3.14 と pytest 8.4.2 を使用します。プロジェクトのルートで仮想環境を作り、その Python で実行します。

```console
python -m venv .venv
```

WindowsのPowerShellの場合

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
```

macOS・Linuxの場合

```sh
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
```

最初の状態は修正後で、14件が成功します。修正前を確かめるには、`app/selection.py` の内容を `app/selection_original.py` で置き換え、同じコマンドで実行します。0件指定に関する2件が失敗することを確認したら、`app/selection.py` を元に戻して再実行してください。変更を戻せるよう、作業用に展開したコピーを使用してください。

修正前後を一度に確かめる場合は、同じ仮想環境の Python で `check.py` を実行します。一時ディレクトリにコピーして、修正前は0件指定の2件だけが失敗し、修正後は14件すべてが成功することを確認します。GitHub Actionsも同じスクリプトを使います。

実行対象はメモリ内のリストを処理する関数です。データベース、外部API、並行処理、実際のエージェント権限は試験に含みません。依存の取得時だけ PyPI への接続が必要です。
