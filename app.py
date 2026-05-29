import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="台股 K 線分析工具", layout="wide", page_icon="📈")

st.title("📈 台股 K 線技術分析儀表板")
st.caption("**作者：趴元** | 作品展示專案")

# 側邊欄
with st.sidebar:
    st.header("🔍 股票查詢")
    stock_input = st.text_input("輸入台股代碼", value="2330", help="例如：2330, 0050, 2881").strip()
    stock_code = stock_input if stock_input.endswith(".TW") else stock_input + ".TW"
    
    period = st.selectbox("時間區間", ["1個月", "3個月", "6個月", "1年", "全部"], index=3)
    
    st.divider()
    st.subheader("顯示指標")
    show_volume = st.checkbox("成交量", value=True)
    show_ma = st.checkbox("移動平均線 (MA)", value=True)
    show_boll = st.checkbox("布林通道", value=True)
    show_rsi = st.checkbox("RSI", value=True)
    show_macd = st.checkbox("MACD", value=True)

# 取得資料
@st.cache_data(ttl=1800)
def get_stock_data(symbol, period_str):
    try:
        ticker = yf.Ticker(symbol)
        period_map = {"1個月":"1mo","3個月":"3mo","6個月":"6mo","1年":"1y","全部":"max"}
        df = ticker.history(period=period_map[period_str])
        return df if not df.empty else None
    except:
        return None

df = get_stock_data(stock_code, period)

if df is not None and not df.empty:
    # 計算指標
    df['MA5'] = df['Close'].rolling(5).mean()
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA60'] = df['Close'].rolling(60).mean()
    
    df['BB_Mid'] = df['Close'].rolling(20).mean()
    df['BB_Std'] = df['Close'].rolling(20).std()
    df['BB_Upper'] = df['BB_Mid'] + 2 * df['BB_Std']
    df['BB_Lower'] = df['BB_Mid'] - 2 * df['BB_Std']
    
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    exp12 = df['Close'].ewm(span=12, adjust=False).mean()
    exp26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp12 - exp26
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['Histogram'] = df['MACD'] - df['Signal']

    st.success(f"✅ 顯示 {stock_input} 的技術分析")

    # K線主圖
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="K線"))
    
    if show_ma:
        fig.add_trace(go.Scatter(x=df.index, y=df['MA5'], name="MA5", line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name="MA20", line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df.index, y=df['MA60'], name="MA60", line=dict(color='purple')))
    
    if show_boll:
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name="上軌", line=dict(dash='dash', color='gray')))
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name="下軌", line=dict(dash='dash', color='gray')))
    
    fig.update_layout(height=700, template="plotly_white", legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, use_container_width=True)

    # 副圖
    col1, col2 = st.columns(2)
    with col1:
        if show_rsi:
            st.subheader("RSI 指標")
            fig_rsi = go.Figure(go.Scatter(x=df.index, y=df['RSI']))
            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
            st.plotly_chart(fig_rsi, use_container_width=True)
    
    with col2:
        if show_macd:
            st.subheader("MACD 指標")
            fig_macd = go.Figure()
            fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD'))
            fig_macd.add_trace(go.Scatter(x=df.index, y=df['Signal'], name='Signal'))
            fig_macd.add_bar(x=df.index, y=df['Histogram'])
            st.plotly_chart(fig_macd, use_container_width=True)

    if show_volume:
        st.subheader("成交量")
        st.plotly_chart(go.Figure(go.Bar(x=df.index, y=df['Volume'])), use_container_width=True)

    st.subheader("最近10筆交易資料")
    st.dataframe(df.tail(10).round(2), use_container_width=True)

else:
    st.error("❌ 無法取得資料，請確認股票代碼是否正確")

st.caption("資料來源：Yahoo Finance | 此專案僅供學習與作品展示")
    st.dataframe(df.tail(10)[['Open', 'High', 'Low', 'Close', 'Volume']].round(2), use_container_width=True)

else:
    st.error("❌ 無法取得資料，請確認股票代碼是否正確（例如：2330、0050、2881）")

st.caption("資料來源：Yahoo Finance | 僅供學習與作品展示使用")
