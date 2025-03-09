import os
import pandas as pd
import streamlit as st


# Load data
orders_df = pd.read_csv("order_sharing_data.csv")
payments_df = pd.read_csv("payments_sharing_data.csv")
product_category_df = pd.read_csv("product_category_sharing_data.csv")
products_df = pd.read_csv("products_sharing_data.csv")
reviews_df = pd.read_csv("reviews_sharing_data.csv")
order_items_df = pd.read_csv("order_sharing_data.csv")

# Calculate total sales
total_sales = orders_df["price"].sum()

# Menghitung distribusi metode pembayaran
payment_distribution = payments_df["payment_type"].value_counts().reset_index()
payment_distribution.columns = ["Metode Pembayaran", "Jumlah Transaksi"]

# Merge order_items with products and categories for Top Categories
merged_df = order_items_df.merge(products_df, on="product_id", how="left")
merged_df = merged_df.merge(product_category_df, on="product_category_name", how="left")
category_sales = merged_df["product_category_name_english"].value_counts().reset_index()
category_sales.columns = ["Kategori", "Jumlah Penjualan"]

# Count review scores
review_scores = reviews_df["review_score"].value_counts().sort_index()

# Streamlit Sidebar
st.sidebar.title("E-commerce Dashboard")
page = st.sidebar.radio("Select a section:", ["Overview", "Payment Methods", "Top Categories", "Review Scores"])

st.sidebar.markdown("### Metrics")
st.sidebar.metric(label="Total Sales", value=f"${total_sales:,.2f}")

# Streamlit Main Content
st.title("E-commerce Dashboard")

if page == "Overview":
    st.subheader("Total Sales")
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")

elif page == "Payment Methods":
    st.subheader("Distribusi Metode Pembayaran yang Digunakan Pelanggan")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=payment_distribution, x="Jumlah Transaksi", y="Metode Pembayaran", hue="Metode Pembayaran", palette="coolwarm", legend=False, ax=ax)
    ax.set_xlabel("Jumlah Transaksi", fontsize=12)
    ax.set_ylabel("Metode Pembayaran", fontsize=12)
    ax.set_title("Distribusi Metode Pembayaran yang Digunakan Pelanggan", fontsize=14)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    st.pyplot(fig)

elif page == "Top Categories":
    st.subheader("10 Kategori Produk Terlaris")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=category_sales.head(10), x="Jumlah Penjualan", y="Kategori", hue="Kategori", palette="viridis", legend=False, ax=ax)
    ax.set_xlabel("Jumlah Penjualan", fontsize=12)
    ax.set_ylabel("Kategori Produk", fontsize=12)
    ax.set_title("10 Kategori Produk Terlaris", fontsize=14)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    st.pyplot(fig)

elif page == "Review Scores":
    st.subheader("Review Score Distribution")
    fig, ax = plt.subplots()
    sns.barplot(x=review_scores.index, y=review_scores.values, ax=ax, palette="magma")
    ax.set_xlabel("Review Score")
    ax.set_ylabel("Count")
    st.pyplot(fig)
