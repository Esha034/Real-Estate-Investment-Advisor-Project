# src/eda_utils.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set a clean plot style
def _set_style():
    sns.set_style("whitegrid")

# Ensure output directory exists
def _ensure_dir(path="outputs/figures/"):
    os.makedirs(path, exist_ok=True)
    return path

# ----------------------
# 1. Price Distribution
# ----------------------
def plot_price_distribution(df, out_dir="../outputs/figures/"):
    _set_style()
    out_dir = _ensure_dir(out_dir)

    plt.figure(figsize=(8, 4))
    sns.histplot(df['Price_in_Lakhs'], bins=50, kde=True)
    plt.title("Distribution of Property Prices (in Lakhs)")
    plt.xlabel("Price (Lakhs)")
    plt.ylabel("Count")
    path = os.path.join(out_dir, "price_distribution.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    return path

# ----------------------
# 2. Size Distribution
# ----------------------

def plot_size_distribution(df, out_dir="../outputs/figures/"):
    _set_style()
    out_dir = _ensure_dir(out_dir)

    plt.figure(figsize=(8, 4))
    sns.histplot(df['Size_in_SqFt_capped'], bins=50, kde=True)
    plt.title("Distribution of Property Sizes (SqFt)")
    path = os.path.join(out_dir, "size_distribution.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    return path

# ----------------------
# 3. Price per SqFt by Property Type (Boxplot)
# ----------------------

def plot_price_per_sqft_by_type(df, out_dir="../outputs/figures/"):
    _set_style()
    out_dir = _ensure_dir(out_dir)

    plt.figure(figsize=(9, 6))
    sns.boxplot(x='Property_Type', y='Price_per_SqFt_capped', data=df)
    plt.xticks(rotation=45)
    plt.title("Price per SqFt by Property Type")
    path = os.path.join(out_dir, "price_per_sqft_by_type.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    return path

# ----------------------
# 4. Price vs Size (Scatter + Regression)
# ----------------------

def plot_price_vs_size(df, out_dir="../outputs/figures/"):
    _set_style()
    out_dir = _ensure_dir(out_dir)

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='Size_in_SqFt_capped', y='Price_in_Lakhs', 
                    hue='Property_Type', data=df, alpha=0.6)
    sns.regplot(x='Size_in_SqFt_capped', y='Price_in_Lakhs', data=df,
                scatter=False, lowess=True, color='black')
    plt.title("Price vs Size")
    path = os.path.join(out_dir, "price_vs_size.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    return path

# ----------------------
# 5. Avg Price per SqFt by City (Bar Chart)
# ----------------------

def plot_avg_price_by_city(df, out_dir="../outputs/figures/"):
    _set_style()
    out_dir = _ensure_dir(out_dir)

    city_avg = df.groupby('City')['Price_per_SqFt_capped'].mean().sort_values(ascending=False)

    plt.figure(figsize=(10, 5))
    city_avg.plot(kind='bar', title='Average Price per SqFt by City')
    path = os.path.join(out_dir, "avg_price_by_city.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    return path

# ----------------------
# 6. BHK Distribution
# ----------------------

def plot_bhk_distribution(df, out_dir="../outputs/figures/"):
    _set_style()
    out_dir = _ensure_dir(out_dir)

    plt.figure(figsize=(10, 4))
    sns.countplot(x='BHK', data=df)
    plt.title("BHK Distribution")
    path = os.path.join(out_dir, "bhk_distribution.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    return path

# ----------------------
# 7. Correlation Matrix Heatmap
# ----------------------

def plot_correlation_heatmap(df, out_dir="../outputs/figures/"):
    _set_style()
    out_dir = _ensure_dir(out_dir)

    num_cols = ['Price_in_Lakhs','Price_per_SqFt_capped','Size_in_SqFt_capped',
                'BHK','Nearby_Schools','Nearby_Hospitals','Age_of_Property']

    corr = df[num_cols].corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='viridis')
    plt.title("Correlation Matrix")
    path = os.path.join(out_dir, "correlation_heatmap.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    return path

# ----------------------
# 8. Owner Type Counts
# ----------------------

def plot_owner_type_counts(df, out_dir="../outputs/figures/"):
    _set_style()
    out_dir = _ensure_dir(out_dir)

    owner_counts = df['Owner_Type'].value_counts()

    plt.figure(figsize=(8, 4))
    sns.barplot(x=owner_counts.index, y=owner_counts.values)
    plt.title("Number of Properties by Owner Type")
    plt.xlabel("Owner Type")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    path = os.path.join(out_dir, "owner_type_counts.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    return path

# ----------------------
# 9. Parking Space Impact on Price
# ----------------------

def plot_parking_vs_price(df, out_dir="../outputs/figures/"):
    _set_style()
    out_dir = _ensure_dir(out_dir)

    plt.figure(figsize=(8, 5))
    sns.boxplot(x='has_parking', y='Price_in_Lakhs', data=df)
    plt.title("Impact of Parking Space on Property Price")
    plt.xlabel("Has Parking (0 = No, 1 = Yes)")
    plt.ylabel("Price (Lakhs)")
    path = os.path.join(out_dir, "parking_vs_price.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    return path

# ----------------------
# 10. Amenities vs Price per SqFt
# ----------------------

def plot_amenities_vs_ppsqft(df, out_dir="../outputs/figures/"):
    _set_style()
    out_dir = _ensure_dir(out_dir)

    plt.figure(figsize=(8, 5))
    sns.scatterplot(x='Amenities', y='Price_per_SqFt_capped', data=df, alpha=0.6)
    plt.title("Amenities vs Price per Sq Ft")
    plt.xlabel("Total Amenities")
    plt.ylabel("Price per SqFt")
    path = os.path.join(out_dir, "amenities_vs_ppsqft.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    return path

# ----------------------
# 11. Public Transport Accessibility vs Price per SqFt
# ----------------------

def plot_public_transport_vs_ppsqft(df, out_dir="../outputs/figures/"):
    _set_style()
    out_dir = _ensure_dir(out_dir)

    plt.figure(figsize=(8, 5))
    sns.scatterplot(x='Public_Transport_Accessibility', y='Price_per_SqFt_capped', data=df, alpha=0.6)
    plt.title("Public Transport Accessibility vs Price per Sq Ft")
    plt.xlabel("Public Transport Accessibility")
    plt.ylabel("Price per SqFt")
    path = os.path.join(out_dir, "public_transport_vs_ppsqft.png")
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    return path


# ----------------------
# Main helper to generate all plots
# ----------------------

def generate_all_eda_plots(df, out_dir="../outputs/figures/"):
    """Generate all EDA plots and save them to outputs/figures"""
    plots = {}
    plots['price_distribution'] = plot_price_distribution(df, out_dir)
    plots['size_distribution'] = plot_size_distribution(df, out_dir)
    plots['price_per_sqft_by_type'] = plot_price_per_sqft_by_type(df, out_dir)
    plots['price_vs_size'] = plot_price_vs_size(df, out_dir)
    plots['avg_price_by_city'] = plot_avg_price_by_city(df, out_dir)
    plots['bhk_distribution'] = plot_bhk_distribution(df, out_dir)
    plots['correlation_heatmap'] = plot_correlation_heatmap(df, out_dir)
    plots['owner_type_counts'] = plot_owner_type_counts(df, out_dir)
    plots['parking_vs_price'] = plot_parking_vs_price(df, out_dir)
    plots['amenities_vs_ppsqft'] = plot_amenities_vs_ppsqft(df, out_dir)
    plots['public_transport_vs_ppsqft'] = plot_public_transport_vs_ppsqft(df, out_dir)

    return plots