import streamlit as st
import pandas as pd
import altair as alt
from data_prep import prep

st.set_page_config(page_title="Marketing Analytics Dashboard", layout="wide")

st.title("📊 Marketing Analytics Dashboard")

# --- Load cleaned data with spinner and exception handling ---
try:
    with st.spinner("Loading and cleaning data..."):
        df = prep("data/marketing_campaign_data.csv")
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# --- Sidebar filters ---
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect("Country", df["Country"].unique())
selected_age_bands = st.sidebar.multiselect("Age Band", df["Age_Band"].unique())
selected_income_bands = st.sidebar.multiselect("Income Band", df["Income_Band"].unique())

# --- Default to all if nothing selected ---
if not selected_countries:
    selected_countries = df["Country"].unique()
if not selected_age_bands:
    selected_age_bands = df["Age_Band"].unique()
if not selected_income_bands:
    selected_income_bands = df["Income_Band"].unique()

# --- Apply filters ---
try:
    filtered = df[
        (df["Country"].isin(selected_countries)) &
        (df["Age_Band"].isin(selected_age_bands)) &
        (df["Income_Band"].isin(selected_income_bands))
    ]
except KeyError as e:
    st.error(f"❌ Missing expected column: {e}")
    st.stop()

# --- Handle empty filter case ---
if filtered.empty:
    st.warning("⚠️ No data available for the selected filters. Try resetting filters.")
    st.stop()

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Response Rate", f"{filtered['Response'].mean():.2%}")
col2.metric("Avg Spend", f"{filtered['Total_Spend'].mean():.0f}")
col3.metric("Avg Purchases", f"{filtered['Total_Purchases'].mean():.1f}")
col4.metric("Avg Web Visits", f"{filtered['NumWebVisitsMonth'].mean():.1f}")

# --- Tabs for visuals ---
tab1, tab2, tab3, tab4 = st.tabs(["📈 Campaigns", "🍷 Products", "🛒 Channels", "👥 Segments"])

with tab1:
    st.subheader("Campaign Acceptance Rates")
    try:
        cmp_cols = ["AcceptedCmp1","AcceptedCmp2","AcceptedCmp3","AcceptedCmp4","AcceptedCmp5","Response"]
        cmp_data = filtered[cmp_cols].mean().reset_index()
        cmp_data.columns = ["Campaign","Rate"]
        chart = alt.Chart(cmp_data).mark_bar().encode(
            x="Campaign", y="Rate", tooltip=["Campaign","Rate"]
        )
        st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error rendering campaign chart: {e}")

with tab2:
    st.subheader("Product Spend by Demographics")
    try:
        spend_cols = ["MntWines","MntFruits","MntMeatProducts","MntFishProducts","MntSweetProducts","MntGoldProds"]
        spend_data = filtered.groupby("Age_Band")[spend_cols].mean().reset_index()
        spend_data = spend_data.melt("Age_Band", var_name="Product", value_name="AvgSpend")
        chart = alt.Chart(spend_data).mark_bar().encode(
            x="Age_Band", y="AvgSpend", color="Product", tooltip=["Age_Band","Product","AvgSpend"]
        )
        st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error rendering product chart: {e}")

with tab3:
    st.subheader("Channel Usage by High-Value Customers")
    try:
        channel_cols = ["NumWebPurchases","NumCatalogPurchases","NumStorePurchases","NumDealsPurchases"]
        channel_data = filtered[channel_cols].mean().reset_index()
        channel_data.columns = ["Channel","AvgUsage"]
        chart = alt.Chart(channel_data).mark_bar().encode(
            x="Channel", y="AvgUsage", tooltip=["Channel","AvgUsage"]
        )
        st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error rendering channel chart: {e}")

with tab4:
    st.subheader("Segment Response Lift")
    try:
        seg_cols = ["Seg_High_Income","Seg_Young","Seg_Responder","Seg_High_Web","Seg_Family","Seg_High_Spender"]
        seg_data = []
        for seg in seg_cols:
            if seg in filtered.columns:
                rate = filtered.loc[filtered[seg]==1,"Response"].mean()
                seg_data.append({"Segment":seg,"ResponseRate":rate})
        seg_df = pd.DataFrame(seg_data)
        chart = alt.Chart(seg_df).mark_bar().encode(
            x="Segment", y="ResponseRate", tooltip=["Segment","ResponseRate"]
        )
        st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error rendering segment chart: {e}")

# --- Reset Filters Button ---
if st.sidebar.button("Reset Filters"):
    st.experimental_rerun()