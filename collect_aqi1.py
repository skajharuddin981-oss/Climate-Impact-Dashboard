"""
collect_aqi.py
Fetch live Air Quality Index (AQI) readings for Indian cities from the WAQI API
(https://aqicn.org/api/) and store them in the MySQL table
climate_dashboard.air_quality_readings.

Setup (Windows PowerShell example):
    pip install requests mysql-connector-python
    setx WAQI_TOKEN "your_token_here"
    setx DB_PASSWORD "your_mysql_password"
(Close and reopen the terminal after setx.)

Run:
    python collect_aqi.py
"""
import os
import sys
import time

import requests
import mysql.connector

WAQI_TOKEN = os.environ.get("WAQI_TOKEN")  # never hard-code the token in the file
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": "climate_dashboard",
}

# Edit this list to match the cities you track.
# Bhubaneswar and Cuttack currently have no WAQI station, so they are skipped.
CITIES = [
    "delhi", "mumbai", "kolkata", "chennai", "bengaluru", "hyderabad",
    "pune", "ahmedabad", "jaipur", "lucknow", "kanpur", "chandigarh",
    "bhubaneswar", "cuttack",
]

INSERT_SQL = """
INSERT INTO air_quality_readings
    (city, station_name, aqi, pm25, pm10, no2, so2, co, o3,
     latitude, longitude, recorded_at, collected_at)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
"""


def fetch_city(city):
    """Return one reading dict for the city, or None if no data is available."""
    url = f"https://api.waqi.info/feed/{city}/"
    resp = requests.get(url, params={"token": WAQI_TOKEN}, timeout=20)
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("status") != "ok":
        return None

    data = payload["data"]
    try:
        aqi = int(data["aqi"])  # WAQI returns "-" when no value is available
    except (KeyError, TypeError, ValueError):
        return None

    iaqi = data.get("iaqi", {})

    def pollutant(key):
        value = iaqi.get(key, {}).get("v")
        return float(value) if value is not None else None

    geo = data.get("city", {}).get("geo") or [None, None]
    return (
        city,
        data.get("city", {}).get("name"),
        aqi,
        pollutant("pm25"), pollutant("pm10"), pollutant("no2"),
        pollutant("so2"), pollutant("co"), pollutant("o3"),
        geo[0], geo[1],
        data.get("time", {}).get("s"),
    )


def main():
    if not WAQI_TOKEN:
        sys.exit("WAQI_TOKEN environment variable is not set.")

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    saved, skipped = 0, []

    for city in CITIES:
        try:
            row = fetch_city(city)
        except requests.RequestException as exc:
            print(f"[error] {city}: {exc}")
            skipped.append(city)
            continue

        if row is None:
            print(f"[skip]  {city}: no monitoring station / no AQI value")
            skipped.append(city)
        else:
            cursor.execute(INSERT_SQL, row)
            saved += 1
            print(f"[ok]    {city}: AQI {row[2]}")
        time.sleep(1)  # be polite to the free API

    conn.commit()
    cursor.close()
    conn.close()
    print(f"\nSaved {saved} readings. Skipped: {', '.join(skipped) or 'none'}")


if __name__ == "__main__":
    main()
