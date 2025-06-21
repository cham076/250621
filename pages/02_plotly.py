import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import datetime
import pandas as pd

# 기본 설정
st.set_page_config(page_title="🌍 글로벌 TOP10 주가 변화", layout="wide")
st.title("📈 글로벌 시가총액 TOP10 기업의 최근 1년 주가 변화")

# 기업 목록 (2025 기준 Top 10 예상)
tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Meta (Facebook)": "META",
    "TSMC": "TSM",
    "Eli Lilly": "LLY"
}

# 날짜 범위
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365)

@st.cache_data(show_spinner=True)
def load_data():
    data = {}
    for name, symbol in tickers.items():
        try:
            df = yf.download(symbol, start=start_date, end=end_date)
            data[name] = df['Adj Close']
        except Exception as e:
            st.error(f"{name} ({symbol}) 데이터 불러오기 실패: {e}")
    return pd.DataFrame(data)

# 데이터 가져오기
df = load_data()

if df.empty:
    st.warning("📭 데이터를 불러오지 못했습니다.")
else:
    # Plotly 그래프 그리기
    fig = go.Figure()
    for name in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[name],
            mode='lines',
            name=name
        ))

    fig.update_layout(
        title="📊 최근 1년간 글로벌 시가총액 TOP10 기업 주가 변화",
        xaxis_title="📅 날짜",
        yaxis_title="💵 조정 종가 (USD)",
        template="plotly_white",
        hovermode="x unified",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
