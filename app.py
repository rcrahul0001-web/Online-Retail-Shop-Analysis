import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Online Retail Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Base ---- */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0F1117;
    color: #E8EAF0;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

[data-testid="stSidebar"] {
    background-color: #16191F;
    border-right: 1px solid #2A2D35;
}

/* ---- KPI cards ---- */
.kpi-card {
    background: #1C1F28;
    border: 1px solid #2A2D35;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: #4F8EF7; }
.kpi-label {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8B90A0;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: #E8EAF0;
    line-height: 1.1;
}
.kpi-delta {
    font-size: 0.78rem;
    color: #4ECB71;
    margin-top: 4px;
}

/* ---- Section headers ---- */
.section-header {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4F8EF7;
    padding: 18px 0 8px 0;
    border-bottom: 1px solid #2A2D35;
    margin-bottom: 16px;
}

/* ---- Hide Streamlit chrome ---- */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ---- Sidebar filters ---- */
.sidebar-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #E8EAF0;
    margin-bottom: 4px;
}
.sidebar-sub {
    font-size: 0.75rem;
    color: #8B90A0;
    margin-bottom: 18px;
}

/* ---- Divider ---- */
hr { border-color: #2A2D35; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOTLY THEME DEFAULTS
# ─────────────────────────────────────────────
CHART_BG   = "#1C1F28"
PAPER_BG   = "#1C1F28"
FONT_COLOR = "#C8CAD4"
GRID_COLOR = "#2A2D35"
ACCENT     = "#4F8EF7"

def dark_layout(fig, title="", height=380):
    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color=FONT_COLOR, family="Inter"), x=0.02),
        plot_bgcolor=CHART_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR, family="Inter", size=11),
        height=height,
        margin=dict(l=16, r=16, t=44, b=16),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, showgrid=True),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, showgrid=True),
    )
    return fig

# ─────────────────────────────────────────────
# DATA LOADER
# ─────────────────────────────────────────────
@st.cache_data(show_spinner="Loading data…")
def load_data():
    df = pd.read_csv("data/clean/online_retail_cleaned.csv", low_memory=False)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df = df.dropna(subset=["InvoiceDate"])
    df["Revenue"]   = df["Quantity"] * df["Price"]
    df["Year"]      = df["InvoiceDate"].dt.year
    df["Month"]     = df["InvoiceDate"].dt.month
    df["MonthName"] = df["InvoiceDate"].dt.strftime("%b")
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)
    df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()
    return df

df = load_data()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">🛒 Retail Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Online Retail · 2009–2011</div>', unsafe_allow_html=True)
    st.divider()

    all_countries = sorted(df["Country"].unique())
    sel_countries = st.multiselect(
        "Country",
        all_countries,
        default=all_countries,
        placeholder="All countries",
    )

    years = sorted(df["Year"].unique())
    sel_years = st.multiselect(
        "Year",
        years,
        default=years,
        placeholder="All years",
    )

    st.divider()
    top_n = st.slider("Top N (products / customers / countries)", 5, 20, 10)
    st.divider()
    st.caption("Built by **Rahul Chauhan**  \nPython · Pandas · Streamlit · Plotly")

# ─────────────────────────────────────────────
# FILTER
# ─────────────────────────────────────────────
fdf = df.copy()
if sel_countries:
    fdf = fdf[fdf["Country"].isin(sel_countries)]
if sel_years:
    fdf = fdf[fdf["Year"].isin(sel_years)]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("## Online Retail — Business Intelligence Dashboard")
st.caption(f"Showing **{len(fdf):,}** transactions · {len(fdf['Country'].unique())} countries · {fdf['YearMonth'].nunique()} months")

# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
total_rev  = fdf["Revenue"].sum()
total_ord  = fdf["Invoice"].nunique()
total_cust = fdf["Customer ID"].nunique()
total_prod = fdf["Description"].nunique()
aov        = total_rev / total_ord if total_ord else 0

k1, k2, k3, k4, k5 = st.columns(5)
for col, label, value in zip(
    [k1, k2, k3, k4, k5],
    ["Total Revenue", "Orders", "Customers", "Products", "Avg Order Value"],
    [f"£{total_rev:,.0f}", f"{total_ord:,}", f"{total_cust:,}", f"{total_prod:,}", f"£{aov:,.2f}"],
):
    with col:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown("")

