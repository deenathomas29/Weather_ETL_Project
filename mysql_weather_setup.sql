
CREATE DATABASE IF NOT EXISTS weather_db;

USE weather_db;

CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100),
    temperature_c FLOAT,
    humidity INT,
    weather_desc VARCHAR(100),
    datetime_recorded DATETIME
);
