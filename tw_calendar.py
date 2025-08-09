#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
from tw_calendar_csv_to_json import csv_to_json, JSON_DIR_DEFAULT as JSON_DIR
from tw_calendar_json_to_ics import json_to_ics, ICS_DIR_DEFAULT as ICS_DIR

JSON_DIR_DEFAULT = os.path.join("data", "json")
ICS_DIR_DEFAULT = os.path.join("data", "calendars")

def main():
    parser = argparse.ArgumentParser(description="民國年 → JSON → ICS，一鍵轉換（自動處理修正版 CSV）")
    parser.add_argument("roc_year", type=int, help="民國年（例如 115）")
    parser.add_argument("--csv-dir", default=os.path.join("data", "中華民國政府行政機關辦公日曆表"),
                        help="CSV 資料夾")
    parser.add_argument("--json-dir", default=JSON_DIR, help="JSON 資料夾")
    parser.add_argument("--ics-dir", default=ICS_DIR, help="ICS 輸出資料夾")
    args = parser.parse_args()

    json_path = os.path.join(args.json_dir, f"{args.roc_year}.json")
    if not os.path.isfile(json_path):
        print(f"📄 找不到 {json_path}，嘗試從 CSV 轉換...")
        csv_to_json(args.roc_year, args.csv_dir, args.json_dir)
    else:
        print(f"✅ 已找到 JSON：{json_path}")

    ics_path = json_to_ics(args.roc_year, args.json_dir, args.ics_dir)
    print(f"🎉 已輸出 ICS：{ics_path}")

## 執行範例: python tw_calendar.py {民國年}
## python tw_calendar.py 115
if __name__ == "__main__":
    main()