# ─────────────────────────────────────────────
# ROW 1 — Revenue trend  |  Country share
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">Revenue Analysis</div>', unsafe_allow_html=True)
c1, c2 = st.columns([3, 2])

with c1:
    monthly = fdf.groupby("YearMonth")["Revenue"].sum().reset_index()
    monthly.columns = ["Month", "Revenue"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Revenue"],
        mode="lines+markers",
        line=dict(color=ACCENT, width=2.5),
        marker=dict(size=5, color=ACCENT),
        fill="tozeroy",
        fillcolor="rgba(79,142,247,0.10)",
        name="Revenue",
    ))
    dark_layout(fig, "Monthly Revenue Trend", height=340)
    fig.update_xaxes(tickangle=-40, tickfont=dict(size=10))
    fig.update_yaxes(tickprefix="£", tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c2:
    ctry_rev = (
        fdf.groupby("Country")["Revenue"].sum()
        .sort_values(ascending=False).head(top_n).reset_index()
    )
    fig2 = px.pie(
        ctry_rev, names="Country", values="Revenue",
        hole=0.52,
        color_discrete_sequence=px.colors.sequential.Blues_r,
    )
    fig2.update_traces(textfont_size=11, textposition="outside")
    dark_layout(fig2, f"Revenue Share — Top {top_n} Countries", height=340)
    fig2.update_layout(
        legend=dict(font=dict(size=10), orientation="v", x=1.02, y=0.5),
        margin=dict(l=0, r=100, t=44, b=0),
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# ROW 2 — Products  |  Customers
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">Products & Customers</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
    top_products = (
        fdf.groupby("Description")["Quantity"].sum()
        .sort_values(ascending=False).head(top_n).reset_index()
    )
    fig3 = px.bar(
        top_products, x="Quantity", y="Description",
        orientation="h",
        color="Quantity",
        color_continuous_scale=[[0, "#1C3A6B"], [1, ACCENT]],
    )
    fig3.update_layout(coloraxis_showscale=False, yaxis=dict(categoryorder="total ascending"))
    dark_layout(fig3, f"Top {top_n} Best-Selling Products", height=420)
    fig3.update_xaxes(tickformat=",.0f")
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

with c4:
    top_customers = (
        fdf.groupby("Customer ID")["Revenue"].sum()
        .sort_values(ascending=False).head(top_n).reset_index()
    )
    top_customers["Customer ID"] = top_customers["Customer ID"].astype(str)
    fig4 = px.bar(
        top_customers, x="Customer ID", y="Revenue",
        color="Revenue",
        color_continuous_scale=[[0, "#2D1B5E"], [1, "#A78BFA"]],
    )
    fig4.update_layout(coloraxis_showscale=False)
    dark_layout(fig4, f"Top {top_n} Customers by Revenue", height=420)
    fig4.update_yaxes(tickprefix="£", tickformat=",.0f")
    fig4.update_xaxes(tickangle=-40)
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# ROW 3 — Country bar  |  Day-of-week heatmap
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">Geographic & Time Patterns</div>', unsafe_allow_html=True)
c5, c6 = st.columns([3, 2])

with c5:
    ctry_bar = (
        fdf.groupby("Country")["Revenue"].sum()
        .sort_values(ascending=False).head(top_n).reset_index()
    )
    fig5 = px.bar(
        ctry_bar, x="Revenue", y="Country",
        orientation="h",
        color="Revenue",
        color_continuous_scale=[[0, "#0A3A2A"], [1, "#4ECB71"]],
    )
    fig5.update_layout(coloraxis_showscale=False, yaxis=dict(categoryorder="total ascending"))
    dark_layout(fig5, f"Top {top_n} Countries by Revenue", height=380)
    fig5.update_xaxes(tickprefix="£", tickformat=",.0f")
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})

