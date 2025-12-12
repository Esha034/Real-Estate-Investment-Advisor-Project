
import pandas as pd
import numpy as np
import datetime
import os

# Optional: For Plotly boxplots (hover-enabled)
import plotly.express as px


def load_data(path="data/india_housing_prices.csv"):
    """Load dataset from the data folder."""
    return pd.read_csv(path)


def cap_outliers(series):
    """Cap outliers using the IQR method."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr
    return series.clip(lower=low, upper=high)


def preprocess_data(df):
    """Apply all preprocessing steps used in the notebook."""
    
    # -------------------------
    # BASIC CLEANING
    # -------------------------
    df = df.drop_duplicates()

    # Convert Price to numeric
    df['Price_in_Lakhs'] = pd.to_numeric(df['Price_in_Lakhs'], errors='coerce')

    # Compute Price_per_SqFt
    df['Price_per_SqFt'] = (df['Price_in_Lakhs'] * 1e5) / df['Size_in_SqFt']
    df['Price_per_SqFt'] = df['Price_per_SqFt'].round(2)

    # -------------------------
    # IMPUTATION
    # -------------------------
    # Numeric imputation
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    for c in num_cols:
        df[c] = df[c].fillna(df[c].median())

    # Categorical imputation
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    for c in cat_cols:
        df[c] = df[c].fillna(df[c].mode().iloc[0])

    # -------------------------
    # FEATURE ENGINEERING
    # -------------------------
    current_year = datetime.datetime.now().year
    if 'Year_Built' in df.columns:
        df['Age_of_Property'] = current_year - pd.to_numeric(df['Year_Built'], errors='coerce')
        df['Age_of_Property'] = df['Age_of_Property'].fillna(df['Age_of_Property'].median())

    # Binary flags
    df['is_ready_to_move'] = df['Availability_Status'].str.lower().str.contains('ready').astype(int)
    df['has_parking'] = df['Parking_Space'].fillna('No').map({'Yes': 1, 'No': 0})

    # -------------------------
    # OUTLIER CAPPING
    # -------------------------
    df['Price_per_SqFt_capped'] = cap_outliers(df['Price_per_SqFt'])
    df['Size_in_SqFt_capped'] = cap_outliers(df['Size_in_SqFt'])

    # -------------------------
    # GOOD INVESTMENT LABEL
    # -------------------------
    df['City_median_price'] = df.groupby('City')['Price_in_Lakhs'].transform('median')

    df['Good_Investment'] = (
        ((df['Price_in_Lakhs'] <= df['City_median_price']) |
         (df['Price_per_SqFt'] <= df.groupby('City')['Price_per_SqFt'].transform('median')))
        & (df['is_ready_to_move'] == 1)
        & ((df['BHK'] >= 2) | (df['has_parking'] == 1))
    ).astype(int)

    return df


# -----------------------------
# OPTIONAL: PLOTLY VISUAL SAVERS
# -----------------------------
def save_plotly_visuals(df, out_dir="../outputs/figures/"):
    """Generate Plotly boxplots for interactive visualizations (optional)."""
    os.makedirs(out_dir, exist_ok=True)

    # Boxplot - Price_per_SqFt_capped
    fig1 = px.box(df, y="Price_per_SqFt_capped",
                  title="Price_per_SqFt (Capped) — Interactive Boxplot")
    fig1.write_html(os.path.join(out_dir, "boxplot_price_per_sqft_capped.html"))

    # Boxplot - Size_in_SqFt_capped
    fig2 = px.box(df, y="Size_in_SqFt_capped",
                  title="Size_in_SqFt (Capped) — Interactive Boxplot")
    fig2.write_html(os.path.join(out_dir, "boxplot_size_sqft_capped.html"))


def export_data(df, path="../outputs/cleaned_india_housing_prices.csv"):
    """Save cleaned dataset to outputs folder."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved cleaned dataset to {path}")


if __name__ == "__main__":
    print("Loading dataset...")
    df = load_data()

    print("Processing dataset...")
    df_clean = preprocess_data(df)

    print("Exporting cleaned dataset...")
    export_data(df_clean)

    print("Preprocessing complete!")
