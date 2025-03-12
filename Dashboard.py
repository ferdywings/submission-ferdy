import os
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
orders_df = pd.read_csv("order_sharing_data.csv")
payments_df = pd.read_csv("payments_sharing_data.csv")
product_category_df = pd.read_csv("product_category_sharing_data.csv")
products_df = pd.read_csv("products_sharing_data.csv")
reviews_df = pd.read_csv("reviews_sharing_data.csv")

# Sidebar Filters
st.sidebar.title("E-commerce Dashboard")

# Filtering by Payment Method
payment_options = payments_df["payment_type"].unique().tolist()
selected_payment = st.sidebar.selectbox("Pilih Metode Pembayaran", ["Semua"] + payment_options)

# Filtering by Review Score
review_options = sorted(reviews_df["review_score"].unique().tolist())
selected_review = st.sidebar.selectbox("Pilih Skor Review", ["Semua"] + list(map(str, review_options)))

# Filtering Data
filtered_orders_df = orders_df.copy()
if selected_payment != "Semua":
    filtered_orders_df = filtered_orders_df[filtered_orders_df["order_id"].isin(payments_df[payments_df["payment_type"] == selected_payment]["order_id"])]

if selected_review != "Semua":
    filtered_orders_df = filtered_orders_df[filtered_orders_df["order_id"].isin(reviews_df[reviews_df["review_score"] == int(selected_review)]["order_id"])]

# Calculate total sales
total_sales = filtered_orders_df["price"].sum()
st.sidebar.metric(label="Total Sales", value=f"${total_sales:,.2f}")

# Streamlit Main Content
st.title("E-commerce Dashboard")

st.subheader("Total Sales")
st.metric(label="Total Sales", value=f"${total_sales:,.2f}")

st.subheader("Distribusi Metode Pembayaran")
payment_distribution = payments_df["payment_type"].value_counts().reset_index()
payment_distribution.columns = ["Metode Pembayaran", "Jumlah Transaksi"]
if selected_payment != "Semua":
    payment_distribution = payment_distribution[payment_distribution["Metode Pembayaran"] == selected_payment]
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=payment_distribution, x="Jumlah Transaksi", y="Metode Pembayaran", hue="Metode Pembayaran", palette="coolwarm", legend=False, ax=ax)
ax.set_xlabel("Jumlah Transaksi")
ax.set_ylabel("Metode Pembayaran")
ax.set_title("Distribusi Metode Pembayaran")
ax.grid(axis='x', linestyle='--', alpha=0.7)
st.pyplot(fig)

st.subheader("Kategori Produk Terlaris")
merged_df = filtered_orders_df.merge(products_df, on="product_id", how="left")
merged_df = merged_df.merge(product_category_df, on="product_category_name", how="left")
category_sales = merged_df["product_category_name_english"].value_counts().reset_index()
category_sales.columns = ["Kategori", "Jumlah Penjualan"]
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=category_sales.head(10), x="Jumlah Penjualan", y="Kategori", hue="Kategori", palette="viridis", legend=False, ax=ax)
ax.set_xlabel("Jumlah Penjualan")
ax.set_ylabel("Kategori Produk")
ax.set_title("10 Kategori Produk Terlaris")
ax.grid(axis='x', linestyle='--', alpha=0.7)
st.pyplot(fig)

st.subheader("Distribusi Skor Review")
review_scores = reviews_df["review_score"].value_counts().sort_index()
if selected_review != "Semua":
    review_scores = review_scores[review_scores.index == int(selected_review)]
fig, ax = plt.subplots()
sns.barplot(x=review_scores.index, y=review_scores.values, ax=ax, palette="magma")
ax.set_xlabel("Review Score")
ax.set_ylabel("Jumlah")
st.pyplot(fig)
