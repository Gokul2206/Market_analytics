import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from data_prep import prep

st.set_page_config(page_title="Marketing Analytics Dashboard", layout="wide")
st.title("Customer & Campaign Analytics")

@st.cache_data
def load_data():
    return prep("data/marketing_campaign_data.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
country = st.sidebar.multiselect("Country", sorted(df['Country'].unique()))
age_band = st.sidebar.multiselect("Age Band", sorted(df['Age_Band'].dropna().unique()))
income_band = st.sidebar.multiselect("Income Band", sorted(df['Income_Band'].dropna().unique()))

filtered = df.copy()
if country: filtered = filtered[filtered['Country'].isin(country)]
if age_band: filtered = filtered[filtered['Age_Band'].isin(age_band)]
if income_band: filtered = filtered[filtered['Income_Band'].isin(income_band)]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Response Rate", f"{filtered['Response'].mean():.2%}")
col2.metric("Avg Spend", f"{filtered['Total_Spend'].mean():,.0f}")
col3.metric("Avg Purchases", f"{filtered['Total_Purchases'].mean():.1f}")
col4.metric("Avg Web Visits", f"{filtered['NumWebVisitsMonth'].mean():.1f}")

# Tabs for visuals
tab1, tab2, tab3, tab4 = st.tabs(["Campaigns","Products","Channels","Segments"])

with tab1:
    st.subheader("Campaign Acceptance Rates")
    cmp_cols = ['AcceptedCmp1','AcceptedCmp2','AcceptedCmp3','AcceptedCmp4','AcceptedCmp5']
    st.bar_chart(filtered[cmp_cols].mean())

with tab2:
    st.subheader("Product Spend by Demographics")
    demo_cols = ['Age_Band','Income_Band','Marital_Status']
    for col in demo_cols:
        fig, ax = plt.subplots()
        sns.barplot(x=col, y='Total_Spend', data=filtered, ax=ax, estimator=sum)
        plt.title(f"Total Spend by {col}")
        st.pyplot(fig)

with tab3:
    st.subheader("Channel Usage")
    channels = ['NumWebPurchases','NumStorePurchases','NumCatalogPurchases','NumDealsPurchases']
    st.write(filtered[channels].mean())

with tab4:
    st.subheader("Segment Response Lift")
    segment_cols = ['Seg_High_Income','Seg_Young','Seg_Responder',
                    'Seg_High_Web','Seg_Family','Seg_High_Spender']
    overall_rate = filtered['Response'].mean()
    seg_rates = {seg: filtered.loc[filtered[seg]==1,'Response'].mean() for seg in segment_cols}
    st.write(pd.DataFrame.from_dict(seg_rates, orient='index', columns=['Response Rate']))
    st.write(f"Overall Response Rate: {overall_rate:.2%}")
