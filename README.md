# RetailPulse — E-Commerce Customer & Sales Analytics

An interactive retail analytics project built using Python, Streamlit, Pandas, Plotly, SQL, and Power BI. RetailPulse explores sales performance, customer purchasing behaviour, product performance, and country-level revenue to generate actionable business insights.

## Project Overview

RetailPulse transforms raw retail transaction data into meaningful business insights through data cleaning, exploratory data analysis, SQL queries, and interactive dashboards.

The project combines a Streamlit analytics application with Power BI dashboards to explore sales trends, customer behaviour, product performance, and transaction patterns.

## Features

- **Executive Overview:** Sales KPIs, revenue trends, and overall business performance.
- **Customer Analytics:** Customer purchasing behaviour, repeat purchases, and top customers.
- **Product Analysis:** Product performance by revenue and units sold.
- **Country Analysis:** Country-level revenue comparisons and transaction analysis.
- **Interactive Filters:** Explore data using available date and country filters.
- **Data Preparation:** Data cleaning, duplicate removal, and investigation of missing and unusual transaction values.
- **SQL Analytics:** Queries for sales aggregation, product analysis, and country-level performance.
- **Power BI Dashboards:** Interactive business intelligence reports for visual exploration of key metrics.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and analysis |
| Pandas & NumPy | Data cleaning and manipulation |
| Plotly | Interactive visualizations |
| Streamlit | Interactive analytics application |
| SQL | Business queries and data aggregation |
| Power BI | Business intelligence dashboards |
| Jupyter Notebook | Data cleaning and exploratory analysis |
| Git & GitHub | Version control and project hosting |

## Project Structure

```text
RetailPulse/
├── app.py
├── README.md
├── requirements.txt
├── data/
│   └── Local datasets (not committed)
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   └── 02_exploratory_data_analysis.ipynb
├── sql/
│   └── SQL analytics queries
├── reports/
│   └── Project report
└── screenshots/
    └── Dashboard screenshots
```

*The structure above describes the intended organization. Adjust filenames to match the actual repository.*

## Key Business Insights

- **Monthly sales trends:** November 2011 recorded the highest monthly revenue in the analysis, at approximately 1.50 million in dataset currency.
- **Lower-revenue period:** February 2011 recorded approximately 522.5 thousand in revenue.
- **Customer data quality:** Missing customer IDs limit the completeness of customer-level analysis.
- **Product performance:** Product-level revenue and quantity analysis helps identify important items and purchasing patterns.
- **Transaction quality:** Cancellations, negative quantities, and unusual transaction values require appropriate filtering and interpretation.

*Revenue figures depend on the project's transaction filters and cleaning methodology. They should not be treated as audited accounting figures.*

## Dashboard Previews

### Streamlit Application

The Streamlit application provides interactive exploration of retail sales, customer purchasing behaviour, product performance, and country-level metrics.



## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/priyanka-sapkal101/ecommerce-customer-sales-analytics.git
cd ecommerce-customer-sales-analytics
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare the dataset

Download or obtain the Online Retail II dataset from its original source. Place the required cleaned CSV at:

```text
data/retail_cleaned_for_sql.csv
```

The dataset is not included in the public repository because of its size. The cleaning notebooks can help you understand the preparation workflow.

### 4. Launch the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to use the dashboard.

## Dataset and Limitations

The project uses the Online Retail II dataset, which contains retail transaction information such as invoices, products, quantities, prices, customer IDs, and countries.

Important considerations:

- Some transactions have missing customer IDs.
- Cancelled invoices and negative quantities need careful treatment.
- Zero or negative prices may represent data-quality issues or special transaction adjustments.
- Customer-level metrics may exclude transactions without customer identifiers.
- Revenue results depend on the selected cleaning rules and sales filters.

## Future Improvements

- Customer segmentation using RFM analysis.
- Sales forecasting and trend prediction.
- Automated data refresh and reporting.
- Customer retention and cohort analysis.
- Deployment of the Streamlit application.

## Author

**Priyanka Sapkal**

Computer Engineering Graduate | Aspiring Data Analyst

