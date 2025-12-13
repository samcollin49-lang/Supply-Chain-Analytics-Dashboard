import streamlit as st

import plotly.express as px
from module1 import load_data, preprocess_data


st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")

st.title("📦 Supply Chain Analytics Dashboard")

# Load and preprocess data
df = load_data("Data/DataCoSupplyChainDataset (4).csv")



df = preprocess_data(df)

# Sidebar Filters
st.sidebar.header("🔍 Filters")

categories = ["All"] + sorted(df["Category Name"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select Product Category", categories)

if selected_category != "All":
    df = df[df["Category Name"] == selected_category]

# Show KPIs
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", len(df))
col2.metric("Average Profit", round(df["Benefit per order"].mean(), 2))
col3.metric("Late Delivery (%)", round(df["Is_Late"].mean() * 100, 2))

# Profit by Category
st.subheader("💰 Profit by Category")
profit_df = df.groupby("Category Name")["Benefit per order"].mean().reset_index()
fig1 = px.bar(profit_df, x="Category Name", y="Benefit per order", title="Profit per Category")
st.plotly_chart(fig1, use_container_width=True)

# Delivery Delay Distribution
st.subheader("⏱ Delivery Delay Distribution")
fig2 = px.histogram(df, x="Delivery_Delay", nbins=50, title="Delivery Delay Histogram")
st.plotly_chart(fig2, use_container_width=True)

# Late Delivery by Country
st.subheader("🌍 Late Delivery Rate by Country")
late_df = df.groupby("Customer Country")["Is_Late"].mean().reset_index()
fig3 = px.choropleth(
    late_df,
    locations="Customer Country",
    locationmode="country names",
    color="Is_Late",
    color_continuous_scale="Reds",
    title="Late Deliveries (%) by Country"
)
st.plotly_chart(fig3, use_container_width=True)


