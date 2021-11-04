import streamlit as st
import pandas as pd
import datetime
import yfinance as yf
import plotly.graph_objects as go



# App title
st.markdown('''
# Stock Price App
This app is showing the stock price data for query companies!

**On this app you can:**
- Pick a ticker from the list
- Pick date range
---
''')

# Sidebar
st.sidebar.subheader('Query Parameters')

start_date = st.sidebar.date_input("Start Date", datetime.date(2016, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date.today())


# Ritriving Ticker Data
ticker_list = pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents_symbols.txt')
ticker_symbol = st.sidebar.selectbox('Stock ticker', ticker_list)
ticker_data = yf.Ticker(ticker_symbol)
ticker_df = ticker_data.history(period='1d', start=start_date, end=end_date)
ticker_df = ticker_df.reset_index()
ticker_df['Date'] = ticker_df['Date'].dt.date
# print(ticker_df)

# Ticker Information
company_logo = '<img src=%s>' % ticker_data.info['logo_url']
st.markdown(company_logo, unsafe_allow_html=True)

company_name = ticker_data.info['longName']
st.header(company_name)

info_checkbox = st.checkbox('Show company information')
if info_checkbox == True:
    company_summary = ticker_data.info['longBusinessSummary']
    st.info(company_summary)    

st.markdown('---')
current_price = ticker_data.info['currentPrice']

st.subheader(ticker_symbol)
st.subheader('Current Price ' + str(current_price))
fig = go.Figure(data=[go.Candlestick(x=ticker_df['Date'], open=ticker_df['Open'], high=ticker_df['High'], low=ticker_df['Low'], close=ticker_df['Close'], name=ticker_symbol)])
# fig.add_trace(go.Candlestick(x=ticker_df['Date'], open=ticker_df['Open'], high=ticker_df['High'], low=ticker_df['Low'], close=ticker_df['Close'], name=ticker_symbol))

fig.update_xaxes(type='category')
fig.update_layout(height=600)

st.plotly_chart(fig, use_container_width=True)

# Ticker Data
st.subheader('Stock Data')
st.write(ticker_df)




# longName
# logo_url
# website
# sector
# symbol
# longBusinessSummary
# currentPrice
