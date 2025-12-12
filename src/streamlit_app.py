import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Real Estate Investment Advisor", layout="wide")
st.title("Real Estate Investment Advisor Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("outputs/cleaned_india_housing_prices.zip", compression='zip')

df = load_data()

# Sidebar Filters
st.sidebar.header(" Property Search & Filters")
city = st.sidebar.selectbox("City", ["All"] + sorted(df['City'].unique()))
ptype = st.sidebar.selectbox("Property Type", ["All"] + sorted(df['Property_Type'].unique()))

min_price, max_price = int(df['Price_in_Lakhs'].min()), int(df['Price_in_Lakhs'].max())
price_range = st.sidebar.slider("Price Range (Lakhs)", min_price, max_price, (min_price, max_price))

# Apply filters
df_filtered = df.copy()
if city != "All": df_filtered = df_filtered[df_filtered['City'] == city]
if ptype != "All": df_filtered = df_filtered[df_filtered['Property_Type'] == ptype]
df_filtered = df_filtered[(df_filtered['Price_in_Lakhs'] >= price_range[0]) & (df_filtered['Price_in_Lakhs'] <= price_range[1])]

# Tabs Setup
tab1, tab2, tab3 = st.tabs(["Property Analysis", " Insights & EDA", " Export & Summary"])

# ----------------------------- TAB 1: PROPERTY ANALYSIS -----------------------------
with tab1:
    st.subheader(" Property Analysis")

    # Property selection
    prop_id = st.selectbox("Select Property ID", ["Choose a property"] + df_filtered['ID'].astype(str).tolist())

    if prop_id != "Choose a property":
        prop = df_filtered[df_filtered['ID'].astype(str) == prop_id].iloc[0]

        # KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("Price (Lakhs)", f"{prop['Price_in_Lakhs']:.2f}")
        col2.metric("Price per SqFt", f"{prop['Price_per_SqFt']:.2f}")
        col3.metric("Good Investment?", "Yes" if prop['Good_Investment']==1 else "No")

        # Property details
        st.write("###  Property Details")
        st.dataframe(prop.to_frame().rename(columns={prop_id: "Value"}))

        # Price growth models
        st.write("###  5-Year Price Estimation")
        r_fixed = st.number_input("Fixed Annual Growth (decimal)", 0.0, 1.0, 0.08, 0.01)
        fixed_future = prop['Price_in_Lakhs'] * ((1 + r_fixed)**5)
        st.info(f"**Fixed-rate 5-year estimate:** {fixed_future:.2f} Lakhs")

        # City-based growth
        st.write("#### City-Based Growth")
        city_rate = st.slider("City Growth Rate", 0.01, 0.20, 0.10)
        city_future = prop['Price_in_Lakhs'] * ((1 + city_rate)**5)
        st.success(f"**City-based 5-year estimate:** {city_future:.2f} Lakhs")

        # Plot: Price Comparison
        fig = go.Figure()
        fig.add_trace(go.Bar(x=["Current Price"], y=[prop['Price_in_Lakhs']], name="Current"))
        fig.add_trace(go.Bar(x=["Fixed Growth"], y=[fixed_future], name="Fixed Rate"))
        fig.add_trace(go.Bar(x=["City Growth"], y=[city_future], name="City Rate"))
        fig.update_layout(title="Price Projection Comparison", height=400)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Please select a property to begin analysis.")

# ----------------------------- TAB 2: INSIGHTS & EDA -----------------------------
with tab2:
    st.subheader(" Market Insights & EDA")

    # KPI Section
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg Price", f"{df_filtered['Price_in_Lakhs'].mean():.2f}")
    c2.metric("Avg Size SqFt", f"{df_filtered['Size_in_SqFt_capped'].mean():.0f}")
    c3.metric("Avg Price per SqFt", f"{df_filtered['Price_per_SqFt_capped'].mean():.2f}")
    c4.metric("Total Properties", len(df_filtered))

    # --------------------- PRICE DISTRIBUTION ---------------------
    st.write("### Price Distribution")
    fig1 = px.histogram(df_filtered, x="Price_in_Lakhs", nbins=50, title="Price Distribution", height=400)
    st.plotly_chart(fig1, use_container_width=True)

    # --------------------- SIZE DISTRIBUTION ----------------------
    st.write("###  Size Distribution (SqFt)")
    fig2 = px.histogram(df_filtered, x="Size_in_SqFt_capped", nbins=50, title="Size Distribution", height=400)
    st.plotly_chart(fig2, use_container_width=True)

    # --------------------- PRICE VS SIZE --------------------------
    st.write("###  Price vs Size")
    fig3 = px.scatter(df_filtered, x="Size_in_SqFt_capped", y="Price_in_Lakhs", color="Property_Type", title="Price vs Size", height=450)
    st.plotly_chart(fig3, use_container_width=True)

    # --------------------- CITY-WISE AVG PRICE --------------------
    st.write("###  City-wise Avg Price per SqFt")
    df_city = df_filtered.groupby('City')['Price_per_SqFt_capped'].mean().reset_index()
    fig4 = px.bar(df_city, x='City', y='Price_per_SqFt_capped', title="Avg Price/SqFt by City", height=450)
    st.plotly_chart(fig4, use_container_width=True)

    # --------------------- CORRELATION HEATMAP --------------------
    st.write("###  Correlation Heatmap")
    num_cols = ['Price_in_Lakhs','Price_per_SqFt_capped','Size_in_SqFt_capped','BHK','Nearby_Schools','Nearby_Hospitals','Age_of_Property']
    corr = df_filtered[num_cols].corr()
    fig5 = px.imshow(corr, text_auto=True, title="Feature Correlation", height=500, color_continuous_scale="Viridis")
    st.plotly_chart(fig5, use_container_width=True)

    # --------------------- NEW ADDITIONS BELOW ---------------------

    # BHK Distribution
    st.write("###  BHK Distribution")
    fig6 = px.histogram(df_filtered, x="BHK", title="BHK Count Distribution", height=400)
    st.plotly_chart(fig6, use_container_width=True)

    # Parking Space vs Price
    st.write("### 🚗 Parking Space Impact on Price")
    fig8 = px.box(df_filtered, x="has_parking", y="Price_in_Lakhs",
                  title="Parking Availability vs Property Price",
                  labels={'has_parking': 'Has Parking (0=No, 1=Yes)', 'Price_in_Lakhs':'Price (Lakhs)'}, height=450)
    st.plotly_chart(fig8, use_container_width=True)

    # Amenities vs Price per SqFt
    st.write("###  Amenities vs Price per SqFt")
    fig9 = px.scatter(df_filtered, x="Amenities", y="Price_per_SqFt_capped", color="Property_Type",
                      title="Amenities vs Price per SqFt", height=450)
    st.plotly_chart(fig9, use_container_width=True)

    # Public Transport Accessibility vs Price per SqFt
    st.write("### 🚌 Public Transport Accessibility vs Price per SqFt")
    fig10 = px.scatter(df_filtered, x="Public_Transport_Accessibility", y="Price_per_SqFt_capped", color="City",
                       title="Transport Accessibility vs Price per SqFt", height=450)
    st.plotly_chart(fig10, use_container_width=True)

# ----------------------------- TAB 3: EXPORT & SUMMARY -----------------------------
with tab3:
    st.subheader("📁 Export Cleaned Dataset & Summary Report")

    st.write("### Download Cleaned Processed Dataset")
    st.download_button(" Download CSV", data=open("outputs/cleaned_india_housing_prices.csv", "rb"), file_name="cleaned_india_housing_prices.csv")

    st.write("### Summary of Findings")
    st.write("- ✔ Market distribution visualized with dynamic charts")
    st.write("- ✔ KPIs reflect filtered area performance")
    st.write("- ✔ Price growth estimated using fixed & city-based models")
    st.write("- ✔ Property-wise insights & investment recommendation included")


