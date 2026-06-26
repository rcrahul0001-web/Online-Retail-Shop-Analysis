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