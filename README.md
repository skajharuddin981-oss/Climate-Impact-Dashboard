# 🌍 Live Climate Impact Dashboard — Indian Cities Air Quality

An end-to-end data project that collects **live Air Quality Index (AQI)** data for Indian cities, stores it in **MySQL**, and visualises it in an interactive **Power BI** dashboard that refreshes with new data every day.

![Dashboard](images/dashboard.png)

## 🎯 Problem Statement
Air pollution is a serious public-health issue in India, but city-wise data is scattered and hard to compare. This project builds an automated pipeline and dashboard that answers:
- Which cities have the worst air quality right now?
- How does AQI change over time in each city?
- Which pollutants (PM2.5, PM10, NO₂, SO₂, CO, O₃) drive the readings?

## 🛠️ Tech Stack
| Layer | Tool |
|---|---|
| Data source | [WAQI API](https://aqicn.org/api/) (free token) |
| Collection | Python (`requests`, `mysql-connector-python`) |
| Storage | MySQL |
| Automation | Windows Task Scheduler (daily run) |
| Visualisation | Power BI Desktop |

## 🔄 Architecture
```
WAQI API  →  Python script  →  MySQL (climate_dashboard)  →  Power BI  →  Dashboard
                ↑
        Windows Task Scheduler (daily)
```

## 🗄️ Database Design
Table: `air_quality_readings`

| Column | Type | Description |
|---|---|---|
| id | INT (PK, auto) | Unique reading ID |
| city | VARCHAR(80) | City name |
| station_name | VARCHAR(150) | Monitoring station |
| aqi | INT | Air Quality Index |
| pm25, pm10, no2, so2, co, o3 | FLOAT | Pollutant levels |
| latitude, longitude | FLOAT | Station location (for the map) |
| recorded_at | VARCHAR(30) | Time reported by the station |
| collected_at | DATETIME | Time my script collected it |

Full SQL (table creation + analysis queries): [`queries.sql`](queries.sql)

## 📊 Dashboard Visuals
- **Map** – average AQI by city (bubble per city)
- **Bar chart** – average AQI ranked by city
- **Line chart** – AQI trend over time for each city
- **Detail table** – city, AQI, AQI category, PM2.5, PM10 and recorded time

## 🔍 Key Findings (snapshot from the dashboard)
- **Pune** shows the highest average AQI in this snapshot (≈ 230, *Very Unhealthy*), followed by **Kolkata**, **Delhi** and **Mumbai**.
- Most large north-Indian cities (**Delhi, Kanpur, Jaipur, Lucknow**) fall in the *Unhealthy* or *Unhealthy for Sensitive Groups* range.
- **Chandigarh** and **Bengaluru** record the lowest values (*Moderate*).
- Delhi's AQI rose across consecutive days in late October (e.g. 142 → 154 → 184 → 189).

> Numbers change with every refresh as new daily readings are added.

## ⚠️ Data Notes & Limitations
- WAQI has **no monitoring station for Bhubaneswar and Cuttack**, so these cities are skipped by the script.
- Some stations report **old timestamps** (`recorded_at`), so a few rows show readings from earlier dates. I keep both `recorded_at` (station time) and `collected_at` (my collection time) to handle this.
- AQI values are point-in-time readings, not 24-hour averages.

## ▶️ How to Run
1. Create a free token at https://aqicn.org/data-platform/token/
2. Run `queries.sql` in MySQL to create the database and table.
3. Install packages: `pip install requests mysql-connector-python`
4. Set environment variables `WAQI_TOKEN` and `DB_PASSWORD`.
5. Run `python collect_aqi.py` (schedule it daily with Windows Task Scheduler).
6. Open `climate_dashboard.pbix` in Power BI, connect it to MySQL and click **Refresh**.

## 📁 Project Structure
```
├── collect_aqi.py          # Python data-collection script
├── queries.sql             # Database + analysis queries
├── climate_dashboard.pbix  # Power BI dashboard
├── images/
│   └── dashboard.png       # Dashboard screenshot
└── README.md
```

## 🚀 Future Improvements
- Add AQI health-advice labels and alerts when AQI crosses 200
- Add more cities and a year-on-year comparison
- Publish the report to Power BI Service for online auto-refresh

## 👤 Author
**Sk. Ajharuddin (Ayaan)** — Aspiring Data Analyst · Cuttack, Odisha
[LinkedIn](https://www.linkedin.com/in/sk-ajharuddin-a37787371/) · [GitHub](https://github.com/skajharuddin981-oss)
