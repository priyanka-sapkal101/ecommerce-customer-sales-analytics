from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="RetailPulse | E-Commerce Analytics", page_icon="📊", layout="wide")

BASE = Path(__file__).resolve().parent
CSV = BASE / "data" / "retail_cleaned_for_sql.csv"

# Premium palette: navy, teal, gold, indigo, and warm neutrals
NAVY = "#14243A"
NAVY2 = "#203852"
TEAL = "#147D70"
GOLD = "#D6AD60"
BLUE = "#477DA8"
PURPLE = "#7663A8"
CORAL = "#D97868"
INK = "#243447"
MUTED = "#6B7A8C"
BG = "#F4F7FB"
BORDER = "#E3E9F0"
WHITE = "#FFFFFF"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html, body, [class*="css"] {{font-family:'DM Sans',sans-serif;}}
.stApp {{background:{BG}; color:{INK};}}
[data-testid="stHeader"] {{background:rgba(244,247,251,.95);}}
/* Remove Streamlit's oversized top padding so the page starts near the top. */
[data-testid="stAppViewContainer"] .main .block-container {{padding-top:1.35rem !important;padding-bottom:2rem !important;max-width:1600px;}}
[data-testid="stSidebar"] {{background:linear-gradient(180deg,{NAVY} 0%,#1C3048 100%);border-right:1px solid #263D56;}}
[data-testid="stSidebar"] > div:first-child {{padding-top:1.1rem !important;}}
[data-testid="stSidebar"] * {{color:#F4F7FB;}}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{color:#C5D1DE;}}
[data-testid="stSidebar"] label {{color:#EAF0F6 !important;}}
/* Sidebar navigation buttons */
[data-testid="stSidebar"] .stButton > button {{
  width:100%;text-align:left;justify-content:flex-start;min-height:2.7rem;
  border:1px solid rgba(225,235,246,.13);border-radius:11px;
  background:rgba(255,255,255,.055);color:#EAF0F6;font-weight:600;
  padding:.62rem .85rem;transition:all .16s ease;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
  border-color:#67C7B8;background:rgba(20,125,112,.25);color:#FFFFFF;
}}
[data-testid="stSidebar"] .stButton > button:focus:not(:active) {{
  border-color:#67C7B8;color:#FFFFFF;box-shadow:0 0 0 2px rgba(103,199,184,.22);
}}
h1,h2,h3 {{font-family:'Manrope',sans-serif !important;color:{NAVY} !important;letter-spacing:-.025em;}}
h1 {{font-size:2rem !important;font-weight:800 !important;}}
h2 {{font-size:1.24rem !important;font-weight:700 !important;}}
[data-testid="stMetric"] {{background:{WHITE};border:1px solid {BORDER};border-radius:15px;padding:17px 18px;box-shadow:0 4px 15px rgba(20,36,58,.035);min-height:112px;}}
[data-testid="stMetricLabel"] {{color:{MUTED};font-size:.82rem;font-weight:600;}}
[data-testid="stMetricValue"] {{color:{NAVY};font-family:'Manrope',sans-serif;font-weight:800;font-size:1.65rem;}}
div[data-testid="stPlotlyChart"] {{background:{WHITE};border:1px solid {BORDER};border-radius:15px;padding:7px;box-shadow:0 4px 15px rgba(20,36,58,.025);}}
.brand-mark {{display:inline-flex;align-items:center;justify-content:center;width:42px;height:42px;border-radius:13px;background:linear-gradient(135deg,#1A9A87,{GOLD});font-size:22px;margin-bottom:10px;}}
.brand-name {{color:#fff;font-family:'Manrope',sans-serif;font-weight:800;font-size:1.42rem;}}
.brand-sub {{color:#B8C8D8;font-size:.77rem;margin-top:3px;}}
.eyebrow {{text-transform:uppercase;letter-spacing:.13em;color:{TEAL};font-size:.72rem;font-weight:800;margin-bottom:5px;}}
.subtitle {{color:{MUTED};margin-top:-8px;margin-bottom:18px;font-size:.94rem;}}
.kicker {{color:{MUTED};font-size:.79rem;margin-top:-7px;margin-bottom:12px;}}
.footer {{color:{MUTED};font-size:.75rem;border-top:1px solid {BORDER};padding-top:15px;margin-top:25px;}}
@media(max-width:768px) {{h1{{font-size:1.55rem !important;}}[data-testid="stMetric"]{{padding:12px;min-height:96px;}}[data-testid="stMetricValue"]{{font-size:1.2rem;}}}}
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner="Loading and preparing retail data…")
def load_data(path):
    d = pd.read_csv(path, low_memory=False)
    required = ["Invoice", "Quantity", "InvoiceDate", "Price", "Customer ID", "Country"]
    missing = [c for c in required if c not in d.columns]
    if missing:
        raise ValueError("CSV is missing required columns: " + ", ".join(missing))
    d["InvoiceDate"] = pd.to_datetime(d["InvoiceDate"], errors="coerce")
    for c in ["Quantity", "Price", "Customer ID"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["Invoice"] = d["Invoice"].astype("string")
    d["Country"] = d["Country"].fillna("Unknown").astype(str)
    d["Description"] = d["Description"].fillna("Unknown").astype(str) if "Description" in d else "Unknown"
    d["Revenue"] = d["Quantity"] * d["Price"]
    d["IsCancellation"] = d["Invoice"].str.startswith("C", na=False)
    if "TransactionType" not in d:
        d["TransactionType"] = "Regular Transaction"
        d.loc[d["Price"].lt(0), "TransactionType"] = "Bad Debt Adjustment"
        d.loc[d["Invoice"].str.startswith("C", na=False), "TransactionType"] = "Cancellation Invoice"
        d.loc[d["Quantity"].lt(0), "TransactionType"] = "Negative Quantity"
        d.loc[d["Price"].eq(0), "TransactionType"] = "Zero Price"
    return d


if not CSV.exists():
    st.error("CSV not found. Place the cleaned file at data/retail_cleaned_for_sql.csv.")
    st.stop()
try:
    raw = load_data(str(CSV))
except Exception as e:
    st.error(f"Could not load the CSV: {e}")
    st.stop()

# Consistent qualifying-sales definition
sales_all = raw[
    raw["Quantity"].gt(0) & raw["Price"].gt(0)
    & ~raw["IsCancellation"] & raw["InvoiceDate"].notna()
].copy()
if sales_all.empty:
    st.error("No qualifying sales rows were found.")
    st.stop()

min_date, max_date = sales_all["InvoiceDate"].min().date(), sales_all["InvoiceDate"].max().date()

PAGES = [
    ("Executive Overview", "▦", "Overview"),
    ("Customer Analytics", "◉", "Customers"),
    ("Product Analytics", "◇", "Products"),
    ("Country & Transactions", "◎", "Markets & Transactions"),
]
if "retailpulse_page" not in st.session_state:
    st.session_state.retailpulse_page = "Executive Overview"

with st.sidebar:
    st.markdown('<div class="brand-mark">↗</div><div class="brand-name">RetailPulse</div><div class="brand-sub">E-Commerce Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:1px;background:rgba(255,255,255,.12);margin:1.25rem 0 1.1rem"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.72rem;font-weight:800;letter-spacing:.12em;color:#91A6BC;margin-bottom:.65rem">WORKSPACE</div>', unsafe_allow_html=True)
    for page_name, page_icon, short_name in PAGES:
        active = st.session_state.retailpulse_page == page_name
        label = f"{page_icon}   {page_name}"
        if st.button(label, key=f"nav_{short_name}", use_container_width=True, type="primary" if active else "secondary"):
            st.session_state.retailpulse_page = page_name
            st.rerun()
    page = st.session_state.retailpulse_page
    st.markdown('<div style="height:1px;background:rgba(255,255,255,.12);margin:1.25rem 0 1.1rem"></div>', unsafe_allow_html=True)
    st.markdown("### Global filters")
    date_range = st.date_input("Invoice date", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    country_options = sorted(sales_all["Country"].dropna().unique().tolist())
    selected_countries = st.multiselect("Country", country_options, placeholder="All countries")
    product_options = sorted(sales_all["Description"].dropna().unique().tolist())
    selected_products = st.multiselect("Product", product_options, placeholder="All products")
    st.divider()
    st.caption("Source: Online Retail II transaction data")
    st.caption("Revenue includes qualifying positive-quantity, positive-price sales.")

df = sales_all.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    df = df[df["InvoiceDate"].dt.date.between(date_range[0], date_range[1])]
if selected_countries:
    df = df[df["Country"].isin(selected_countries)]
if selected_products:
    df = df[df["Description"].isin(selected_products)]
if df.empty:
    st.warning("No sales match the current filters. Adjust your selections.")
    st.stop()

revenue = float(df["Revenue"].sum())
orders = int(df["Invoice"].nunique())
aov = revenue / orders if orders else 0
customers = int(df["Customer ID"].dropna().nunique())
units = int(df["Quantity"].sum())


def compact(n):
    if abs(n) >= 1_000_000:
        return f"{n / 1_000_000:,.2f}M"
    if abs(n) >= 1_000:
        return f"{n / 1_000:,.2f}K"
    return f"{n:,.0f}"


def header(title, subtitle, eyebrow):
    st.markdown(f'<div class="eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<div class="subtitle">{subtitle}</div>', unsafe_allow_html=True)


def kpis(items):
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        col.metric(label, value)


def style(fig, height=360):
    fig.update_layout(
        template="plotly_white", height=height,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FFFFFF",
        font=dict(family="DM Sans, sans-serif", color=INK, size=12),
        title=dict(font=dict(family="Manrope, sans-serif", size=15, color=NAVY)),
        margin=dict(l=16, r=18, t=28, b=20),
        hoverlabel=dict(bgcolor=NAVY, font_color="#FFFFFF"),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E9EEF4", zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


def bar_chart(data, x, y, color, horizontal=False, height=360, labels=None):
    fig = px.bar(
        data, x=x, y=y, orientation="h" if horizontal else "v",
        color_discrete_sequence=[color], text_auto=".3s",
        labels=labels or {},
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    style(fig, height)
    fig.update_layout(margin=dict(l=12, r=45, t=25, b=24))
    return fig


# ------------------ EXECUTIVE OVERVIEW ------------------
if page == "Executive Overview":
    header("Executive Overview", "A consolidated view of sales performance, order value and market contribution.", "BUSINESS PERFORMANCE")
    kpis([("Total Revenue", compact(revenue)), ("Total Orders", f"{orders:,}"), ("Average Order Value", f"{aov:,.2f}"), ("Identified Customers", f"{customers:,}")])

    monthly = df.assign(Month=df["InvoiceDate"].dt.to_period("M").dt.to_timestamp()).groupby("Month", as_index=False).agg(Revenue=("Revenue", "sum")).sort_values("Month")
    countries = df.groupby("Country", as_index=False).agg(Revenue=("Revenue", "sum")).nlargest(10, "Revenue").sort_values("Revenue")
    left, right = st.columns([1.55, 1], gap="large")
    with left:
        st.subheader("Monthly Revenue Trend")
        st.markdown('<div class="kicker">Qualifying sales by month</div>', unsafe_allow_html=True)
        fig = px.line(monthly, x="Month", y="Revenue", markers=True, color_discrete_sequence=[TEAL])
        fig.update_traces(line=dict(width=3), marker=dict(size=6))
        fig.update_xaxes(tickformat="%b\n%Y")
        st.plotly_chart(style(fig, 365), use_container_width=True)
    with right:
        st.subheader("Top 10 Countries by Revenue")
        st.markdown('<div class="kicker">Ranked by sales revenue</div>', unsafe_allow_html=True)
        st.plotly_chart(bar_chart(countries, "Revenue", "Country", TEAL, True, 365), use_container_width=True)

    st.subheader("Top 10 Products by Revenue")
    top = df.groupby("Description", as_index=False).agg(Revenue=("Revenue", "sum")).nlargest(10, "Revenue").sort_values("Revenue")
    st.plotly_chart(bar_chart(top, "Revenue", "Description", TEAL, True, 390), use_container_width=True)

# ------------------ CUSTOMER ANALYTICS ------------------
elif page == "Customer Analytics":
    header("Customer Analytics", "Explore repeat purchasing, customer concentration and buying frequency.", "CUSTOMER INTELLIGENCE")
    cs = df.dropna(subset=["Customer ID"]).copy()
    cust_orders = cs.groupby("Customer ID")["Invoice"].nunique()
    cust_count = int(cust_orders.index.nunique())
    repeat_count = int(cust_orders.ge(2).sum())
    repeat_rate = repeat_count / cust_count * 100 if cust_count else 0
    high_value = int(cs.groupby("Customer ID")["Revenue"].sum().ge(2000).sum())
    kpis([("Repeat Customer Rate", f"{repeat_rate:.2f}%"), ("Repeat Customers", f"{repeat_count:,}"), ("Identified Customers", f"{cust_count:,}"), ("High-Value Customers", f"{high_value:,}")])

    freq = cust_orders.reset_index(name="Orders")
    freq["Purchase Frequency"] = pd.cut(freq["Orders"], bins=[0, 1, 5, 10, float("inf")], labels=["1 invoice", "2–5 invoices", "6–10 invoices", "More than 10"], include_lowest=True)
    order = ["1 invoice", "2–5 invoices", "6–10 invoices", "More than 10"]
    freq_summary = freq.groupby("Purchase Frequency", observed=False).size().reindex(order, fill_value=0).rename("Customers").reset_index()
    top_cust = cs.groupby("Customer ID", as_index=False).agg(Revenue=("Revenue", "sum"), Orders=("Invoice", "nunique")).nlargest(10, "Revenue").sort_values("Revenue")
    top_cust["Customer ID"] = top_cust["Customer ID"].map(lambda v: str(int(v)) if float(v).is_integer() else str(v))

    left, right = st.columns(2, gap="large")
    with left:
        st.subheader("Customers by Purchase Frequency")
        fig = px.bar(freq_summary, x="Purchase Frequency", y="Customers", text="Customers", color_discrete_sequence=[NAVY2])
        fig.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(style(fig, 365), use_container_width=True)
    with right:
        st.subheader("Top 10 Customers by Revenue")
        fig = px.bar(top_cust, x="Revenue", y="Customer ID", orientation="h", text_auto=".3s", color_discrete_sequence=[GOLD])
        fig.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(style(fig, 365), use_container_width=True)

    st.subheader("Customer Revenue Detail")
    customer_table = cs.groupby("Customer ID", as_index=False).agg(Revenue=("Revenue", "sum"), Orders=("Invoice", "nunique"), Units=("Quantity", "sum")).sort_values("Revenue", ascending=False).head(20)
    customer_table["Customer ID"] = customer_table["Customer ID"].map(lambda v: str(int(v)) if float(v).is_integer() else str(v))
    st.dataframe(customer_table, hide_index=True, use_container_width=True)

# ------------------ PRODUCT ANALYTICS ------------------
elif page == "Product Analytics":
    header("Product Analytics", "Compare product revenue, sales volume and product-level performance.", "PRODUCT PERFORMANCE")
    prod = df.groupby("Description", as_index=False).agg(Revenue=("Revenue", "sum"), Units_Sold=("Quantity", "sum"), Orders=("Invoice", "nunique"))
    kpis([("Qualifying Revenue", compact(revenue)), ("Units Sold", f"{units:,}"), ("Products", f"{prod['Description'].nunique():,}"), ("Orders", f"{orders:,}")])

    left, right = st.columns(2, gap="large")
    with left:
        st.subheader("Top Products by Revenue")
        d = prod.nlargest(10, "Revenue").sort_values("Revenue")
        st.plotly_chart(bar_chart(d, "Revenue", "Description", TEAL, True, 410), use_container_width=True)
    with right:
        st.subheader("Top Products by Units Sold")
        d = prod.nlargest(10, "Units_Sold").sort_values("Units_Sold")
        st.plotly_chart(bar_chart(d, "Units_Sold", "Description", BLUE, True, 410), use_container_width=True)

    st.subheader("Product Performance: Units Sold vs Revenue")
    st.markdown('<div class="kicker">Each point represents a product. Hover for product details.</div>', unsafe_allow_html=True)
    scatter = prod.nlargest(400, "Revenue")
    fig = px.scatter(scatter, x="Units_Sold", y="Revenue", size="Orders", color="Revenue",
                     color_continuous_scale=["#D9F0E7", TEAL, NAVY], hover_name="Description",
                     hover_data={"Units_Sold": ":,", "Revenue": ":,.2f", "Orders": True})
    fig.update_layout(coloraxis_colorbar_title="Revenue")
    st.plotly_chart(style(fig, 450), use_container_width=True)

    st.subheader("Product Performance Table")
    st.dataframe(prod.sort_values("Revenue", ascending=False).head(25), hide_index=True, use_container_width=True)

# ------------------ COUNTRY & TRANSACTIONS ------------------
elif page == "Country & Transactions":
    header("Country & Transactions", "Explore geographic revenue concentration and transaction patterns.", "MARKET & TRANSACTION INTELLIGENCE")
    country_summary = df.groupby("Country", as_index=False).agg(Revenue=("Revenue", "sum"), Orders=("Invoice", "nunique"), Units=("Quantity", "sum"))
    country_count = int(country_summary["Country"].nunique())
    uk_rev = float(country_summary.loc[country_summary["Country"].eq("United Kingdom"), "Revenue"].sum())
    uk_share = uk_rev / revenue * 100 if revenue else 0

    cancels = raw[raw["IsCancellation"] & raw["InvoiceDate"].notna()].copy()
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        cancels = cancels[cancels["InvoiceDate"].dt.date.between(date_range[0], date_range[1])]
    if selected_countries:
        cancels = cancels[cancels["Country"].isin(selected_countries)]
    cancel_count = int(cancels["Invoice"].nunique())

    kpis([("UK Revenue", compact(uk_rev),), ("UK Revenue Share", f"{uk_share:.2f}%"), ("Cancellation Invoices", f"{cancel_count:,}"), ("Countries", f"{country_count:,}")])
    left, right = st.columns(2, gap="large")
    with left:
        st.subheader("Top 10 Countries by Revenue")
        d = country_summary.nlargest(10, "Revenue").sort_values("Revenue")
        st.plotly_chart(bar_chart(d, "Revenue", "Country", PURPLE, True, 380), use_container_width=True)
    with right:
        st.subheader("Revenue Share — Top 5 Countries")
        d = country_summary.nlargest(5, "Revenue")
        fig = px.pie(d, names="Country", values="Revenue", hole=.58, color_discrete_sequence=[PURPLE, TEAL, GOLD, BLUE, CORAL])
        fig.update_traces(textposition="outside", textinfo="label+percent", hovertemplate="%{label}<br>Revenue: %{value:,.2f}<br>Share: %{percent}<extra></extra>")
        st.plotly_chart(style(fig, 380), use_container_width=True)

    st.subheader("Monthly Cancellation Invoice Trend")
    if not cancels.empty:
        cm = cancels.assign(Month=cancels["InvoiceDate"].dt.to_period("M").dt.to_timestamp()).groupby("Month", as_index=False).agg(Cancellation_Invoices=("Invoice", "nunique")).sort_values("Month")
        fig = px.line(cm, x="Month", y="Cancellation_Invoices", markers=True, color_discrete_sequence=[CORAL])
        fig.update_traces(line=dict(width=3), marker=dict(size=6))
        fig.update_xaxes(tickformat="%b\n%Y")
        st.plotly_chart(style(fig, 330), use_container_width=True)
    else:
        st.info("No cancellation invoices match the selected filters.")

    st.subheader("Transaction Type Breakdown")
    tx = raw["TransactionType"].fillna("Unknown").value_counts().rename_axis("Transaction Type").reset_index(name="Records")
    tx = tx.sort_values("Records")
    fig = px.bar(tx, x="Records", y="Transaction Type", orientation="h", text="Records", color_discrete_sequence=[NAVY2])
    fig.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(style(fig, 340), use_container_width=True)

    st.subheader("Country Performance Detail")
    st.dataframe(country_summary.sort_values("Revenue", ascending=False), hide_index=True, use_container_width=True)

st.markdown(f"""
<div class="footer">
<strong>RetailPulse</strong> · E-Commerce Customer & Sales Analytics<br>

</div>
""", unsafe_allow_html=True)
