#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import uuid
import argparse
import datetime as dt

JSON_DIR_DEFAULT = os.path.join("data", "json")
ICS_DIR_DEFAULT = os.path.join("data", "calendars")

def dtstamp_now():
    return dt.datetime.now().strftime("%Y%m%dT%H%M%S")

def make_event(date_str: str, description: str) -> str:
    uid = str(uuid.uuid4())
    lines = [
        "BEGIN:VEVENT",
        f"UID:{uid}",
        "SUMMARY:放假日",
        "STATUS:CONFIRMED",
        "TRANSP:TRANSPARENT",
        f"DTSTART;VALUE=DATE:{date_str}",
        f"DTSTAMP:{dtstamp_now()}",
        "CATEGORIES:dayoff",
        f"DESCRIPTION:{description}",
        "END:VEVENT"
    ]
    return "\r\n".join(lines)

def load_json_by_roc(roc_year: int, json_dir: str = "data/json") -> list:
    path = os.path.join(json_dir, f"{roc_year}.json")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"找不到 JSON：{path}（請先建立或轉換 CSV→JSON）")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_ics(roc_year: int, data: list, out_dir: str = "data/calendars") -> str:
    gregorian = roc_year + 1911
    description = f"中華民國{roc_year}年（西元{gregorian}年）政府行政機關辦公日曆表"
    os.makedirs(out_dir, exist_ok=True)
    ics_path = os.path.join(out_dir, f"{roc_year}-dayoffs.ics")

    header = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//NTUST CCE HCI Lab//Taiwan Government Office Cals//ZH-TW",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH"
    ]

    events = []
    for item in data:
        # 期望欄位：date, isHoliday, week, description
        if item.get("isHoliday"):
            date_str = str(item.get("date", ""))
            if len(date_str) == 8 and date_str.isdigit():
                events.append(make_event(date_str, description))

    footer = ["END:VCALENDAR"]
    ics_content = "\r\n".join(header + events + footer) + "\r\n"

    with open(ics_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ics_content)
    return ics_path

def json_to_ics(roc_year: int, json_dir: str = "data/json", out_dir: str = "data/calendars") -> str:
    data = load_json_by_roc(roc_year, json_dir)
    return write_ics(roc_year, data, out_dir)

## 執行範例: python tw_calendar_json_to_ics.py {民國年}
## python tw_calendar_json_to_ics.py 115
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="從 data/json/{民國年}.json 產生 ICS（不連網）。")
    parser.add_argument("roc_year", type=int, help="民國年（例如 115）")
    parser.add_argument("--json-dir", default="data/json", help="JSON 資料夾（預設 data/json）")
    parser.add_argument("--out-dir",  default="data/calendars", help="ICS 輸出資料夾（預設 data/calendars）")
    args = parser.parse_args()

    data = load_json_by_roc(args.roc_year, args.json_dir)
    ics_path = write_ics(args.roc_year, data, args.out_dir)
    print(f"✅ 已輸出：{ics_path}")
