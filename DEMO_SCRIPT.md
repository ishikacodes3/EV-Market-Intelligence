# 3–4 minute project demonstration script

1. **Introduction (20 sec):** “This is an EV Market Intelligence Dashboard designed to explore sales, manufacturers, battery technologies, driving range, geography and customer ratings.”
2. **Data and database (40 sec):** Show `data/ev_market_data.csv`, explain its fields, then show that Flask creates a SQLite database on first run. Clearly disclose that the included dataset is synthetic demo data.
3. **Dashboard (90 sec):** Show KPI cards. Change year, category and manufacturer filters. Explain that charts and KPIs refresh from SQL queries.
4. **Visuals and story (45 sec):** Briefly explain category sales, manufacturer performance, battery mix, range, country distribution and ratings. Open Market Story and walk through its five scenes.
5. **SQL / Tableau (35 sec):** Open `sql_queries.sql`. Explain that the CSV is Tableau-ready and can be connected through Tableau’s Text File connector.
6. **Conclusion (15 sec):** “The project demonstrates an end-to-end analytics workflow using CSV, Python, SQLite, SQL, Flask and Plotly. For production conclusions, the sample data must be replaced with a verified market dataset.”
