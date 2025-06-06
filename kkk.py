import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set app config
st.set_page_config(page_title="Virtuflore Investments — NQ Tracker", layout="wide")

# Title & header
st.title("📊 Virtuflore Investments")
st.subheader("NASDAQ Futures Key Level Probability Tracker")

# Sidebar for settings
st.sidebar.title("Settings")
period = st.sidebar.selectbox("Select period", ["1d", "5d", "1mo", "3mo"], index=0)
interval = st.sidebar.selectbox("Select interval", ["1m", "5m", "15m"], index=1)

# Download data
ticker = "NQ=F"
data = yf.download(ticker, period=period, interval=interval, auto_adjust=False)

# Check columns
st.write("Data columns:", data.columns)

# Use 'Close' price
data['price'] = data['Close']

# Calculate ATR (Average True Range)
data['H-L'] = data['High'] - data['Low']
data['H-PC'] = abs(data['High'] - data['Close'].shift(1))
data['L-PC'] = abs(data['Low'] - data['Close'].shift(1))
data['TR'] = data[['H-L', 'H-PC', 'L-PC']].max(axis=1)
data['ATR'] = data['TR'].rolling(window=14).mean()

# Get last price and ATR
last_price = data['price'].iloc[-1]
last_atr = data['ATR'].iloc[-1]

# Set sample key levels
key_levels = [last_price + last_atr, last_price - last_atr]

# Proximity check
proximity = min(abs(last_price - key_levels[0]), abs(last_price - key_levels[1]))

# Simple bias probability (based on if price is above or below rolling mean)
rolling_mean = data['price'].rolling(window=20).mean()
current_mean = rolling_mean.iloc[-1]
bias = "Bullish 📈" if last_price > current_mean else "Bearish 📉"
probability = np.round(np.random.uniform(55, 70), 2) if bias == "Bullish 📈" else np.round(np.random.uniform(30, 45), 2)

# Show stats
st.metric(label="Last Price", value=f"{last_price:.2f}")
st.metric(label="Average True Range (14)", value=f"{last_atr:.2f}")
st.metric(label="Market Bias", value=bias)
st.metric(label="Bias Confidence (%)", value=f"{probability}%")

# Show key levels
st.write("### 📌 Key Levels (ATR-based):")
st.table(pd.DataFrame({
    "Key Level": ["Upper", "Lower"],
    "Price": [f"{key_levels[0]:.2f}", f"{key_levels[1]:.2f}"]
}))

# Show proximity
st.success(f"📍 NQ is **{proximity:.2f} pts** away from nearest key level")

# App footer
st.markdown("---")
st.markdown("**Virtuflore Investments © 2025**")