with c6:
    DOW_ORDER = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    dow = (
        fdf.groupby("DayOfWeek")["Revenue"].sum()
        .reindex(DOW_ORDER).fillna(0).reset_index()
    )
    fig6 = go.Figure(go.Bar(
        x=dow["Revenue"], y=dow["DayOfWeek"],
        orientation="h",
        marker=dict(
            color=dow["Revenue"],
            colorscale=[[0,"#3B2512"],[1,"#F97316"]],
        ),
    ))
    dark_layout(fig6, "Revenue by Day of Week", height=380)
    fig6.update_xaxes(tickprefix="£", tickformat=",.0f")
    st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# RAW DATA EXPANDER
# ─────────────────────────────────────────────
with st.expander("📋 View Raw Data", expanded=False):
    st.dataframe(
        fdf.reset_index(drop=True),
        use_container_width=True,
        height=380,
    )
    csv = fdf.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️  Download filtered CSV",
        data=csv,
        file_name="online_retail_filtered.csv",
        mime="text/csv",
    )

st.markdown("---")
st.caption("Online Retail Analytics · Built by Rahul Chauhan · Python · Pandas · Plotly · Streamlit")
from matplotlib.gridspec import GridSpec
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv(
    "data/clean/online_retail_cleaned.csv",
    low_memory=False
)

# Convert InvoiceDate to datetime
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    errors="coerce"
)

# Create Revenue column
df["Revenue"] = df["Quantity"] * df["Price"]

# ============================
# KPI Calculations
# ============================

total_revenue = df["Revenue"].sum()

total_orders = df["Invoice"].nunique()

total_customers = df["Customer ID"].nunique()

total_products = df["Description"].nunique()

average_order_value = total_revenue / total_orders


print("="*60)
print("BUSINESS KPIs")
print("="*60)

print(f"Total Revenue      : £{total_revenue:,.2f}")
print(f"Total Orders       : {total_orders:,}")
print(f"Total Customers    : {total_customers:,}")
print(f"Total Products     : {total_products:,}")
print(f"Average Order Value: £{average_order_value:,.2f}")


# ============================
# CREATE DASHBOARD
# ============================

fig = plt.figure(figsize=(18, 10))

gs = GridSpec(
    3, 2,
    figure=fig,
    height_ratios=[1, 3, 3]
)

fig.suptitle(
    "ONLINE RETAIL DASHBOARD",
    fontsize=22,
    fontweight="bold"
)


ax1 = fig.add_subplot(gs[1, 0])
ax2 = fig.add_subplot(gs[1, 1])
ax3 = fig.add_subplot(gs[2, 0])
ax4 = fig.add_subplot(gs[2, 1])



monthly_revenue = (
    df.groupby(df["InvoiceDate"].dt.to_period("M"))["Revenue"]
      .sum()
)

monthly_revenue.index = monthly_revenue.index.astype(str)

ax1.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    color="green",
    marker="o"
)

ax1.set_title("Monthly Revenue")

ax1.set_xlabel("Month")
ax1.set_ylabel("Revenue (£)")

ax1.tick_params(axis="x", rotation=45)

ax1.grid(True)

