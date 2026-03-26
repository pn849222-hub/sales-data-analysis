# Sales Data Analysis - Superstore Dataset
# Author: [Your Name]

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Config
DATA_PATH = "data/superstore.csv"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data
df = pd.read_csv(DATA_PATH, encoding="latin-1")

print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nMissing values:")
print(df.isnull().sum())
print("\nFirst 5 rows:")
print(df.head())
# ── 2. DATA CLEANING ─────────────────────────────────────

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"]  = pd.to_datetime(df["Ship Date"])

# Add useful columns
df["Year"]          = df["Order Date"].dt.year
df["Month"]         = df["Order Date"].dt.month
df["Ship Duration"] = (df["Ship Date"] - df["Order Date"]).dt.days

# Clean column names (remove spaces)
df.columns = df.columns.str.strip().str.replace(" ", "_")

print("\n── After Cleaning ──")
print("Date range:", df["Order_Date"].min().date(), "→", df["Order_Date"].max().date())
print("Years in data:", sorted(df["Year"].unique()))
print("Categories:", df["Category"].unique())
print("Regions:", df["Region"].unique())
print("Avg ship duration:", round(df["Ship_Duration"].mean(), 1), "days")
# ── 3. VISUALIZATION ─────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Superstore Sales Analysis", fontsize=16, fontweight="bold")

# Chart 1: Monthly Sales Trend
monthly = df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"].sum()
monthly.index = monthly.index.astype(str)
axes[0, 0].plot(monthly.index[::3], monthly.values[::3], marker="o", color="#2196F3")
axes[0, 0].set_title("Monthly Sales Trend")
axes[0, 0].set_xlabel("Month")
axes[0, 0].set_ylabel("Sales ($)")
axes[0, 0].tick_params(axis="x", rotation=45)

# Chart 2: Sales by Category
cat_sales = df.groupby("Category")["Sales"].sum().sort_values()
axes[0, 1].barh(cat_sales.index, cat_sales.values, color=["#FF9800", "#4CAF50", "#2196F3"])
axes[0, 1].set_title("Sales by Category")
axes[0, 1].set_xlabel("Total Sales ($)")

# Chart 3: Profit by Region
region_profit = df.groupby("Region")["Profit"].sum().sort_values()
colors = ["#f44336" if x < 0 else "#4CAF50" for x in region_profit.values]
axes[1, 0].bar(region_profit.index, region_profit.values, color=colors)
axes[1, 0].set_title("Profit by Region")
axes[1, 0].set_ylabel("Total Profit ($)")

# Chart 4: Sales by Segment
seg_sales = df.groupby("Segment")["Sales"].sum()
axes[1, 1].pie(seg_sales.values, labels=seg_sales.index,
               autopct="%1.1f%%", colors=["#2196F3", "#FF9800", "#4CAF50"])
axes[1, 1].set_title("Sales by Segment")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/sales_overview.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nChart saved to outputs/sales_overview.png ✓")
# ── 4. DEEPER ANALYSIS ───────────────────────────────────

# Chart 5: Top 10 Products by Sales
top10 = df.groupby("Product_Name")["Sales"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
plt.barh(top10.index, top10.values, color="#2196F3")
plt.title("Top 10 Products by Sales", fontsize=14, fontweight="bold")
plt.xlabel("Total Sales ($)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/top10_products.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart saved: top10_products.png ✓")

# Chart 6: Discount vs Profit scatter
plt.figure(figsize=(10, 6))
colors = df["Category"].map({"Furniture": "#FF9800", 
                              "Office Supplies": "#4CAF50", 
                              "Technology": "#2196F3"})
plt.scatter(df["Discount"], df["Profit"], alpha=0.4, c=colors, s=20)
plt.axhline(y=0, color="red", linestyle="--", linewidth=1)
plt.title("Discount vs Profit (by Category)", fontsize=14, fontweight="bold")
plt.xlabel("Discount")
plt.ylabel("Profit ($)")
from matplotlib.patches import Patch
legend = [Patch(color="#FF9800", label="Furniture"),
          Patch(color="#4CAF50", label="Office Supplies"),
          Patch(color="#2196F3", label="Technology")]
plt.legend(handles=legend)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/discount_vs_profit.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart saved: discount_vs_profit.png ✓")

# Chart 7: Yearly Sales Growth
yearly = df.groupby("Year")["Sales"].sum()
plt.figure(figsize=(8, 5))
bars = plt.bar(yearly.index.astype(str), yearly.values, color="#4CAF50", width=0.5)
for bar, val in zip(bars, yearly.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
             f"${val:,.0f}", ha="center", fontsize=10)
plt.title("Yearly Sales Growth", fontsize=14, fontweight="bold")
plt.xlabel("Year")
plt.ylabel("Total Sales ($)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/yearly_growth.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart saved: yearly_growth.png ✓")
# ── 5. BUSINESS INSIGHTS ─────────────────────────────────

print("\n" + "="*50)
print("KEY BUSINESS INSIGHTS")
print("="*50)

# Insight 1: Best & worst category
cat_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
print(f"\n[1] Most profitable category : {cat_profit.index[0]} (${cat_profit.iloc[0]:,.0f})")
print(f"    Least profitable category: {cat_profit.index[-1]} (${cat_profit.iloc[-1]:,.0f})")

# Insight 2: Best region
region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
print(f"\n[2] Best region by sales : {region_sales.index[0]} (${region_sales.iloc[0]:,.0f})")
print(f"    Worst region by sales: {region_sales.index[-1]} (${region_sales.iloc[-1]:,.0f})")

# Insight 3: Yearly growth rate
yearly = df.groupby("Year")["Sales"].sum()
growth = ((yearly.iloc[-1] - yearly.iloc[0]) / yearly.iloc[0] * 100)
print(f"\n[3] Sales growth 2014 → 2017: +{growth:.1f}%")

# Insight 4: Discount impact
high_discount = df[df["Discount"] >= 0.3]["Profit"].mean()
low_discount  = df[df["Discount"] <  0.3]["Profit"].mean()
print(f"\n[4] Avg profit WITH high discount (>=30%): ${high_discount:,.2f}")
print(f"    Avg profit WITH low  discount (<30%) : ${low_discount:,.2f}")
print(f"    → High discounts HURT profit by: ${low_discount - high_discount:,.2f} per order")

# Insight 5: Top segment
seg = df.groupby("Segment")["Sales"].sum().sort_values(ascending=False)
print(f"\n[5] Top customer segment: {seg.index[0]} (${seg.iloc[0]:,.0f})")

print("\n" + "="*50)
print("Analysis complete! Charts saved in /outputs")
print("="*50)