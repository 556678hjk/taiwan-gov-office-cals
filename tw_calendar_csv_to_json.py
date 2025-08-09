#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import json
import argparse
from typing import List, Dict

CSV_DIR_DEFAULT = os.path.join("data", "中華民國政府行政機關辦公日曆表")
JSON_DIR_DEFAULT = os.path.join("data", "json")

def find_csv_by_roc(roc_year: int, csv_dir: str) -> str:
    """
    在 csv_dir 下搜尋民國年檔案（支援附註檔名，如 '114年中華民國政府行政機關辦公日曆表(修正版).csv'）
    優先使用包含 '修正版' 的檔案
    """
    prefix = f"{roc_year}年中華民國政府行政機關辦公日曆表"
    candidates = [
        f for f in os.listdir(csv_dir)
        if f.startswith(prefix) and f.lower().endswith(".csv")
    ]
    if not candidates:
        raise FileNotFoundError(f"找不到檔案開頭為「{prefix}」的 CSV，資料夾：{csv_dir}")

    # 優先選含"修正版"
    candidates.sort(key=lambda name: ("修正版" not in name, name))
    selected = candidates[0]
    return os.path.join(csv_dir, selected)

def read_calendar_csv(csv_path: str) -> List[Dict[str, str]]:
    """
    讀取 CSV 檔案，回傳列字典清單。
    預期欄位：西元日期, 星期, 是否放假, 備註
    """
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            cleaned = {
                (k.strip() if isinstance(k, str) else k):
                (v.strip() if isinstance(v, str) else v)
                for k, v in row.items()
            }
            rows.append(cleaned)
    return rows

def convert_rows_to_ruyut_json(rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    """
    轉換成 ruyut 格式 JSON
    是否放假："2" → True, "0" → False
    """
    out = []
    for r in rows:
        date = (r.get("西元日期") or "").strip()
        week = (r.get("星期") or "").strip()
        flag = (r.get("是否放假") or "").strip()
        desc = (r.get("備註") or "").strip()

        if not (len(date) == 8 and date.isdigit()):
            continue

        is_holiday = True if flag == "2" else False
        out.append({
            "date": date,
            "week": week,
            "isHoliday": is_holiday,
            "description": desc
        })
    return out

def save_json_by_roc(data: List[Dict[str, object]], roc_year: int, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{roc_year}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return out_path

def csv_to_json(roc_year: int, csv_dir: str = CSV_DIR_DEFAULT, json_dir: str = JSON_DIR_DEFAULT) -> str:
    csv_path = find_csv_by_roc(roc_year, csv_dir)
    rows = read_calendar_csv(csv_path)
    json_data = convert_rows_to_ruyut_json(rows)
    return save_json_by_roc(json_data, roc_year, json_dir)
    
## 執行範例: python tw_calendar_csv_to_json.py {民國年}
## python tw_calendar_csv_to_json.py 114
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="將民國年版政府行政機關辦公日曆表 CSV 轉為 JSON（支援修正版檔案）")
    parser.add_argument("roc_year", type=int, help="民國年（例如 114）")
    parser.add_argument("--csv-dir", default=CSV_DIR_DEFAULT, help=f"CSV 資料夾（預設 {CSV_DIR_DEFAULT}）")
    parser.add_argument("--json-dir", default=JSON_DIR_DEFAULT, help=f"JSON 輸出資料夾（預設 {JSON_DIR_DEFAULT}）")
    parser.add_argument("--csv", default=None, help="直接指定 CSV 檔路徑（略過自動搜尋）")
    args = parser.parse_args()

    # 找 CSV 檔案
    if args.csv:
        csv_path = args.csv
    else:
        csv_path = find_csv_by_roc(args.roc_year, args.csv_dir)

    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"找不到檔案：{csv_path}")

    # 讀取與轉換
    rows = read_calendar_csv(csv_path)
    json_data = convert_rows_to_ruyut_json(rows)

    # 儲存 JSON
    out_path = save_json_by_roc(json_data, args.roc_year, args.json_dir)

    print(f"✅ 轉換完成（民國 {args.roc_year} 年）")
    print(f"   來源 CSV：{csv_path}")
    print(f"   輸出 JSON：{out_path}")
    print(f"   事件筆數：{len(json_data)}")
