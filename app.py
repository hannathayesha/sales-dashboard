import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown("""
# 📊 Sales Intelligence Dashboard
### Real-time Business Performance Analytics
""")
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales & Revenue Dashboard")

# Load data
df = pd.read_csv("data/sales.csv")

df["Sales"] = pd.to_numeric(df["Sales"])
df["Profit"] = pd.to_numeric(df["Profit"])
# ---------------- FILTERS ----------------
st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]


st.divider()
# ---------------- KPI SECTION ----------------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Total Orders", f"{total_orders:,}")
st.divider()


# ---------------- CHART SECTION ----------------
st.subheader("📈 Sales Trend")

df["Order Date"] = pd.to_datetime(df["Order Date"])
sales_trend = df.groupby("Order Date")["Sales"].sum().reset_index()

fig = px.line(sales_trend, x="Order Date", y="Sales", title="Sales Over Time")
st.plotly_chart(fig, use_container_width=True)

st.divider()


st.subheader("🏆 Top 10 Products")

top_products = df.groupby("Product Name")["Sales"].sum().nlargest(10).reset_index()

fig2 = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Sales"
)


st.plotly_chart(fig2, use_container_width=True)
st.divider()

st.subheader("💰 Profit by Category")

profit_cat = df.groupby("Category")["Profit"].sum().reset_index()

fig3 = px.bar(
    profit_cat,
    x="Category",
    y="Profit",
    title="Profit by Category",
    text_auto=True
)

st.plotly_chart(fig3, use_container_width=True)
st.divider()

# ---------------- DATA SECTION ----------------
st.subheader("📋 Data Preview")
st.dataframe(df)

st.subheader("💡 Key Business Insights")

best_product = df.groupby("Product Name")["Sales"].sum().idxmax()
best_category = df.groupby("Category")["Profit"].sum().idxmax()
total_revenue = df["Sales"].sum()

st.info(f"""
- 🏆 Best Selling Product: {best_product}
- 💰 Most Profitable Category: {best_category}
- 📊 Total Revenue: ${total_revenue:,.2f}
""")