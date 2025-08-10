# Taiwan Government Office Calendar to ICS

使用Python撰寫，此專案為Vibe Code

本專案提供轉換 **中華民國政府行政機關辦公日曆表** 成 `.ics` 行事曆檔案的工具，  
支援直接從 CSV（含修正版優先）轉換為 JSON，再輸出為標準 ICS，可匯入 Google Calendar、Apple Calendar、Outlook 等軟體。

## 功能特色
- 📂 **CSV → JSON → ICS** 自動化流程
- 📌 **支援修正版 CSV 優先**：同一年若有修正版檔案，會自動優先使用
- 🗓 **民國年輸入**：指令輸入民國年，例如 `115` 表示西元 2026 年
- 💾 **資料夾結構自動建立**：
  - `data/中華民國政府行政機關辦公日曆表/` — 原始 CSV 檔
  - `data/json/` — 轉換後的 JSON
  - `data/calendars/` — 轉換後的 ICS
- 🏷 **ICS 格式**：
  - `SUMMARY:放假日`
  - `CATEGORIES:dayoff`
  - `DESCRIPTION`：中華民國與西元年份
  - `UID`、`DTSTAMP` 自動生成

## 資料來源/格式
- [政府資料開放平台](https://data.gov.tw/dataset/14718)
- 政府行政機關公告的年度辦公日曆表 CSV
    - 例如: 114年中華民國政府行政機關辦公日曆表(修正版).csv
    - 例如: 115年中華民國政府行政機關辦公日曆表.csv

- JSON 格式
```
[
  {
    "date": "20230101",
    "week": "日",
    "isHoliday": true,
    "description": "開國紀念日"
  },
  {
    "date": "20230102",
    "week": "一",
    "isHoliday": true,
    "description": "補假"
  },
  {
    "date": "20230103",
    "week": "二",
    "isHoliday": false,
    "description": ""
  }
]
```
- ICS 格式
```
SUMMARY:放假日
STATUS:CONFIRMED
TRANSP:TRANSPARENT
DTSTART;VALUE=DATE:20260501
DTSTAMP:20250809T164843
CATEGORIES:dayoff
DESCRIPTION:中華民國115年（西元2026年）政府行政機關辦公日曆表
END:VEVENT
BEGIN:VEVENT
UID:2f73171b-f84c-4ad1-b0c2-b5aca0899be8
```

## 專案結構
```
├── data/
│ ├── 中華民國政府行政機關辦公日曆表/ # 原始 CSV 放這裡
│ │ ├── 115年中華民國政府行政機關辦公日曆表.csv
│ │ └── 115年中華民國政府行政機關辦公日曆表(修正版).csv
│ ├── json/ # JSON 輸出
│ └── calendars/ # ICS 輸出
├── tw_calendar_csv_to_json.py # CSV → JSON（修正版優先）
├── tw_calendar_json_to_ics.py # JSON → ICS
├── tw_calendar.py # 整合工具（民國年 → JSON → ICS）
└── README.md
```
## 執行程式 (115年為範例)
### tw_calendar.py (CSV→JSON→ICS)
```
python tw_calendar.py 115
```
### tw_calendar_csv_to_json.py (CSV→JSON)
```
python tw_calendar_csv_to_json.py 115
```
### tw_calendar_json_to_ics.py (JSON→ICS)
```
python tw_calendar_json_to_ics.py 115
```

## 參考資料
[ruyut/TaiwanCalendar](https://github.com/ruyut/TaiwanCalendar)

[Diana's Lab](https://gitlab.com/ntusthcilab/twgocal)