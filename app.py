import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Smart Price Alert System", layout="wide")

st.title("🔔 Smart Multi-Product Price Alert System")

# =========================
# EMAIL CONFIG
# =========================
SENDER_EMAIL = "mandeepsinghnegi_bca24_27@its.edu.in"
APP_PASSWORD = "Hero@2006HERO"

# =========================
# PRICE GENERATOR (Simulated)
# =========================
def generate_price(base):
    fluctuation = random.randint(int(base * -0.05), int(base * 0.05))
    return base + fluctuation

# =========================
# SEND EMAIL FUNCTION
# =========================
def send_email(receiver_email, product, price):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = f"Price Alert for {product} 🚨"

        body = f"""
        Good News!

        The price of {product} has dropped to ₹{price}.
        This meets your target price.

        Hurry up and buy now!
        """

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()

        return True
    except:
        return False

# =========================
# USER INPUT
# =========================
product_name = st.text_input("Enter Product Name")
base_price = st.number_input("Enter Approx Current Price", min_value=100, value=1000)
target_price = st.number_input("Enter Your Target Price", min_value=100, value=900)
user_email = st.text_input("Enter Your Email for Alert")

if st.button("Start Monitoring"):

    if product_name and user_email:

        current_price = generate_price(base_price)

        st.subheader("Current Price Check")
        st.write(f"Current Price of {product_name}: ₹ {current_price}")

        if current_price <= target_price:

            email_status = send_email(user_email, product_name, current_price)

            if email_status:
                st.success("🎉 Price dropped! Email alert sent successfully.")
            else:
                st.error("Email sending failed. Check credentials.")

        else:
            st.info("Price not yet at your target. Keep monitoring!")

    else:
        st.warning("Please fill all fields.")
