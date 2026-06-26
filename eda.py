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