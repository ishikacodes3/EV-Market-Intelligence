from flask import Flask, render_template, request, jsonify, send_file
import sqlite3, os, pandas as pd
from pathlib import Path

app = Flask(__name__)
ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "ev_market.db"
CSV_PATH = ROOT / "data" / "ev_market_data.csv"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    if not DB_PATH.exists():
        df = pd.read_csv(CSV_PATH)
        conn = sqlite3.connect(DB_PATH)
        df.to_sql("ev_vehicles", conn, if_exists="replace", index=False)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_year ON ev_vehicles(year)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_manufacturer ON ev_vehicles(manufacturer)")
        conn.commit()
        conn.close()

def filters_from_request():
    return {
        "year": request.args.get("year", "All"),
        "category": request.args.get("category", "All"),
        "manufacturer": request.args.get("manufacturer", "All"),
    }

def where_clause(filters):
    clauses, params = [], []
    for key, col in [("year","year"),("category","category"),("manufacturer","manufacturer")]:
        val = filters[key]
        if val != "All":
            clauses.append(f"{col} = ?")
            params.append(int(val) if key == "year" else val)
    return (" WHERE " + " AND ".join(clauses) if clauses else ""), params

def query_df(sql, params=()):
    with get_conn() as conn:
        return pd.read_sql_query(sql, conn, params=params)

@app.route("/")
def index():
    with get_conn() as conn:
        years = [r[0] for r in conn.execute("SELECT DISTINCT year FROM ev_vehicles ORDER BY year").fetchall()]
        categories = [r[0] for r in conn.execute("SELECT DISTINCT category FROM ev_vehicles ORDER BY category").fetchall()]
        manufacturers = [r[0] for r in conn.execute("SELECT DISTINCT manufacturer FROM ev_vehicles ORDER BY manufacturer").fetchall()]
    return render_template("index.html", years=years, categories=categories, manufacturers=manufacturers)

@app.route("/api/dashboard")
def dashboard_data():
    f = filters_from_request()
    w,p = where_clause(f)
    kpis = query_df(f"""SELECT SUM(annual_sales) total_sales, COUNT(*) vehicle_models,
        ROUND(AVG(driving_range_km),1) avg_range, ROUND(AVG(customer_rating),2) avg_rating,
        ROUND(AVG(battery_capacity_kwh),1) avg_battery FROM ev_vehicles{w}""",p).fillna(0).iloc[0].to_dict()
    def records(sql):
        return query_df(sql.replace("/*WHERE*/",w),p).to_dict(orient="records")
    result = {
      "kpis": kpis,
      "category_sales": records("SELECT category, SUM(annual_sales) sales FROM ev_vehicles /*WHERE*/ GROUP BY category ORDER BY sales DESC"),
      "manufacturer_sales": records("SELECT manufacturer, SUM(annual_sales) sales FROM ev_vehicles /*WHERE*/ GROUP BY manufacturer ORDER BY sales DESC LIMIT 10"),
      "battery_mix": records("SELECT battery_technology, COUNT(*) models FROM ev_vehicles /*WHERE*/ GROUP BY battery_technology ORDER BY models DESC"),
      "range_category": records("SELECT category, ROUND(AVG(driving_range_km),1) avg_range FROM ev_vehicles /*WHERE*/ GROUP BY category ORDER BY avg_range DESC"),
      "country_production": records("SELECT manufacturing_country, SUM(annual_sales) sales FROM ev_vehicles /*WHERE*/ GROUP BY manufacturing_country ORDER BY sales DESC"),
      "ratings": records("SELECT category, ROUND(AVG(customer_rating),2) rating FROM ev_vehicles /*WHERE*/ GROUP BY category ORDER BY rating DESC"),
      "rows": records("SELECT manufacturer, model, category, year, annual_sales, battery_technology, driving_range_km, manufacturing_country, customer_rating FROM ev_vehicles /*WHERE*/ ORDER BY annual_sales DESC LIMIT 12")
    }
    return jsonify(result)

@app.route("/download")
def download_csv():
    return send_file(CSV_PATH, as_attachment=True, download_name="ev_market_data.csv")

@app.route("/story")
def story():
    return render_template("story.html")

@app.route("/health")
def health():
    return jsonify({"status":"ok","database":str(DB_PATH.name)})

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True, host="127.0.0.1", port=5000)
