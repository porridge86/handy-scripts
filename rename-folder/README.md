# フォルダ名一括変換

「1 April 2019」や「1 January 1」のような【日＋英語月名＋年】形式のフォルダー名を、
一括で【YYYY-MM-DD】形式（例: `2019-04-01`、`0001-01-01`）に安全にリネームするための Python スクリプトです。

フォルダー名（目次）のみを書き換えるため、**フォルダー内のデータ（更新日時やファイル中身）は一切保持されたまま変更されません。**

## 主な特徴

- **ドライラン（確認モード）機能**: 実際の変更を行う前に、変換前後のリストを画面で確認できます。

- **履歴の自動保存**: 実行と同時に、元の名前と新しい名前の対応表（`_rename_history.csv`）が対象フォルダー内に自動生成されます。

- **形式エラーの自動スキップ**: 指定した形式に合わないフォルダー（スペースの数が違う、日付ではない等）は安全のために無視されます。


## 対応するファイル（パターン別）

膨大な量のフォルダーを一括で変更する際の安全性を最優先にするため、あえて1つのプログラムにまとめず、命名規則パターンごとにスクリプトファイルを分離しています。これにより、意図しない誤変換のリスクを完全に排除します。

1. **`rename.py`**（DMY：Day Month Year)
   - **元の形式**: `23 July 2020`
   - **変換後**: `2020-07-23`

2. **`rename_LDMY.py`**（Location Dash-Date-Pattern）
   - **元の形式**: `NY, 2019-7-27`
   - **変換後**: `2019-07-27-NY`

3. **`rename_DMYL.py`**（Date-Dash-Location-Pattern）
   - **元の形式**: `23 July 2020,NY`
   - **変換後**: `2020-07-23-NY`

## 使い方

### 1. スクリプトの設定

`rename.py` を開き、上部の【設定エリア】を環境に合わせて書き換えます。

```python
# =================【設定エリア】=================
TARGET_DIR = "/Users/YOUR_USER_NAME/Desktop/Test"  # 対象の親フォルダーパス
DRY_RUN = True  # 最初は必ず True（確認モード）にしてください
# ===============================================
```

### 2. ターミナルでの実行手順

#### ステップ1：スクリプトのフォルダーへ移動

ターミナルを開き、このスクリプトが置かれているフォルダーへ移動します。

```bash
cd /Users/＊＊＊/Projects/rename-folder
```

#### ステップ2：確認モード（DRY_RUN = True）で実行

まずは実際の変更を行わずに、シミュレーションを実行します。

```bash
python3 rename.py
```

画面に `[確認用] 変換前 ===> 変換後` のリストが表示されます。
また、対象フォルダー内に `_rename_history.csv` が作成されるので、エラーや予期せぬ変換がないか必ず目視で確認してください。

#### ステップ3：本番実行（DRY_RUN = False）

CSVのリストに問題がないことを確信できたら、`rename.py` の設定を書き換えます。

```python
DRY_RUN = False  # 本番モードに変更
```

保存後、ターミナルで再度実行します。

```bash
python3 rename.py
```

1400個程度のフォルダーであれば、1〜2秒で一括変換が完了します。

## 注意事項

- 万が一のトラブル（予期せぬ電源オフなど）に備え、大規模な処理を行う前には**対象フォルダー全体のバックアップ（コピー）を取ってから**本番実行することをお勧めします。

---

## Date Folder Renamer

A safe Python script to batch rename folders from **"D Month YYYY"** (e.g., `1 April 2019`, `1 January 1`) to **"YYYY-MM-DD"** (e.g., `2019-04-01`, `0001-01-01`).

**Note:** This script only modifies the folder names. **All files and data inside the folders remain completely untouched and preserved.**

- **Dry Run Mode**: Preview the changes before actually renaming any folders.
- **Auto-Generated History**: Creates a `_rename_history.csv` mapping original names to new names.
- **Safety Skip**: Automatically ignores folders that do not match the expected date pattern.


