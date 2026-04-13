import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from xgboost import XGBRegressor
from datetime import timedelta

# --- PAGE CONFIG ---
st.set_page_config(page_title="Supply Chain BI Dashboard", layout="wide", page_icon="🏭")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    file_path = 'finalCleaned_DataCoSupplyChainDataset.csv'
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    
    # Dates fix
    df['order date (DateOrders)'] = pd.to_datetime(df['order date (DateOrders)'])
    
    # Numeric columns fix
    numeric_cols = ['Sales', 'Order Item Quantity', 'Order Profit Per Order', 'Product Price', 'Order Item Discount']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("📊 Filter Your Data")
region_filter = st.sidebar.multiselect("Select Region", options=sorted(df["Order Region"].unique()), default=df["Order Region"].unique())
category_filter = st.sidebar.multiselect("Select Category", options=sorted(df["Category Name"].unique()), default=df["Category Name"].unique()[:5])
segment_filter = st.sidebar.multiselect("Select Customer Segment", options=sorted(df["Customer Segment"].unique()), default=df["Customer Segment"].unique())

# Filtered Data
df_filtered = df[
    (df["Order Region"].isin(region_filter)) & 
    (df["Category Name"].isin(category_filter)) &
    (df["Customer Segment"].isin(segment_filter))
]

# --- MAIN DASHBOARD ---
st.title("🏭 Supply Chain Strategy Dashboard")
st.markdown("Interactive Business Intelligence for DataCo Supply Chain")

# --- KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${df_filtered['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${df_filtered['Order Profit Per Order'].sum():,.0f}")
col3.metric("Total Orders", f"{len(df_filtered):,}")
col4.metric("Avg Discount", f"${df_filtered['Order Item Discount'].mean():,.2f}")

st.markdown("---")

# --- ROW 1: Q1 & Q2 ---
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("✅ 1. Demand Trend Over Time")
    demand_trend = df_filtered.groupby(df_filtered['order date (DateOrders)'].dt.to_period('M'))['Order Item Quantity'].sum().reset_index()
    demand_trend['order date (DateOrders)'] = demand_trend['order date (DateOrders)'].dt.to_timestamp()
    fig1 = px.line(demand_trend, x='order date (DateOrders)', y='Order Item Quantity', markers=True, template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("✅ 2. Top Selling Products")
    top_selling = df_filtered.groupby('Product Name')['Order Item Quantity'].sum().sort_values(ascending=False).head(10).reset_index()
    fig2 = px.bar(top_selling, x='Order Item Quantity', y='Product Name', orientation='h', color='Order Item Quantity', color_continuous_scale='Viridis')
    st.plotly_chart(fig2, use_container_width=True)

# --- ROW 2: Q3 & Q4 ---
col_c, col_d = st.columns(2)
with col_c:
    st.subheader("✅ 3. Sales by Category")
    sales_cat = df_filtered.groupby('Category Name')['Sales'].sum().reset_index()
    fig3 = px.pie(sales_cat, values='Sales', names='Category Name', hole=0.4)
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    st.subheader("✅ 4. Delivery Performance (Late Risk)")
    del_perf = df_filtered['Delivery Status'].value_counts().reset_index()
    fig4 = px.pie(del_perf, names='Delivery Status', values='count', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig4, use_container_width=True)

# --- ROW 3: Q5 & Q6 ---
col_e, col_f = st.columns(2)
with col_e:
    st.subheader("✅ 5. Shipping Mode Analysis (Speed)")
    ship_mode = df_filtered.groupby('Shipping Mode')['Days for shipping (real)'].mean().sort_values().reset_index()
    fig5 = px.bar(ship_mode, x='Shipping Mode', y='Days for shipping (real)', text_auto='.2f', color='Days for shipping (real)', color_continuous_scale='Bluered')
    st.plotly_chart(fig5, use_container_width=True)

with col_f:
    st.subheader("✅ 6. Profit Analysis by Category")
    profit_cat = df_filtered.groupby('Category Name')['Order Profit Per Order'].sum().sort_values(ascending=False).reset_index()
    fig6 = px.bar(profit_cat, x='Category Name', y='Order Profit Per Order', color='Order Profit Per Order', color_continuous_scale='Greens')
    st.plotly_chart(fig6, use_container_width=True)

# --- ROW 4: Q7 & Q8 ---
col_g, col_h = st.columns(2)
with col_g:
    st.subheader("✅ 7. Regional Sales Analysis")
    reg_sales = df_filtered.groupby('Order Region')['Sales'].sum().sort_values().reset_index()
    fig7 = px.bar(reg_sales, x='Sales', y='Order Region', orientation='h', color='Sales', color_continuous_scale='Purples')
    st.plotly_chart(fig7, use_container_width=True)

with col_h:
    st.subheader("✅ 8. Customer Segment Analysis")
    seg_sales = df_filtered.groupby('Customer Segment')['Sales'].sum().reset_index()
    fig8 = px.bar(seg_sales, x='Customer Segment', y='Sales', color='Customer Segment')
    st.plotly_chart(fig8, use_container_width=True)

# --- ROW 5: Q9 & Q10 ---
col_i, col_j = st.columns(2)
with col_i:
    st.subheader("✅ 9. Discount Impact on Sales")
    fig9 = px.scatter(df_filtered.sample(min(5000, len(df_filtered))), x='Order Item Discount', y='Sales', trendline="ols", opacity=0.4)
    st.plotly_chart(fig9, use_container_width=True)

with col_j:
    st.subheader("✅ 10. Late Delivery Comparison")
    fig10 = px.box(df_filtered, x='Shipping Mode', y='Days for shipping (real)', color='Delivery Status')
    st.plotly_chart(fig10, use_container_width=True)

# --- ADVANCED BONUS: Q11 FORECAST ---
st.markdown("---")
st.header("🚀 11. Advanced: Future Demand Forecast (Next 5 Months)")
try:
    df_forecast = df.groupby(df['order date (DateOrders)'].dt.to_period('M'))['Order Item Quantity'].sum().reset_index()
    df_forecast['order date (DateOrders)'] = df_forecast['order date (DateOrders)'].dt.to_timestamp()
    df_forecast['Month'] = df_forecast['order date (DateOrders)'].dt.month
    df_forecast['Year'] = df_forecast['order date (DateOrders)'].dt.year
    
    X_f = df_forecast[['Month', 'Year']]
    y_f = df_forecast['Order Item Quantity']
    
    model = XGBRegressor(n_estimators=100)
    model.fit(X_f, y_f)
    
    last_date = df_forecast['order date (DateOrders)'].max()
    future_dates = [last_date + timedelta(days=31*i) for i in range(1, 6)]
    future_df = pd.DataFrame({
        'Month': [d.month for d in future_dates],
        'Year': [d.year for d in future_dates]
    })
    predictions = model.predict(future_df)
    
    fig11 = go.Figure()
    fig11.add_trace(go.Scatter(x=df_forecast['order date (DateOrders)'], y=df_forecast['Order Item Quantity'], name='Historical Demand'))
    fig11.add_trace(go.Scatter(x=future_dates, y=predictions, name='XGBoost Forecast', line=dict(dash='dash', color='red')))
    fig11.update_layout(title="Predicted Order Volumes (Next 5 Months)", template="plotly_white")
    st.plotly_chart(fig11, use_container_width=True)
except Exception as e:
    st.warning(f"Forecasting unavailable: {e}")

st.success("Industrial Level Dashboard Ready!")
