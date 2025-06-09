
# weather_dashboard.py

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import mysql.connector
import plotly.express as px
from sklearn.linear_model import LinearRegression
from datetime import datetime
import logging
import os

# ✅ Page config must come FIRST before any other Streamlit command
st.set_page_config(page_title="🌍 Weather Dashboard", layout="wide")

# Set up logging
log_file = "logs/dashboard_log.txt"
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("✅ Streamlit dashboard script started with auto-refresh.")

# Auto-refresh every 2 minutes (120000 ms)
st_autorefresh(interval=120000, key="autorefresh")

# Title
st.title("📊 Global Weather Summary Dashboard")

# Connect to MySQL
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="weather_db"
    )
    cursor = conn.cursor()
    logging.info("✅ Connected to MySQL database.")
except Exception as e:
    logging.error(f"❌ Failed to connect to database: {e}")
    st.error(f"❌ Database connection failed: {e}")
    st.stop()

# Fetch data
query = "SELECT city, temperature_c, humidity, weather_desc, datetime_recorded FROM weather_data ORDER BY datetime_recorded DESC"
cursor.execute(query)
rows = cursor.fetchall()
cursor.close()
conn.close()
logging.info("✅ Data fetched successfully from database.")

# DataFrame
df = pd.DataFrame(rows, columns=["City", "Temperature (°C)", "Humidity (%)", "Weather", "Time"])
df["Time"] = pd.to_datetime(df["Time"])

# Filters
with st.sidebar:
    st.header("🔍 Filters")
    selected_cities = st.multiselect("Select Cities", df["City"].unique(), default=df["City"].unique())
    df = df[df["City"].isin(selected_cities)]


# --- Optional Smart Rain Alert System ---
with st.sidebar.expander("☔ Smart Rain Alert (AI)", expanded=False):
    selected_alert_city = st.selectbox("Select a city for rain alert", df["City"].unique())
    alert_df = df[df["City"] == selected_alert_city].sort_values("Time", ascending=False).head(3)
    st.write("📅 Recent records:")
    st.write(alert_df[["Time", "Temperature (°C)", "Humidity (%)", "Weather"]])

    if not alert_df.empty:
        latest = alert_df.iloc[0]
        humidity = latest["Humidity (%)"]
        desc = latest["Weather"].lower()
        rain_keywords = ["rain", "drizzle", "storm"]
        rain_signals = sum([1 for word in rain_keywords if word in desc])

        if humidity > 80 and rain_signals >= 1:
            st.error("☔ Rain likely tomorrow. Don’t forget your umbrella!")
        else:
            st.success("☀️ No rain expected. You're good to go!")
    # --- AI Temperature Prediction ---
    st.subheader("🔮 Next-Day Temperature Forecast")
    if len(alert_df) >= 2:
        from sklearn.linear_model import LinearRegression
        import numpy as np

        alert_df_sorted = alert_df.sort_values("Time")
        X = np.arange(len(alert_df_sorted)).reshape(-1, 1)
        y = alert_df_sorted["Temperature (°C)"].values
        model = LinearRegression().fit(X, y)
        next_day_pred = model.predict([[len(alert_df_sorted)]])[0]
        st.info(f"Predicted next-day temperature in {selected_alert_city}: {next_day_pred:.2f}°C")

        # Smart weather message
        if next_day_pred > 35:
            st.warning("🔥 It's going to be hot tomorrow. Stay hydrated!")
        elif next_day_pred < 5:
            st.warning("❄️ Cold day expected. Dress warmly!")
        else:
            st.success("🌤️ Mild weather expected tomorrow.")

    else:
        st.warning("Not enough data to make a forecast.")


# Latest Metrics
st.subheader("🌡️ Latest Weather by City")
latest = df.sort_values("Time").drop_duplicates("City", keep="first")
cols = st.columns(3)
for i, row in enumerate(latest.itertuples()):
    cols[i % 3].metric(label=f"{row.City}", value=f"{row._2}°C", delta=f"💧{row._3}% {row.Weather}")

# Table View
st.subheader("📋 All Weather Data")
st.dataframe(df.sort_values(by="Time", ascending=False), use_container_width=True)

# Pie Chart
st.subheader("🌦️ Weather Condition Breakdown")
fig_pie = px.pie(df, names="Weather", title="Weather Type Distribution")
st.plotly_chart(fig_pie, use_container_width=True)

# AI Forecast Table
st.subheader("🤖 AI Forecast: Next Day Temperature")
forecast_data = []
for city in df["City"].unique():
    city_df = df[df["City"] == city].copy()
    city_df["day"] = (city_df["Time"] - city_df["Time"].min()).dt.days
    if len(city_df) >= 2:
        model = LinearRegression()
        model.fit(city_df[["day"]], city_df["Temperature (°C)"])
        next_day = city_df["day"].max() + 1
        pred_temp = model.predict([[next_day]])[0]
        forecast_data.append({"City": city, "Forecast (Next Day °C)": round(pred_temp, 2)})
forecast_df = pd.DataFrame(forecast_data)
st.dataframe(forecast_df)

# Export button (manual only)
st.subheader("📥 Export to Excel")
if st.button("Download Excel File"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_file = f"data/weather_export_{timestamp}.xlsx"
    os.makedirs("data", exist_ok=True)
    df.to_excel(excel_file, index=False)
    with open(excel_file, "rb") as file:
        st.download_button(label="📥 Click to Download", data=file, file_name=excel_file)

logging.info("✅ Streamlit dashboard script completed.")
