# Personal Financial Analytics Dashboard

A modern, high-fidelity personal finance and portfolio tracking dashboard built with **Streamlit**, **Plotly**, and **SQLite**. Designed with a dark-mode mobile-banking aesthetic, fine-grained CSS customizations, and event-driven data caching.

## Visual Previews

### Overview & Key Metrics


*High-level financial KPIs, Recent Transactions feed, Expense Breakdown, and Annual Performance.*

## Key Features

* **Executive KPI Tracking:** Real-time metrics for Gross Profit, Net Profit, Total Costs, and Losses with automated year-over-year (YoY) percentage delta calculations.

* **Unified Transaction Feed:** An aggregated, chronological transaction history unifying Earnings, Costs, and Losses with conditional outflow/inflow indicator styling.

* **Smart Visual Breakdowns:**

  * Interactive Plotly Donut charts with threshold clustering (groups categories $<6\%$ into a dynamic `OTHER` grouping).

  * Empty-state fallbacks for periods with zero outflow to maintain dashboard grid balance.

* **Multipage Navigation & Analytics:**

  * **Dashboard:** Core KPIs, recent cash flows, and performance comparisons.

  * **Costs & Losses:** Granular expense tracking, search filtering, and quick modal additions.

  * **Earnings & Pending Cashflow:** Unsettled sales tracking with a single-click settlement pipeline into realized earnings.

  * **Investments & Portfolio:** Multi-currency tracker with integrated real-time exchange rates via API.

* **Interactive Tools:** Built-in multi-mode ROI & Annualized ROI calculator and quick operational calculators.

* **CSV Data Pipeline:** Download pre-formatted CSV template files and bulk upload entries directly into the SQLite backend.

## Architecture & Tech Stack

* **Frontend & App Framework:** [Streamlit](https://streamlit.io/) with targeted Emotion CSS/HTML injection via `st.markdown`.

* **Data Visualization:** [Plotly](https://plotly.com/python/) (Pie/Donut charts, Area curves, Bar charts).

* **Data Processing:** [Pandas](https://pandas.pydata.org/) for vectorized transformations, date sorting, and data reshaping.

* **Database Backend:** [SQLite](https://sqlite.org/) with raw SQL queries using `UNION ALL` aggregation.

* **Caching Architecture:** Event-driven invalidation using `@st.cache_data` on query layers, instantly invalidated upon create/delete mutations to minimize database I/O while guaranteeing up-to-date UI rendering.

## Project Structure

```
├── assets/                  # Dashboard screenshots and UI assets
│   ├── dashboard_overview_1.png
│   ├── dashboard_overview_2.png
│   ├── expenses_breakdown_1.png
│   ├── expenses_breakdown_2.png
│   ├── earnings_breakdown_1.png
│   ├── earnings_breakdown_2.png
│   ├── earnings_breakdown_3.png
│   └── portfolio_tracking.png
├── database.db              # SQLite persistent storage (auto-initialized)
├── database.py              # Database connection, schemas, cached queries & CRUD logic
├── utils.py                 # Mathematical metrics, percentage calculators & formatters
├── loader.py                # CSV ingest parsing and validation pipeline
├── streamlit_app.py         # Main multipage UI layout, custom CSS, and visual components
└── requirements.txt         # Project dependencies

```

## Getting Started

### 1. Clone the Repository

```
git clone https://github.com/aggelos-12/analytics_app
cd financial-analytics-dashboard

```

### 2. Set Up a Virtual Environment

```
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate

```

### 3. Install Dependencies

```
pip install -r requirements.txt

```

*(Ensure your `requirements.txt` includes: `streamlit`, `pandas`, `plotly`, `requests`)*

### 4. Run the Application

```
streamlit run streamlit_app.py

```

The app will automatically initialize the local `database.db` SQLite database if it does not already exist and open in your default browser at `http://localhost:8501`.

## CSV Template Format

If bulk importing records via the upload interface, files should follow these header specifications:

| Table | Required Columns | 
| ----- | ----- | 
| **Earnings** | `CATEGORY`, `PROFIT`, `DESCRIPTION`, `ROI`, `NOTES`, `DATE` | 
| **Costs** | `DATE`, `COST`, `DESCRIPTION`, `CATEGORY`, `NOTES` | 
| **Losses** | `CATEGORY`, `LOSS`, `DESCRIPTION`, `DATE`, `NOTES` | 
| **Investments** | `DATE`, `ENTRY`, `DESCRIPTION`, `AMOUNT`, `CURRENCY`, `PLATFORM`, `ACCOUNT` | 
| **Pending Earnings** | `CATEGORY`, `PROFIT`, `DESCRIPTION`, `ROI`, `NOTES`, `DATE`, `IMMEDIATE_TRANSFER` | 

Pre-formatted sample templates can be downloaded directly from the sidebar inside the running dashboard.

## License

