import os
import shutil
import csv
import sys
from datetime import datetime

# --- 設定項目 ---
SRC_DIR = r"..."
DST_DIR = r"..."
# True: シミュレーション（画面＆CSV出力のみ）
# False:本番実行
DRY_RUN = True
# ---------------

def get_dir_size(path):
    """フォルダ内のファイル総容量（バイト）を計算"""
    total_size = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == ".DS_Store":
                continue
            file_path = os.path.join(root, file)
            try:
                # リンク切れなどのエラーを回避しつつサイズ取得
                if os.path.exists(file_path):
                    total_size += os.path.getsize(file_path)
            except Exception:
                pass
    return total_size

def copy_with_rename(src, dst, dry_run=True):
    mode_label = "【テスト】" if dry_run else "【本番実行】"
    print(f"{mode_label} 処理開始...\n")


        # 1. ディスク容量の事前チェック
    print("ディスク容量をチェックしています...")
    required_bytes = get_dir_size(src)

    # 移動先フォルダが存在しない場合は、その親フォルダのディスク容量をチェック
    check_target_dir = dst
    while check_target_dir and not os.path.exists(check_target_dir):
        check_target_dir = os.path.dirname(check_target_dir)

    try:
        total, used, free_bytes = shutil.disk_usage(check_target_dir)
    except Exception as e:
        print(f" ディスク容量の取得に失敗しました: {e}")
        free_bytes = 0

    required_gb = required_bytes / (1024 ** 3)
    free_gb = free_bytes / (1024 ** 3)

    print(f" -> 移動元の総容量: {required_gb:.2f} GB")
    print(f" -> 移動先の空き容量: {free_gb:.2f} GB")

    # 本番実行時に容量が足りない場合は強制終了
    if not dry_run and required_bytes > free_bytes:
        print(f"\n エラー: 移動先のディスク容量が足りません！ (不足: {(required_gb - free_gb):.2f} GB)")
        print("処理を安全に中止しました。")
        sys.exit(1)
    elif dry_run and required_bytes > free_bytes:
        print(f"\n 警告: 本番実行時に容量が不足します！ (不足: {(required_gb - free_gb):.2f} GB)")
    else:
        print(" -> ディスク容量OK")
    print("-" * 40 + "\n")

    # ファイル名用に現在の日付と時刻を取得
    current_date = datetime.now().strftime("%Y%m%d")

    # CSVファイルの保存パス
    csv_file_path = os.path.join(dst, f"_log_{current_date}.csv")

    # テスト時でも移動先フォルダ（ログ保存用）が存在しない場合は作成
    if dry_run:
        os.makedirs(dst, exist_ok=True)

    csv_data = []
    # 出力予定のパスを記録
    planned_paths = set()

    for root, dirs, files in os.walk(src):
        # 移動元と同じ階層構造を移動先に作るパスを計算
        rel_path = os.path.relpath(root, src)
        target_dir = os.path.join(dst, rel_path) if rel_path != "." else dst

        if not dry_run:
            os.makedirs(target_dir, exist_ok=True)

        for file in files:
            # .DS_StoreなどのMac固有の隠しシステムファイルは記録・コピーから除外
            if file == ".DS_Store":
                continue

            src_file_path = os.path.join(root, file)
            dst_file_path = os.path.join(target_dir, file)
            # 名称変更が起きたかどうかを追跡するフラグ
            is_renamed = False

            # 実際のファイル存在、またはテスト時の出力予定リストに既にあるかチェック
            if os.path.exists(dst_file_path) or dst_file_path in planned_paths:
                is_renamed = True  # 同名あり→リネーム判定
                base, ext = os.path.splitext(file)
                counter = 2
                while True:
                    new_file_name = f"{base}_{counter:02d}{ext}"
                    dst_file_path = os.path.join(target_dir, new_file_name)
                    # 実際のファイルと、予定リストの両方にない空き番号を探す
                    if not os.path.exists(dst_file_path) and dst_file_path not in planned_paths:
                        break
                    counter += 1

            # 決定したパスを予定リストに追加
            planned_paths.add(dst_file_path)

            # 処理した日時（年月日時分秒）を取得
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_file_name = os.path.basename(dst_file_path)

            # CSVに記録する情報をまとめる
            csv_data.append([timestamp, root, file, target_dir, new_file_name])



            # 本番実行時のみ実際にファイルをコピー
            if not dry_run:
                shutil.copy2(src_file_path, dst_file_path)
            label = "[テスト確認]" if dry_run else "[コピー完了]"
            if is_renamed:
                print(f"{label}: {file} -> {new_file_name}(名前変更)")
            else:
                print(f"{label}: {file} -> {new_file_name}")


    # CSVファイルへの書き込み（文字化け防止で utf-8-sig）
    with open(csv_file_path, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        # ヘッダー（列名）の書き込み
        writer.writerow(["処理日時", "元のフォルダパス", "元のファイル名", "移動先フォルダパス", "新しいファイル名"])
        # データの書き込み
        writer.writerows(csv_data)

    print(f"\n{mode_label} 処理が完了しました。")
    print(f"ログファイルを出力しました: {csv_file_path}")

    print(f"本番ではディスク容量が 【{required_gb:.2f} GB】 必要です。")
    print(f"現在の移動先のディスクには容量が 【{free_gb:.2f} GB】 あります。")

    if required_bytes > free_bytes:
        print(f" 警告: 現在、ディスク容量が 【{(required_gb - free_gb):.2f} GB】 不足しています。")
    else:
        print(" 判定: ディスク容量は十分に足りています。")

if __name__ == "__main__":
    copy_with_rename(SRC_DIR, DST_DIR, dry_run=DRY_RUN)
