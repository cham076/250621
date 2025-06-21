import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="Global Top 10 Market Cap Stocks", layout="wide")
st.title("📈 글로벌 시가총액 Top10 기업 - 최근 1년 주가 변화")

# 시가총액 기준 글로벌 Top 10 기업 (2025년 기준, 티커는 yfinance 기준)
top10_tickers = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'NVIDIA': 'NVDA',
    'Saudi Aramco': '2222.SR',
    'Alphabet (Google)': 'GOOGL',
    'Amazon': 'AMZN',
    'Berkshire Hathaway': 'BRK-B',
    'Meta': 'META',
    'Eli Lilly': 'LLY',
    'TSMC': 'TSM'
}

# 기간 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 데이터 수집
@st.cache_data
def get_stock_data(ticker):
    df = yf.download(ticker, start=start_date, end=end_date)
    return df['Adj Close']

# 데이터프레임 구성
price_df = pd.DataFrame()
for name, ticker in top10_tickers.items():
    try:
        price_df[name] = get_stock_data(ticker)
    except:
        st.warning(f"{name} ({ticker}) 데이터를 불러오지 못했습니다.")

# 시각화
fig = go.Figure()

for company in price_df.columns:
    fig.add_trace(go.Scatter(
        x=price_df.index,
        y=price_df[company],
        mode='lines',
        name=company
    ))

fig.update_layout(
    title="Global Top 10 Market Cap Companies - 1-Year Stock Price",
    xaxis_title="Date",
    yaxis_title="Adjusted Closing Price (USD or Local)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
