import requests
import sqlite3
from datetime import datetime

DB_NAME = "weather.db"

def fetch_and_save_weather():
    AREA_CODE = "130000"  # 東京
    AREA_NAME = "東京"
    URL = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{AREA_CODE}.json"

    res = requests.get(URL)
    res.raise_for_status()
    data = res.json()

    # ===== 天気・日付 =====
    time_series_weather = data[0]["timeSeries"][0]
    forecast_date = time_series_weather["timeDefines"][0][:10]
    weather = time_series_weather["areas"][0]["weathers"][0]

    # ===== 気温 =====
    temp_min = None
    temp_max = None

    temp_series = next(
        (s for s in data[0]["timeSeries"]
         if "temps" in s["areas"][0]),
        None
    )

    if temp_series:
        temps = temp_series["areas"][0]["temps"]
        if len(temps) >= 2:
            temp_min = temps[0]
            temp_max = temps[1]

    fetched_at = datetime.now().isoformat(timespec="seconds")

    # ===== DB保存 =====
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # area テーブル
    cur.execute("""
        INSERT OR IGNORE INTO area (area_code, area_name)
        VALUES (?, ?)
    """, (AREA_CODE, AREA_NAME))

    # forecast テーブル
    cur.execute("""
        INSERT OR IGNORE INTO forecast
        (area_code, forecast_date, weather, temp_min, temp_max, fetched_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (AREA_CODE, forecast_date, weather, temp_min, temp_max, fetched_at))

    conn.commit()
    conn.close()

    print("✅ 天気データをDBに保存しました")
    print(f"{forecast_date} / {AREA_NAME} / {weather}")

if __name__ == "__main__":
    fetch_and_save_weather()