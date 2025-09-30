
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load the dataset
df = pd.read_csv('lulu_synthetic_data.csv')

# Streamlit Layout
st.set_page_config(page_title="Lulu UAE Sales Dashboard", layout="wide")
st.title("Lulu UAE Sales Dashboard")
st.markdown("Analyze sales, loyalty program & advertisement budget data by demographic filters.")

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_region = st.sidebar.multiselect("Select Region", df['Region'].unique(), default=df['Region'].unique())
selected_category = st.sidebar.multiselect("Select Category", df['Category'].unique(), default=df['Category'].unique())
selected_gender = st.sidebar.multiselect("Select Gender", df['Gender'].unique(), default=df['Gender'].unique())
selected_loyalty = st.sidebar.multiselect("Select Loyalty Status", df['Loyalty_Status'].unique(), default=df['Loyalty_Status'].unique())

# Filter data
filtered_df = df[(df['Region'].isin(selected_region)) &
                 (df['Category'].isin(selected_category)) &
                 (df['Gender'].isin(selected_gender)) &
                 (df['Loyalty_Status'].isin(selected_loyalty))]

# Key Metrics
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"AED {filtered_df['Sales_Amount'].sum():,.2f}")
col2.metric("Average Sales", f"AED {filtered_df['Sales_Amount'].mean():,.2f}")
col3.metric("Total Customers", filtered_df['Customer'].nunique())
col4.metric("Avg Ad Budget", f"AED {filtered_df['Ad_Budget_Expenditure'].mean():,.2f}")

# Sales by Category
st.subheader("Sales by Category")
sales_category = filtered_df.groupby('Category')['Sales_Amount'].sum().reset_index()
fig1 = px.pie(sales_category, names='Category', values='Sales_Amount', title="Sales Distribution by Category")
st.plotly_chart(fig1, use_container_width=True)

# Sales Trend by Age
st.subheader("Sales Trend by Age")
sales_age = filtered_df.groupby('Age')['Sales_Amount'].sum().reset_index()
fig2 = px.line(sales_age, x='Age', y='Sales_Amount', markers=True, title="Sales Trend by Age")
st.plotly_chart(fig2, use_container_width=True)

# Loyalty Program Analysis
st.subheader("Loyalty Program Distribution")
loyalty_counts = filtered_df['Loyalty_Status'].value_counts().reset_index()
loyalty_counts.columns = ['Loyalty_Status', 'Count']
fig3 = px.bar(loyalty_counts, x='Loyalty_Status', y='Count', color='Loyalty_Status', title="Loyalty Program Participation")
st.plotly_chart(fig3, use_container_width=True)

# Advertisement Budget Analysis
st.subheader("Advertisement Budget Expenditure")
ad_budget_category = filtered_df.groupby('Category')['Ad_Budget_Expenditure'].sum().reset_index()
fig4 = px.bar(ad_budget_category, x='Category', y='Ad_Budget_Expenditure', color='Category', title="Ad Budget by Category")
st.plotly_chart(fig4, use_container_width=True)

# Raw Data
st.subheader("Raw Data")
st.dataframe(filtered_df)
