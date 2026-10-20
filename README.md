
# RetailPulse — E-Commerce Customer & Sales Analytics

An interactive analytics dashboard built with Python, Streamlit, Pandas, and Plotly to explore retail sales performance, customer purchasing behaviour, product performance, and country-level revenue.

## Features

- Executive overview with sales KPIs and monthly revenue trends
- Customer analytics, repeat purchases, and top customers
- Product performance by revenue and units sold
- Country revenue and transaction analysis
- Interactive date and country filters

## Technology Stack

- Python
- Pandas
- Plotly
- Streamlit
- SQL
- Jupyter Notebook

## Project Structure

- `app.py` — Streamlit dashboard
- `data/` — Local dataset (not included in the public repository)
- `notebooks/` — Data cleaning and exploratory analysis
- `sql/` — SQL analytics queries
- `reports/` — Project report
- `screenshots/` — Dashboard screenshots
- `requirements.txt` — Python dependencies

## Run Locally

1. Clone this repository.
2. Install the dependencies:
   `pip install -r requirements.txt`
3. Place the cleaned CSV at `data/retail_cleaned_for_sql.csv`.
4. Run the dashboard:
   `streamlit run app.py`

## Dataset and Limitations

The project uses the Online Retail II dataset. Customer IDs are missing for some transactions, and unusual quantities and transaction adjustments require careful interpretation. Revenue metrics are based on the project's defined sales filters and should not automatically be interpreted as audited accounting revenue.

## Author

Add your name and GitHub profile link here.
