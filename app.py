import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="台股 K 線分析工具", layout="wide")
st.title("📈 台股 K 線技術分析儀表板")
st.markdown("**作者：趴元** | 一個用來練習與展示的台股分析工具")

# ====================== 側邊欄 ======================
with st.sidebar:
    st.header("🔍 查詢設定")
    
    stock_code = st.text_input("輸入台股代碼（例如：2330）", value="2330")
    if not stock_code.endswith(".TW"):
        stock_code += ".TW"
    
    period = st.selectbox("時間區間", 
                         ["1個月", "3個月", "6個月", "1年", "全部"], 
                         index=3)
    
    # 轉換成 yfinance 可用的 period
    period_map = {
        "1個月": "1mo", "3個月": "3mo", 
        "6個月": "6mo", "1年": "1y", "全部": "max"
    }
    
    show_volume = st.checkbox("顯示成交量", value=True)
    show_ma = st.checkbox("顯示移動平均線 (MA5, MA20, MA60)", value=True)
    show_boll = st.checkbox("顯示布林通道", value=True)
    show_rsi = st.checkbox("顯示 RSI", value=True)
    show_macd = st.checkbox("顯示 MACD", value=True)

# ====================== 取得資料 ======================
@st.cache_data(ttl=3600)  # 快取 1 小時
def get_stock_data(symbol, period):
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=period_map[period])
        if df.empty:
            st.error("無法取得資料，請確認股票代碼是否正確")
            return None
        return df
    except:
        st.error("資料取得失敗，請稍後再試")
        return None

df = get_stock_data(stock_code, period)

if df is not None and not df.empty:
    # 計算技術指標
    df['MA5'] = df['Close'].rolling(5).mean()
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA60'] = df['Close'].rolling(60).mean()
    
    # 布林通道
    df['BB_Mid'] = df['Close'].rolling(20).mean()
    df['BB_Std'] = df['Close'].rolling(20).std()
    df['BB_Upper'] = df['BB_Mid'] + 2 * df['BB_Std']
    df['BB_Lower'] = df['BB_Mid'] - 2 * df['BB_Std']
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['Histogram'] = df['MACD'] - df['Signal']

    # ====================== 主圖 ======================
    st.subheader(f"{stock_code.replace('.TW','')}  K 線圖")
    
    fig = go.Figure()
    
    # K 線
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="K 線"
    ))
    
    if show_ma:
        fig.add_trace(go.Scatter(x=df.index, y=df['MA5'], name='MA5', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name='MA20', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df.index, y=df['MA60'], name='MA60', line=dict(color='purple')))
    
    if show_boll:
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name='布林上軌', line=dict(dash='dash', color='gray')))
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name='布林下軌', line=dict(dash='dash', color='gray')))
    
    fig.update_layout(
        height=600,
        xaxis_title="日期",
        yaxis_title="股價 (TWD)",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ====================== 副圖 ======================
    col1, col2 = st.columns(2)
    
    with col1:
        if show_rsi:
            st.subheader("RSI 指標")
            fig_rsi = go.Figure()
            fig_rsi.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI'))
            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
            fig_rsi.update_layout(height=300, template="plotly_white")
            st.plotly_chart(fig_rsi, use_container_width=True)
    
    with col2:
        if show_macd:
            st.subheader("MACD 指標")
            fig_macd = go.Figure()
            fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue')))
            fig_macd.add_trace(go.Scatter(x=df.index, y=df['Signal'], name='Signal', line=dict(color='orange')))
            fig_macd.add_bar(x=df.index, y=df['Histogram'], name='Histogram', marker_color='gray')
            fig_macd.update_layout(height=300, template="plotly_white")
            st.plotly_chart(fig_macd, use_container_width=True)
    
    if show_volume:
        st.subheader("成交量")
        fig_vol = go.Figure()
        fig_vol.add_bar(x=df.index, y=df['Volume'], name='Volume')
        fig_vol.update_layout(height=300, template="plotly_white")
        st.plotly_chart(fig_vol, use_container_width=True)

    # 最新資料表格
    st.subheader("最近交易資料")
    st.dataframe(df.tail(10)[['Open','High','Low','Close','Volume']].round(2), use_container_width=True)

else:
    st.warning("請輸入正確的台股代碼")

st.caption("資料來源：Yahoo Finance | 此專案僅供學習與展示使用")