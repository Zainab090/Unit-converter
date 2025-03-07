import streamlit as st
import time
import random
import requests
import qrcode
from io import BytesIO
from forex_python.converter import CurrencyRates

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="Mesmerizing Unit Converter",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Custom CSS -----------------
st.markdown("""
    <style>
    body { background-color: #0e1117; color: #ffffff; }
    .header { text-align: center; font-size: 42px; color: #ffcc00; font-weight: bold; text-shadow: 0px 0px 15px #ffcc00; }
    .subheader { text-align: center; font-size: 24px; color: #bbbbbb; }
    .container { text-align: center; background: #222; padding: 20px; border-radius: 15px; box-shadow: 0px 0px 10px #ffcc00; }
    .footer { position: fixed; bottom: 10px; width: 100%; text-align: center; font-size: 16px; color: gray; }
    .glow-button { background-color: #ffcc00; color: black; border-radius: 8px; padding: 12px; font-size: 20px; font-weight: bold; text-shadow: 0px 0px 8px #ffcc00; }
    .input-box { border-radius: 8px; padding: 10px; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# ----------------- App Title -----------------
st.markdown("<h1 class='header'>✨ Mesmerizing Unit Converter ✨</h1>", unsafe_allow_html=True)
st.write("### **Convert anything effortlessly with style! 🌟**")

# ----------------- Conversion Functions -----------------
def convert_length(value, from_unit, to_unit):
    conversion_factors = {
        "Meters": 1,
        "Kilometers": 0.001,
        "Miles": 0.000621371,
        "Feet": 3.28084,
        "Inches": 39.3701
    }
    return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

def convert_weight(value, from_unit, to_unit):
    conversion_factors = {
        "Kilograms": 1,
        "Grams": 1000,
        "Pounds": 2.20462,
        "Ounces": 35.274
    }
    return value * (conversion_factors[to_unit] / conversion_factors[from_unit])

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "Celsius":
        return value * 9/5 + 32 if to_unit == "Fahrenheit" else value + 273.15
    if from_unit == "Fahrenheit":
        return (value - 32) * 5/9 if to_unit == "Celsius" else (value - 32) * 5/9 + 273.15
    if from_unit == "Kelvin":
        return value - 273.15 if to_unit == "Celsius" else (value - 273.15) * 9/5 + 32

# ----------------- Sidebar -----------------
st.sidebar.title("🌍 Choose Conversion Type")
category = st.sidebar.radio("Select Category:", ["Length", "Weight", "Temperature", "Currency Exchange", "Generate QR Code"])

if category == "Length":
    st.write("### 📏 Length Converter")
    value = st.number_input("Enter value:", min_value=0.0, format="%.2f", key="length_value")
    from_unit = st.selectbox("From:", ["Meters", "Kilometers", "Miles", "Feet", "Inches"], key="length_from")
    to_unit = st.selectbox("To:", ["Meters", "Kilometers", "Miles", "Feet", "Inches"], key="length_to")
    if st.button("Convert", key="length_convert"):
        result = convert_length(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.2f} {to_unit}")

elif category == "Weight":
    st.write("### ⚖️ Weight Converter")
    value = st.number_input("Enter value:", min_value=0.0, format="%.2f", key="weight_value")
    from_unit = st.selectbox("From:", ["Kilograms", "Grams", "Pounds", "Ounces"], key="weight_from")
    to_unit = st.selectbox("To:", ["Kilograms", "Grams", "Pounds", "Ounces"], key="weight_to")
    if st.button("Convert", key="weight_convert"):
        result = convert_weight(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.2f} {to_unit}")

elif category == "Temperature":
    st.write("### 🌡️ Temperature Converter")
    value = st.number_input("Enter value:", format="%.2f", key="temp_value")
    from_unit = st.selectbox("From:", ["Celsius", "Fahrenheit", "Kelvin"], key="temp_from")
    to_unit = st.selectbox("To:", ["Celsius", "Fahrenheit", "Kelvin"], key="temp_to")
    if st.button("Convert", key="temp_convert"):
        result = convert_temperature(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.2f} {to_unit}")

elif category == "Currency Exchange":
    st.write("### 💰 Live Currency Converter")
    from_currency = st.selectbox("From Currency:", ["USD", "EUR", "GBP", "INR", "JPY", "AUD"], key="currency_from")
    to_currency = st.selectbox("To Currency:", ["USD", "EUR", "GBP", "INR", "JPY", "AUD"], key="currency_to")
    amount = st.number_input("Enter Amount:", min_value=0.0, format="%.2f", key="currency_amount")
    if st.button("Convert", key="currency_convert"):
        c = CurrencyRates()
        rate = c.get_rate(from_currency, to_currency)
        converted_amount = amount * rate
        st.success(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")

elif category == "Generate QR Code":
    st.write("### 📱 Generate QR Code")
    qr_text = st.text_input("Enter Text or URL:", key="qr_text")
    if st.button("Generate QR Code", key="qr_generate"):
        qr = qrcode.make(qr_text)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        st.image(buffer.getvalue(), caption="Your QR Code", use_column_width=True)

# ----------------- Footer -----------------
st.markdown("<p class='footer'>✨ Convert, Explore & Elevate with the Mesmerizing Converter! ✨</p>", unsafe_allow_html=True)
