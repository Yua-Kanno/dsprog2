from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
DB_NAME = "weather.db"

# ======================
# DBから天気を取得
# ======================
def get_forecast():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT
            area.area_name,
            forecast.forecast_date,
            forecast.weather,
            forecast.temp_min,
            forecast.temp_max
        FROM forecast
        JOIN area ON forecast.area_code = area.area_code
        ORDER BY forecast.forecast_date DESC
        LIMIT 1
    """)

    data = cur.fetchone()
    conn.close()
    return data

# ======================
# ルーティング
# ======================
@app.route("/")
def index():
    forecast = get_forecast()
    return render_template("index.html", forecast=forecast)

if __name__ == "__main__":
    app.run(debug=True)
