import requests
import mysql.connector
from datetime import datetime

# === Settings ===
API_KEY = "f886b0b73f720967ef18e5939d13c2b4"
cities = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "London", "Paris", "Berlin", "Madrid", "Rome",
    "Tokyo", "Seoul", "Beijing", "Bangkok", "Singapore",
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Cairo", "Istanbul", "Moscow", "Johannesburg", "Lagos",
    "Sydney", "Melbourne", "Toronto", "Mexico City", "Rio de Janeiro"
]

log_file = open("weather_log.txt", "a", encoding="utf-8")


def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_msg = f"[{timestamp}] {message}"
    print(full_msg)
    log_file.write(full_msg + "\n")

# Connect to MySQL
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="weather_db"
    )
    cursor = conn.cursor()
    log("✅ Connected to MySQL database.")
except Exception as e:
    log(f"❌ Database connection failed: {e}")
    log_file.close()
    exit()

# Fetch and store data
for city in cities:
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp_c = round(data["main"]["temp"] - 273.15, 2)
            humidity = data["main"]["humidity"]
            desc = data["weather"][0]["description"]
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            query = """
            INSERT INTO weather_data (city, temperature_c, humidity, weather_desc, datetime_recorded)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (city, temp_c, humidity, desc, now)
            cursor.execute(query, values)
            log(f"✅ {city} saved successfully.")

        else:
            log(f"⚠️ {city} failed – API error: {data.get('message')}")

    except Exception as e:
        log(f"❌ {city} error occurred: {e}")

conn.commit()
cursor.close()
conn.close()
log("🎉 All data inserted and database closed.")
log_file.close()
