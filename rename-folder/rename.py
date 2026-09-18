import os
import re
from datetime import datetime
import csv

# =================【設定エリア】=================
# 1. 変換したいフォルダーが置かれている親フォルダーのパスを記述
TARGET_DIR = "..."

# 2. 最初に確認するため、最初は必ず True
#    確認して問題なければ 本番は False に書き換え
DRY_RUN = True
# ===============================================


# 英語の月名パターン（January, Aprなど）
month_pattern = r"(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"

# 「地名, 日 月 年」にマッチする正規表現
# 前半の (.+?),\s+ で地名とカンマ、スペースをキャプチャします
pattern = re.compile(rf"^(.+?),\s+(\d{{1,2}})\s+{month_pattern}\s+(\d{{1,4}})$", re.IGNORECASE)


history = []
failed_logs = []

print(f"--- リネーム処理開始 (DRY_RUN: {DRY_RUN}) ---")

# フォルダーを一括スキャン
for folder_name in os.listdir(TARGET_DIR):
    folder_path = os.path.join(TARGET_DIR, folder_name)

    # ディレクトリ（フォルダー）のみを対象にする
    if os.path.isdir(folder_path):
        match = pattern.match(folder_name)
        if match:
            day = match.group(1).zfill(2)       # 1桁なら「01」にする
            month_str = match.group(2)
            year = match.group(3).zfill(4)      # 1桁の年「1」を「0001」に揃える

            # 月名を数字（2桁）に変換
            month = None
            for fmt in ("%B", "%b"):
                try:
                    month = str(datetime.strptime(month_str, fmt).month).zfill(2)
                    break
                except ValueError:
                    continue

            if not month:
                failed_logs.append(f"[解析失敗] 月名が解釈できません: {folder_name}")
                continue

            # 新しい名前の組み立て: YYYY-MM-DD-地名
            new_name = f"{year}-{month}-{day}"
            new_path = os.path.join(TARGET_DIR, new_name)

            # 履歴に追加
            history.append({
                "original_name": folder_name,
                "new_name": new_name,
                "status": "変更予定" if DRY_RUN else "変更完了"
            })

            if DRY_RUN:
                print(f"[確認用] {folder_name}  ===>  {new_name}")
            else:
                # 本番実行：重複エラーを防ぎつつリネーム
                if os.path.exists(new_path):
                    print(f"[エラー] 変更先の名前が既に存在します: {new_name}")
                else:
                    os.rename(folder_path, new_path)

print(f"\n--- 処理終了 (対象フォルダー数: {len(history)}個) ---")

# 万が一のための「名前の履歴表」をCSVで保存
history_csv_path = os.path.join(TARGET_DIR, "_rename_history.csv")
with open(history_csv_path, mode="w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["original_name", "new_name", "status"])
    writer.writeheader()
    writer.writerows(history)

print(f"元の名前との対応表を保存しました: {history_csv_path}")

if failed_logs:
    print("\n == 以下のフォルダーは形式が合わずスキップされました ==")
    for log in failed_logs:
        print(log)
