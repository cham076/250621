import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import datetime
import pandas as pd

# 제목
st.set_page_config(page_title="🌍 글로벌 시가총액 TOP10 주가 변화", layout="wide")
st.markdown("# 📈 글로벌 시가총액 TOP10 기업의 최근 1년 주가 변화")

# 티커 목록 (2025 기준 추정)
tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Meta (Facebook)": "META",
    "TSMC": "TSM",
    "Eli Lilly": "LLY"
}

# 날짜 설정
end = datetime.date.today()
start = end - datetime.timedelta(days=365)

# 데이터 수집
@st.cache_data
def load_data():
    price_data = {}
    for name, symbol in tickers.items():
        try:
            df = yf.download(symbol, start=start, end=end)
            price_data[name] = df['Adj Close']
        except:
            continue
    return pd.DataFrame(price_data)

data = load_data()

# Plotly 그래프
fig = go.Figure()
for company in data.columns:
    fig.add_trace(go.Scatter(x=data.index, y=data[company],
                             mode='lines', name=company))

fig.update_layout(
    title="최근 1년 간 글로벌 시가총액 TOP10 기업의 주가 변화 📊",
    xaxis_title="날짜",
    yaxis_title="주가 (USD)",
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
