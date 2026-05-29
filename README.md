# 📈 台股 K 線技術分析儀表板

一個現代化、互動式的台股技術分析工具，使用 **Streamlit + Plotly** 開發。

🔗 **線上體驗**：  
[https://twstockmarket-mvrknvck4utiaya5tasird.streamlit.app/](https://twstockmarket-mvrknvck4utiaya5tasird.streamlit.app/)

---

## ✨ 主要功能

- 支援**任意台股代碼**查詢（2330、0050、2881、TSMC 等）
- 美觀互動式 K 線圖
- 多種技術指標自由切換：
  - 移動平均線（MA5、MA20、MA60）
  - 布林通道
  - RSI 指標
  - MACD 指標
  - 成交量
- 多時間區間選擇（1個月 ~ 全部歷史）
- 響應式設計（手機、電腦皆可順暢使用）

## 🛠️ 技術棧

- **框架**：Streamlit
- **圖表**：Plotly
- **資料來源**：yfinance
- **資料處理**：Pandas

## 🚀 本地執行方式

```bash
git clone https://github.com/cheap-labor782/TW_stock_market.git
cd TW_stock_market
pip install -r requirements.txt
streamlit run app.py

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 執行
streamlit run app.py
