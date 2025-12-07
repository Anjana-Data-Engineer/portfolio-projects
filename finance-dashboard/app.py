# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Personal Finance Dashboard")
st.title("Personal Finance Dashboard")

uploaded = st.file_uploader("Upload CSV (columns: date,category,amount)", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded, parse_dates=["date"])
    st.subheader("Preview")
    st.dataframe(df.head())

    st.subheader("Monthly Spend")
    df['month'] = df['date'].dt.to_period("M").astype(str)
    monthly = df.groupby('month')['amount'].sum().reset_index()
    st.line_chart(monthly.set_index('month'))

    st.subheader("Category Breakdown")
    cat = df.groupby('category')['amount'].sum().reset_index()
    st.table(cat.sort_values(by='amount', ascending=False))

    st.subheader("Largest Transactions")
    st.table(df.sort_values(by='amount', ascending=False).head(10))
else:
    st.info("Upload CSV to get started. Sample data in sample_data/expenses.csv")
