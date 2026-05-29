# 📈 台股 K 線技術分析儀表板

一個乾淨、美觀且實用的台股視覺化分析工具，使用 **Streamlit + Plotly** 開發。

適合個人使用、學習 Python 資料視覺化，以及放在履歷 / 接案作品集展示。

## ✨ 功能特色

- 支援**任意台股代碼**查詢（2330、0050、2882 等）
- 互動式 K 線圖 + 成交量
- 多種常用技術指標（可自由開關）：
  - 移動平均線（MA5、MA20、MA60）
  - 布林通道（Bollinger Bands）
  - RSI 指標
  - MACD 指標
- 時間區間選擇（1個月 ~ 全部歷史）
- 響應式設計，手機、平板、電腦皆可流暢使用

## 🖼️ 預覽
（部署上線後可在此插入截圖）

## 🚀 如何在本機執行

```bash
# 1. Clone 專案
git clone https://github.com/cheap-labor782/TW_stock_market.git
cd TW_stock_market

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 執行
streamlit run app.py
