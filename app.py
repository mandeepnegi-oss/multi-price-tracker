import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Multi Product Price Tracker", layout="wide")

st.title("🛒 Multi-Product Smart Price Tracker")

# =============================
# FUNCTION TO GENERATE PRICE
# =============================
def generate_price(base):
    fluctuation = random.randint(int(base * -0.05), int(base * 0.05))
    return base + fluctuation

# =============================
# USER INPUT
# =============================
product_name = st.text_input("Enter Product Name")
base_price = st.number_input("Enter Approx Base Price", min_value=100, value=1000)

track_button = st.button("Track Product")

# =============================
# TRACK PRODUCT
# =============================
if track_button and product_name:

    filename = f"{product_name.replace(' ', '_')}.csv"

    flipkart_price = generate_price(base_price)
    amazon_price = generate_price(base_price)

    today = datetime.now().strftime("%Y-%m-%d")

    new_data = pd.DataFrame({
        "Date": [today],
        "Flipkart": [flipkart_price],
        "Amazon": [amazon_price]
    })

    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data

    df.to_csv(filename, index=False)

    st.success(f"{product_name} Added Successfully!")

# =============================
# SHOW TRACKED PRODUCTS
# =============================
st.header("📦 Tracked Products")

csv_files = [f for f in os.listdir() if f.endswith(".csv")]

if csv_files:

    selected_file = st.selectbox("Select Product to View", csv_files)

    df = pd.read_csv(selected_file)

    st.subheader("Price History")
    st.dataframe(df)

    # =============================
    # GRAPH
    # =============================
    st.subheader("📈 Price Trend")

    df["Day"] = np.arange(len(df))

    plt.figure()
    plt.plot(df["Day"], df["Flipkart"])
    plt.plot(df["Day"], df["Amazon"])
    st.pyplot(plt)

    # =============================
    # AI PREDICTION
    # =============================
    if len(df) > 1:

        X = df[["Day"]]
        y = df["Flipkart"]

        model = LinearRegression()
        model.fit(X, y)

        next_day = np.array([[len(df)]])
        predicted_price = model.predict(next_day)[0]

        st.subheader("🤖 AI Prediction")
        st.write(f"Predicted Flipkart Price Tomorrow: ₹ {round(predicted_price, 2)}")

else:
    st.info("No products tracked yet.")