top_products = (
    df.groupby("Description")["Quantity"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)
ax2.bar(
    top_products.index,
    top_products.values,
    color="steelblue"
)

ax2.set_title("Top 10 Products")

ax2.tick_params(axis="x", rotation=75)

ax2.set_ylabel("Quantity")



# -----------------------------
# Top 10 Countries by Revenue
# -----------------------------

top_countries = (
    df.groupby("Country")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

ax3.barh(
    top_countries.index,
    top_countries.values,
    color="orange"
)

ax3.set_title("Top 10 Countries by Revenue")
ax3.set_xlabel("Revenue (£)")

# -----------------------------
# Top 10 Customers
# -----------------------------

top_customers = (
    df.groupby("Customer ID")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

ax4.bar(
    top_customers.index.astype(str),
    top_customers.values,
    color="purple"
)

ax4.set_title("Top 10 Customers")
ax4.set_xlabel("Customer ID")
ax4.set_ylabel("Revenue (£)")

ax4.tick_params(axis="x", rotation=45)


fig.text(
    0.05, 0.88,
    f"Revenue\n£{total_revenue:,.0f}",
    fontsize=16,
    bbox=dict(facecolor="lightgreen", edgecolor="black")
)

fig.text(
    0.28, 0.88,
    f"Orders\n{total_orders:,}",
    fontsize=16,
    bbox=dict(facecolor="lightblue", edgecolor="black")
)

fig.text(
    0.50, 0.88,
    f"Customers\n{total_customers:,}",
    fontsize=16,
    bbox=dict(facecolor="orange", edgecolor="black")
)

fig.text(
    0.72, 0.88,
    f"Products\n{total_products:,}",
    fontsize=16,
    bbox=dict(facecolor="pink", edgecolor="black")
)


plt.tight_layout()
plt.show()
import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/online_retail_II.csv")

# Remove Unnamed columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Remove duplicates
df = df.drop_duplicates()

# Remove missing descriptions
df = df.dropna(subset=["Description"])

# Keep only valid sales
df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]

# Save cleaned dataset
df.to_csv("data/clean/online_retail_cleaned.csv", index=False)

print("=" * 60)
print("Dataset cleaned successfully!")
print("=" * 60)

print("\nFinal Shape:")
print(df.shape)

print("\nSaved Successfully!")
print("Location: data/clean/online_retail_cleaned.csv")
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv(
    "data/clean/online_retail_cleaned.csv",
    low_memory=False
)

# Convert InvoiceDate to datetime
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    errors="coerce"
)
print("ONLINE RETAIL - EXPLORATORY DATA ANALYSIS")
print("=" * 60)

print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())

# Calculate Revenue
df["Revenue"] = df["Quantity"] * df["Price"]

print("=" * 60)
print("TOTAL REVENUE")
print("=" * 60)

total_revenue = df["Revenue"].sum()

print(f"Total Revenue: £{total_revenue:,.2f}")
# Create Year-Month column
df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

monthly_revenue = (
    df.groupby("YearMonth")["Revenue"]
      .sum()
)

print("=" * 60)
print("MONTHLY REVENUE")
print("=" * 60)
print(monthly_revenue)


plt.figure(figsize=(14,6))

monthly_revenue.plot(
    kind="line",
    marker="o",
    linewidth=2,
    color="green"
)

plt.title("Monthly Revenue Trend", fontsize=16, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Revenue (£)")

plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()

top_country_revenue = (
    df.groupby("Country")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)


print("=" * 60)
print("TOP 10 COUNTRIES REVENUE")
print("=" * 60)

print(top_country_revenue)



plt.figure(figsize=(10,10))

plt.pie(
    top_country_revenue,
    labels=top_country_revenue.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Revenue Share by Top 10 Countries", fontsize=16)

plt.tight_layout()
plt.show()


print("=" * 60)
print("TOP 10 BEST-SELLING PRODUCTS")
print("=" * 60)

top_products = (
    df.groupby("Description")["Quantity"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print(top_products)


plt.figure(figsize=(14,6))

top_products.plot(
    kind="bar",
    color="steelblue",
    edgecolor="black"
)

plt.title("Top 10 Best Selling Products", fontsize=16, fontweight="bold")
plt.xlabel("Products", fontsize=12)
plt.ylabel("Quantity Sold", fontsize=12)

plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()

top_countries = (
    df.groupby("Country")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)


print(top_countries)

print("=" * 60)
print("TOP 10 COUNTRIES BY REVENUE")
print("=" * 60)

top_countries.plot(
    kind="bar",
    figsize=(12,6),
    color="orange",
    edgecolor="black"
)

plt.title("Top 10 Countries by Revenue", fontsize=16)
plt.xlabel("Country")
plt.ylabel("Revenue (£)")


top_customers = (
    df.groupby("Customer ID")["Revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print("=" * 60)
print("TOP 10 CUSTOMERS")
print("=" * 60)
print(top_customers)

plt.figure(figsize=(12,6))

top_customers.plot(
    kind="bar",
    color="purple",
    edgecolor="black"
)

plt.title("Top 10 Customers by Revenue", fontsize=16)
plt.xlabel("Customer ID")
plt.ylabel("Revenue (£)")

plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()

plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()
