# EV Market Intelligence Dashboard

A ready-to-run Flask + SQLite + Plotly analytics project for an Electric Vehicle market dataset.

## Important data note
The included 650-row CSV is **synthetic demonstration data** created to make the project runnable immediately. It is not verified real-world EV market data. Do not describe its numbers as actual market share or real global sales. Replace `data/ev_market_data.csv` with a verified dataset using the same column names for a real market analysis.

## Features
- CSV data collection / extraction and SQLite database loading
- SQL aggregation queries and indexes
- Interactive dashboard with Year, Category and Manufacturer filters
- Five KPI cards and six unique chart types/visuals plus a data table
- Five-scene market story page
- Responsive layout for desktop, tablet and mobile
- CSV download endpoint and health-check endpoint
- Tableau-ready CSV and SQLite database

## Run in VS Code (Windows)
1. Extract the ZIP and open the `ev_market_intelligence` folder in VS Code.
2. Open Terminal (`Terminal > New Terminal`).
3. Create and activate a virtual environment (recommended):
   ```powershell
   py -m venv .venv
   .venv\\Scripts\\activate
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Start the app:
   ```powershell
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser. The SQLite database is created automatically on first run.

If `py` is unavailable, use `python` instead. If the database needs rebuilding after replacing the CSV, stop the app, delete `data/ev_market.db`, and run `python app.py` again.

## Project structure
```
ev_market_intelligence/
├── app.py
├── requirements.txt
├── sql_queries.sql
├── README.md
├── data/
│   └── ev_market_data.csv
├── templates/
│   ├── index.html
│   └── story.html
└── static/
    └── style.css
```

## Data dictionary
- `vehicle_id`: unique record key
- `manufacturer`, `model`, `category`, `year`: vehicle/product dimensions
- `annual_sales`: represented annual sales units
- `battery_technology`, `battery_capacity_kwh`: battery attributes
- `driving_range_km`: estimated range in kilometres
- `price_usd`: listed price in USD
- `manufacturing_country`: country dimension
- `customer_rating`: rating on a 1–5 scale
- `fast_charge_minutes`: illustrative fast-charge duration

## Tableau connection
The CSV is the easiest Tableau input: open Tableau Desktop/Public → Connect → Text file → select `data/ev_market_data.csv`. You can also connect to SQLite using an appropriate SQLite connector/driver if installed. Create worksheets for category sales, manufacturer sales, battery mix, range by category, country sales and customer ratings, then assemble a dashboard and story. The Flask dashboard is a web alternative; it is not an embedded Tableau workbook. Tableau workbook publishing/embedding requires a Tableau account/server and its own authentication/configuration.

## Mapping to the project brief
| Requirement | Implemented evidence |
|---|---|
| Problem understanding | EV market problem framing in this README and story |
| Data collection | Included CSV; replace with verified source data |
| Store data in DB | SQLite `data/ev_market.db`, auto-created |
| SQL operations | `sql_queries.sql`, dashboard SQL aggregations |
| Connect DB with Tableau | Tableau connection steps above; CSV ready |
| Data preparation | pandas ingestion, numeric aggregation, missing-safe KPI display |
| Visualizations | 6 interactive Plotly charts + detail table |
| Dashboard design | Responsive dark executive dashboard |
| Story | 5 narrative scenes in `/story` |
| Performance | SQLite indexes on year and manufacturer; aggregate queries |
| Filters | Year, category, manufacturer |
| Calculated fields | KPI aggregates and SQL market-share calculation |
| Web integration | Flask routes and responsive UI |
| Documentation | This README |

## Suggested demonstration
1. Explain the business problem and the three stakeholder personas.
2. Show the CSV columns and explain synthetic-data limitation.
3. Run the Flask app and show the SQLite database auto-creation.
4. Change each dashboard filter and explain how KPIs/charts update.
5. Walk through the five story scenes.
6. Open `sql_queries.sql` and explain market share and category aggregation.
7. Show how the CSV can be opened in Tableau.

## GitHub upload
Create a new empty GitHub repository. In the VS Code terminal from this folder:
```bash
git init
git add .
git commit -m "Build EV market intelligence dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```
Do not upload `.venv/`. A `.gitignore` is included.
