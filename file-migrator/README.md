# 自動連番付きファイル移動・コピー処理ツール

[-> English](#english)

---

### 概要

- フォルダの階層構造（深さ）を完全に維持したまま、安全にファイルをコピー・統合します。
- 移動先（コピー先）に同名のファイルが存在する場合、データを上書きせずに自動で末尾に連番（`_02`, `_03` など）を付与して両方のファイルを残します。

### 重要な注意点

1. **元データの削除は手動で行ってください**: このスクリプトはデータ損失を防ぐため、あくまでファイルの「**コピー**」を行います。移動元のファイルは自動では削除されません。処理完了後、データが正しくコピーされたことを確認した上で、**元のフォルダのファイルを手動で削除**することを強く推奨します。

2. **一時的な空き容量が必要です**: 移動（カット＆ペースト）ではなくコピー処理を行うため、実行中はコピーする総データ量分の**ディスク空き容量が一時的に必要**になります。ストレージ残量に十分な余裕があるか事前にご確認ください。

3. **メタデータ（Exif情報等）とタイムスタンプの挙動**:
   - **Exif情報（撮影日時等）**: 完全に保持されます。ただし、Exifのない画像（LINE保存、ネット画像等）は写真アプリ読み込み時に「コピーした日時」が撮影日として代用される場合があります。
   - **ファイルの更新日時**: 元のファイルの日時が完全に引き継がれます。
   - **ファイルの作成日時**: Macのシステム仕様上、コピーした「今の時間」に新しくセットされます。


### 特徴

* **事前の容量計算**: 実行直後に「移動元の容量」と「移動先の残り容量」を GB（ギガバイト）単位で画面に表示します。

* **本番時の一時停止**: もし容量が1バイトでも不足している場合、sys.exit(1) によってファイルを1個もコピーすることなく安全にプログラムを終了させ、ストレージがパンクするのを防ぎます。
* **多階層対応**: 何層もある深いフォルダ構造を自動的にスキャンし、移動先に再現します。

* **自動連番リネーム**: 同名ファイルの衝突時、空いている番号（`_02`、`_03`...）を自動検索してリネームします。

* **シミュレーション機能（DRY_RUN）**: 本番実行前に、どのファイルがどうリネームされるかを画面とCSVで事前に安全に確認できます。

* **詳細なCSVログ出力**: 処理日時、元のパス、新しいファイル名を含む詳細な履歴ファイルを自動作成します。

* **Mac最適化**: `.DS_Store` などの不要な隠しシステムファイルは自動で除外されます。

### 使用方法

1. **初期設定**: スクリプト内の6行目・7行目のパスをご自身の環境に書き換えます。

   ```python
   SRC_DIR = r"/ユーザー/移動元のフォルダパス"
   DST_DIR = r"/ユーザー/移動先のフォルダパス"
   ```

2. **テスト実行（シミュレーション）**: スクリプト内の `DRY_RUN = True`（初期状態）のまま、ターミナルで実行します。

   ```bash
   python3 file_migrator.py
   ```

   移動先フォルダ内に生成される `_log_YYYYMMDD.csv` や画面ログを確認し、連番が正しく割り振られているか確認します。

3. **本番実行**: 問題がなければスクリプト内の設定を `DRY_RUN = False` に変更して保存し、再度ターミナルで実行して実際のコピーを開始します。


---

## English

### File Migrator Tool with Auto-Renaming

### Description

- This Python script safely merges folders and copies files while retaining the original hierarchical directory structure.

- If files with identical names conflict, it automatically appends serial suffixes (e.g., `_02`, `_03`) to ensure no data is overwritten.


### Important Notes

1. **Manual Deletion Required (Safety First)**: This script only **copies** files to ensure data safety. It will **not** delete anything from the source folder. After the process is complete and you have verified the results, please **manually delete the original files**.

2. **Temporary Disk Space Required**: Because the script duplicates files by copying them, you will temporarily need **enough free disk space** on the destination drive to hold the total volume of all copied files during the operation.


3. **Metadata (Exif) and Timestamp Behavior**:
   - **Exif Metadata (Capture Date/Time)**: Fully preserved. For images without Exif (e.g., from LINE, web downloads), the "copied date" might be used as the capture date when imported into photo apps.
   - **File Modified Date**: Completely preserved from the original file.
   - **File Created Date**: Reset to the "current time" when the copy is created due to macOS system specifications.


### Features

- **Pre-execution Storage Check**: Calculates and displays the total size of the source files and the available space on the destination drive in GB right after starting.
- **Auto-abort on Insufficient Space**: If the target drive lacks even a single byte of required space, the script exits safely (`sys.exit(1)`) before copying any files, preventing target storage exhaustion.
* **Multi-Layer Support**: Traverses and recreates deeply nested folder hierarchies.
* **Smart De-duplication**: Automatically increments file names (`filename_02.ext`, `filename_03.ext`) upon conflict.
* **Dry-Run Simulation**: Review the execution outcome via console log and CSV without making actual changes.
* **Detailed CSV Logging**: Outputs a comprehensive execution log including timestamps, source paths, and target paths.
* **Mac Optimized**: Automatically filters out macOS system files such as `.DS_Store`.

### How to Use

1. **Configuration**: Open the script and modify lines 6 and 7 with your folder paths:
   ```python
   SRC_DIR = r"/path/to/source_folder"
   DST_DIR = r"/path/to/destination_folder"
   ```
2. **Dry Run (Simulation)**: Ensure `DRY_RUN = True` is set (default). Open Terminal and execute:

   ```bash
   python3 file_migrator.py
   ```

   Check the printed logs and the generated `_log_YYYYMMDD.csv` in the destination folder to verify the result.
3. **Execution**: Change `DRY_RUN = False` inside the script, save it, and re-run the script in your Terminal to initiate the actual copy process.

