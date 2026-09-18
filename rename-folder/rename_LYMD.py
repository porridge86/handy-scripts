import os
import re
import csv

# =================【設定エリア】=================
# 処理したいフォルダーが置かれている親フォルダーのパスを指定
TARGET_DIR = "..."
DRY_RUN = True
# ===============================================

# 「地名, 年-月-日」にマッチする正規表現
# 月（\d{1,2}）や日（\d{1,2}）が1桁〜2桁のどちらでも対応します
pattern = re.compile(r"^(.+?),\s+(\d{4})-(\d{1,2})-(\d{1,2})$")

history = []
failed_logs = []

print(f"--- リネーム処理開始 (DRY_RUN: {DRY_RUN}) ---")

for folder_name in os.listdir(TARGET_DIR):
    folder_path = os.path.join(TARGET_DIR, folder_name)

    if os.path.isdir(folder_path):
        match = pattern.match(folder_name)
        if match:
            location = match.group(1).strip()  # 地名
            year = match.group(2)              # 年
            month = match.group(3).zfill(2)    # 月
            day = match.group(4).zfill(2)      # 日

            # 新しい名前の組み立て: YYYY-MM-DD-地名
            new_name = f"{year}-{month}-{day}-{location}"
            new_path = os.path.join(TARGET_DIR, new_name)

            history.append({
                "original_name": folder_name,
                "new_name": new_name,
                "status": "変更予定" if DRY_RUN else "変更完了"
            })

            if DRY_RUN:
                print(f"[確認用] {folder_name}  ===>  {new_name}")
            else:
                if os.path.exists(new_path):
                    print(f"[エラー] 変更先の名前が既に存在します: {new_name}")
                else:
                    os.rename(folder_path, new_path)

print(f"\n--- 処理終了 (対象フォルダー数: {len(history)}個) ---")

history_csv_path = os.path.join(TARGET_DIR, "_rename_dash_history.csv")
with open(history_csv_path, mode="w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["original_name", "new_name", "status"])
    writer.writeheader()
    writer.writerows(history)

print(f"元の名前との対応表を保存しました: {history_csv_path}")

if failed_logs:
    print("\n == 以下のフォルダーは形式が合わずスキップされました ==")
    for log in failed_logs:
        print(log)
