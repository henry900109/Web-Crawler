# Web Scraping Project

## 聲明

本專案為大數據股份有限公司數據實習工程師 (長期) / Data Engineer Intern 預面試考題。

本專案的部分內容參考了網路資源並有使用 ChatGPT 協助撰寫與註解。

## 問題一：

爬取 PTT 熱門看板的列表名稱與網址  
例：列表名稱 Gossiping  
網址 https://www.ptt.cc/bbs/Gossiping/index.html  
**回答**:  
`Q1.py` 的執行結果儲存在 `question1.txt` 中。

## 問題二：

爬取八卦看板內 7 天內的貼文與留言

1. 貼文資料需包含作者、標題、發文時間、內文、類別
2. 留言資料需包含作者、發文時間、內文
3. 每則貼文與所屬留言存成一個檔案  
   **回答**:  
   `Q2.py` 的執行結果儲存在 `file` 資料夾中，每個檔案名稱為貼文標題（`.txt`）。

## 問題三（加分題）：

爬取「古騰堡計劃」前兩百本中文電子書  
網址：https://www.gutenberg.org/browse/languages/zh  
每本書為一個檔案，檔案名稱為書名  
每本書需抓取標題、作者、時間、內文  
**回答**:  
`Q3.py` 的執行結果儲存在 `file` 資料夾中，每個檔案名稱為書名（`.txt`）。

## 檔案配置 :

/WEB CRAWLER
│
├── Q1
│ ├── Q1.py
│ └── question1.txt
│
├── Q2
│ ├── Q2.py
│ └── file
│ └── 貼文標題.txt
│ └── ...（其他貼文檔案）
│
└── Q3
├── Q3.py
└── file
└── 書名.txt
└── ...（其他書籍檔案）
