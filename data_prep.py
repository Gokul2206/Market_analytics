import pandas as pd
import numpy as np

# -----------------------------
# 1. Load raw data
# -----------------------------
def load_data(data_path: str, dict_path: str = None) -> pd.DataFrame:
    df = pd.read_csv(data_path, low_memory=False)
    df.columns = df.columns.str.strip()   # remove spaces around column names
    return df

# -----------------------------
# 2. Cleaning
# -----------------------------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Convert date
    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], errors='coerce')

    # Convert categorical
    cat_cols = ['Education','Marital_Status','Country']
    for c in cat_cols:
        if c in df.columns:
            df[c] = df[c].astype('category')

    # Force numeric conversion for known numeric columns
    numeric_cols = [
        'Income','MntWines','MntFruits','MntMeatProducts','MntFishProducts',
        'MntSweetProducts','MntGoldProds','NumDealsPurchases','NumWebPurchases',
        'NumCatalogPurchases','NumStorePurchases','NumWebVisitsMonth',
        'Response','AcceptedCmp1','AcceptedCmp2','AcceptedCmp3','AcceptedCmp4','AcceptedCmp5'
    ]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    return df

# -----------------------------
# 3. Handle outliers & missing
# -----------------------------
def handle_outliers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Age sanity check
    df['Age'] = pd.Timestamp.today().year - df['Year_Birth']
    df.loc[(df['Age'] < 18) | (df['Age'] > 100), 'Age'] = np.nan

    # Winsorize Income
    Q1, Q3 = df['Income'].quantile([0.25,0.75])
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR
    df['Income'] = np.clip(df['Income'], lower, upper)

    # Fill missing numeric with median
    num_cols = df.select_dtypes(include=['int64','float64']).columns
    df[num_cols] = df[num_cols].apply(lambda s: s.fillna(s.median()))

    return df

# -----------------------------
# 4. Feature engineering
# -----------------------------
def derive_features(df: pd.DataFrame, ref_date: pd.Timestamp = None) -> pd.DataFrame:
    df = df.copy()
    now = pd.Timestamp.today() if ref_date is None else ref_date

    # Children
    df['Children'] = df['Kidhome'] + df['Teenhome']

    # Spend & Purchases
    spend_cols = ['MntWines','MntFruits','MntMeatProducts',
                  'MntFishProducts','MntSweetProducts','MntGoldProds']
    purchase_cols = ['NumDealsPurchases','NumWebPurchases',
                     'NumCatalogPurchases','NumStorePurchases','NumWebVisitsMonth']

    df['Total_Spend'] = df[spend_cols].sum(axis=1, numeric_only=True)
    df['Total_Purchases'] = df[purchase_cols].sum(axis=1, numeric_only=True)

    # Tenure
    df['Customer_Tenure_Days'] = (now - df['Dt_Customer']).dt.days

    return df

# -----------------------------
# 5. Banding
# -----------------------------
def apply_bands(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['Age_Band'] = pd.cut(df['Age'], bins=[18,30,40,50,60,100],
                            labels=['18-29','30-39','40-49','50-59','60+'], right=True)
    df['Income_Band'] = pd.cut(df['Income'], bins=[0,30000,75000,150000,300000],
                               labels=['<30k','30-75k','75-150k','150-300k'], right=True)
    return df

# -----------------------------
# 6. Segmentation
# -----------------------------
def build_segments(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    p90_spend = df['Total_Spend'].quantile(0.90)
    df['Seg_High_Income'] = (df['Income'] > 75000).astype(int)
    df['Seg_Young'] = (df['Age'] < 30).astype(int)
    df['Seg_Responder'] = (df['Response'] == 1).astype(int)
    df['Seg_High_Web'] = (df['NumWebVisitsMonth'] > 5).astype(int)
    df['Seg_Family'] = (df['Children'] > 0).astype(int)
    df['Seg_High_Spender'] = (df['Total_Spend'] > p90_spend).astype(int)
    return df

# -----------------------------
# 7. Master pipeline
# -----------------------------
def prep(data_path: str, dict_path: str = None, ref_date: pd.Timestamp = None) -> pd.DataFrame:
    df = load_data(data_path, dict_path)
    df = clean_data(df)
    df = handle_outliers(df)
    df = derive_features(df, ref_date)
    df = apply_bands(df)
    df = build_segments(df)
    return df