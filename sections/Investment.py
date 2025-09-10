import streamlit as st
import pandas as pd
import yfinance as yf
import os
import json
from sklearn.linear_model import LinearRegression
import numpy as np
import altair as alt

DATA_FILE = "data_invest.json"

# ------------------------
# JSON Data Loading & Saving
# ------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"portfolio": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ------------------------
# Prediction Function
# ------------------------
def predict_prices(df, days=7):
    df = df.reset_index()
    df["t"] = np.arange(len(df))
    X = df[["t"]]
    y = df["Close"]

    model = LinearRegression()
    model.fit(X, y)

    future_t = np.arange(len(df), len(df) + days).reshape(-1, 1)
    future_pred = model.predict(future_t)

    future_dates = pd.date_range(start=df["Date"].iloc[-1] + pd.Timedelta(days=1), periods=days)
    pred_df = pd.DataFrame({"Date": future_dates, "Predicted": future_pred})
    return pred_df

# ------------------------
# Main Display
# ------------------------
def show():
    st.title("Investment Tracker")

    data = load_data()

    # ------------------------
    # Add Asset
    # ------------------------
    st.subheader("Add Asset to Portfolio")
    with st.form("add_asset"):
        asset_type = st.selectbox("Select Asset Type:", ["Stock", "Gold", "Crypto"])
        symbol = st.text_input("Enter Symbol (e.g. AAPL, BTC-USD, XAUUSD=X):")
        amount = st.number_input("Amount Owned ($):", min_value=0.0, step=0.1)
        note = st.text_area("Optional Note:")
        submitted = st.form_submit_button("Add to Portfolio")

        if submitted and symbol.strip() != "":
            new_entry = {
                "type": asset_type,
                "symbol": symbol.strip().upper(),
                "amount": amount,
                "note": note.strip()
            }
            data["portfolio"].append(new_entry)
            save_data(data)
            st.success(f"{symbol.upper()} ({asset_type}) added to your portfolio!")
            st.rerun()

    # ------------------------
    # Portfolio
    # ------------------------
    st.subheader("Your Portfolio")
    if data["portfolio"]:
        for idx, asset in enumerate(data["portfolio"]):
            col1, col2, col3 = st.columns([0.3, 0.5, 0.2])
            with col1:
                st.markdown(f"**{asset['symbol']}** ({asset['type']})")
            with col2:
                st.write(f"{asset['amount']} $")
                if asset["note"]:
                    st.caption(asset["note"])
            with col3:
                if st.button("Delete", key=f"del_asset_{idx}"):
                    data["portfolio"].pop(idx)
                    save_data(data)
                    st.rerun()
    else:
        st.info("No assets in your portfolio yet.")

    # ------------------------
    # Analyze
    # ------------------------
    st.warning("⚠️ This is not financial advice. Predictions are for educational purposes only.")
    st.subheader("Analyze Asset")
    if data["portfolio"]:
        selected_symbol = st.selectbox(
            "Choose Asset:",
            [f"{a['symbol']} ({a['type']})" for a in data["portfolio"]]
        )

        if st.button("Fetch & Predict"):
            symbol_only = selected_symbol.split()[0]

            try:
                df = yf.download(symbol_only, period="6mo")

                if df.empty:
                    st.error("No data found for this symbol.")
                    return

                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)

                df["Close"] = df["Close"].squeeze()

                st.write(f"Last Prices for {symbol_only}:")
                st.dataframe(df.tail())

                # Predict
                pred_df = predict_prices(df, days=7)

                # Plot
                df_reset = df.reset_index()[["Date", "Close"]]
                df_reset["Type"] = "Historical"
                pred_df["Type"] = "Predicted"
                pred_df = pred_df.rename(columns={"Predicted": "Close"})

                combined = pd.concat([df_reset, pred_df])

                chart = alt.Chart(combined).mark_line(point=True).encode(
                    x="Date:T",
                    y="Close:Q",
                    color="Type:N"
                ).properties(
                    width=800,
                    height=400,
                    title=f"{symbol_only} Price Prediction"
                )

                st.altair_chart(chart, use_container_width=True)

            except Exception as e:
                st.error(f"Error fetching data: {e}")
    else:
        st.info("Add some assets to analyze.")
