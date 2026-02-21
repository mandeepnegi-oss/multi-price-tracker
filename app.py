import streamlit as st
import pandas as pd
import random
import datetime
from sklearn.linear_model import LinearRegression
import numpy as np
import os

st.set_page_config(page_title="Smart Price Tracker", layout="centered")

st.title("🛒 Multi-Ecommerce Smart Price Tracker")
st.markdown("AI-Based Price Comparison & Prediction System")

product_name = st.text_input("Enter Product Name", "iPhone 15 Pro")
base_price = st.number_input("Enter Approx Base Price", value=75000)

def generate_price(base):
    fluctuation = random.randint(-3000, 3000)
    return base + fluctuation

if st.button("Check Latest Prices"):

    flipkart_price = generate_price(base_price)
    amazon_price = generate_price(base_price - 500)

    st.subheader("📦 Today's Prices")
    st.write(f"Flipkart: ₹{flipkart_price}")
    st.write(f"Amazon: ₹{amazon_price}")

    today = datetime.datetime.now()

    new_data = {
        "Date": [today],
        "Flipkart": [flipkart_price],
        "Amazon": [amazon_price]
    }

    new_df = pd.DataFrame(new_data)

    if os.path.exists("price_history.csv"):
        old_df = pd.read_csv("price_history.csv")
        df = pd.concat([old_df, new_df], ignore_index=True)
    else:
        df = new_df

    df.to_csv("price_history.csv", index=False)

    st.success("✅ Price history updated.")

    # Best Deal Logic
    if flipkart_price < amazon_price:
        st.success("🔥 Best Deal Today: Flipkart")
    elif amazon_price < flipkart_price:
        st.success("🔥 Best Deal Today: Amazon")
    else:
        st.info("⚖ Both platforms have same price")

    # Smart Alert
    lowest_flipkart = df["Flipkart"].min()
    lowest_amazon = df["Amazon"].min()

    if flipkart_price == lowest_flipkart:
        st.warning("🚨 Flipkart price is lowest ever recorded!")

    if amazon_price == lowest_amazon:
        st.warning("🚨 Amazon price is lowest ever recorded!")

    # AI Prediction
    if len(df) > 1:
        df["Index"] = range(len(df))
        X = df[["Index"]]
        y = df["Flipkart"]

        model = LinearRegression()
        model.fit(X, y)

        next_day = np.array([[len(df)]])
        prediction = model.predict(next_day)

        st.info(f"🤖 Predicted Next Flipkart Price: ₹{int(prediction[0])}")

        st.subheader("📊 Price Trend Graph")
        st.line_chart(df[["Flipkart", "Amazon"]])

    else:
        st.info("Run multiple times to activate AI prediction.")