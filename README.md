
# 🌦️ Weather ETL Project

This project demonstrates a complete ETL (Extract, Transform, Load) pipeline for collecting and visualizing real-time weather data.

## 🔧 Technologies Used

- **Python** – For ETL scripts
- **MySQL** – For storing cleaned weather data
- **Streamlit** – For building the interactive dashboard
- **OpenWeatherMap API** – Source of real-time weather data
- **Scikit-learn** – For simple AI temperature predictions

## 📁 Project Structure

```
Weather_ETL_Project/
│
├── bulk_weather_etl.py          # Extracts & loads weather data into MySQL
├── weather_dashboard.py         # Streamlit dashboard
├── mysql_weather_setup.sql      # SQL script to create weather table
├── requirements.txt             # Python dependencies
├── README.md                    # Project overview
└── env/                         # (Optional) Environment variables
```

## ⚙️ Features

- Real-time weather updates across 30 cities
- Dashboard visualizations (temperature, humidity, forecast)
- AI-powered temperature prediction
- Smart rain alert system
- Export data to Excel
- Optional: Auto-refresh and logging

## ▶️ How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Start the Streamlit dashboard
streamlit run weather_dashboard.py
```

## 📊 Example Dashboard View

Interactive bar charts, pie charts, and weather tables are available in the dashboard.

## 📬 Contact

Feel free to reach out for suggestions or questions.

## 🕒 Automation

This project includes an automation setup using a `.bat` script (`run_weather_dashboard.bat`) that can be scheduled to:
- Auto-refresh the weather data by re-running the ETL script.
- Automatically update MySQL with the latest weather info every 2 days.
- Run the Streamlit dashboard continuously with updated data.

**Note:** You can use Task Scheduler (Windows) or `cron` (Linux/macOS) to schedule the `.bat` file execution.
