import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="Global Top 10 Market Cap Stocks", layout="wide")
st.title("📈 글로벌 시가총액 Top10 기업 - 최근 1년 주가 변화")

# 시가총액 기준 글로벌 Top10 기업 (2025년 추정, 일부는 yfinance에서 예외 처리)
top10_tickers = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'NVIDIA': 'NVDA',
    'Alphabet (Google)': 'GOOGL',
    'Amazon': 'AMZN',
    'Berkshire Hathaway': 'BRK-B',  # 마이너스 포함되면 오류나므로 처리 필요
    'Meta': 'META',
    'Eli Lilly': 'LLY',
    'TSMC': 'TSM',
    'Broadcom': 'AVGO'  # Saudi Aramco 대체로 안정적 티커 사용
}

# 기간 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 데이터 수집 함수
@st.cache_data
def get_stock_data(ticker):
    # 마이너스(-)가 있는 티커는 yfinance에서 . 으로 대체해야 동작
    safe_ticker = ticker.replace('-', '.')
    df = yf.download(safe_ticker, start=start_date, end=end_date, progress=False)
    if 'Adj Close' in df.columns and not df.empty:
        return df['Adj Close']
    else:
        return None

# 데이터프레임 생성
price_df = pd.DataFrame()
missing = []

for name, ticker in top10_tickers.items():
    data = get_stock_data(ticker)
    if data is not None:
        price_df[name] = data
    else:
        missing.append(name)

# 경고 출력
if missing:
    st.warning(f"다음 종목은 데이터를 불러오지 못했습니다: {', '.join(missing)}")

# 시각화
if not price_df.empty:
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
        yaxis_title="Adjusted Closing Price (USD)",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("유효한 주식 데이터를 불러올 수 없습니다. 인터넷 연결 또는 티커명을 확인해주세요.")
