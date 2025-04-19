import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime

# all_df = pd.read_csv('all_data.csv')
all_df = pd.read_csv("your_data.csv.gz", compression="gzip")
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])
all_df['year_month'] = all_df['order_purchase_timestamp'].dt.to_period('M').astype(str)

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
st.title("📦 E-Commerce Data Dashboard")

min_date = all_df['order_purchase_timestamp'].min()
max_date = all_df['order_purchase_timestamp'].max()

with st.sidebar:
    st.image("e-commerce logo.jpg", width=300)
    st.markdown("### 📅 Atur Tanggal")

    start_date, end_date = st.date_input(
        label='Rentang Tanggal', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered_df = all_df[
    (all_df['order_purchase_timestamp'] >= start_date) &
    (all_df['order_purchase_timestamp'] <= end_date)
]

def plot_daily_orders(df):
    daily_orders = df.groupby(df['order_purchase_timestamp'].dt.date)['order_id'].count().reset_index()
    daily_orders.columns = ['date', 'order_count']

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=daily_orders, x='date', y='order_count', ax=ax)
    ax.set_title("Jumlah Pesanan per Hari")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Pesanan")
    return fig

def plot_order_detail(df):
    order_detail_df = df.copy()
    order_detail_df['date'] = order_detail_df['order_purchase_timestamp'].dt.date

    order_summary = order_detail_df.groupby(['date', 'product_category_name_english']).size().reset_index(name='order_count')
    return order_summary.sort_values(['date', 'order_count'], ascending=[False, False])

def plot_top_categories(df):
    top_categories = df['product_category_name_english'].value_counts().head(5).reset_index()
    top_categories.columns = ['Kategori Produk', 'Jumlah Pesanan']
    return top_categories

def plot_monthly_sales(df):
    monthly_sales = (
        df.groupby(df['order_purchase_timestamp'].dt.to_period('M'))
        .agg(order_count=('order_id', 'count'))
        .reset_index()
        .rename(columns={'order_purchase_timestamp': 'month_year'})
    )

    monthly_sales['month_year'] = monthly_sales['month_year'].astype(str)

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(data=monthly_sales, x='month_year', y='order_count', ax=ax)
    ax.set_title("Penjualan per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pesanan")
    plt.xticks(rotation=45)
    return fig

def plot_payment_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df, x="payment_type", y="payment_value", ax=ax)
    ax.set_title("Nilai Transaksi per Metode Pembayaran")
    ax.set_xlabel("Metode Pembayaran")
    ax.set_ylabel("Nilai Transaksi")
    return fig

def plot_installments_vs_value(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=df, x='payment_installments', y='payment_value', hue='payment_type', ax=ax)
    ax.set_title("Hubungan Jumlah Cicilan dan Nilai Transaksi")
    ax.set_xlabel("Jumlah Cicilan")
    ax.set_ylabel("Nilai Transaksi")
    return fig

def plot_product_description_sales(df):
    sales_analysis = df.groupby("product_id").agg(
        total_sales=('order_id', 'size'),
        product_photos_qty=('product_photos_qty', 'first'),
        product_description_lenght=('product_description_lenght', 'first')
    ).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=sales_analysis,
        x='product_description_lenght',
        y='total_sales',
        size='product_photos_qty',
        hue='product_photos_qty',
        palette='coolwarm',
        sizes=(20, 200),
        alpha=0.7,
        edgecolor='w',
        ax=ax
    )
    ax.set_title('Panjang Deskripsi & Jumlah Foto terhadap Total Penjualan')
    ax.set_xlabel('Panjang Deskripsi Produk')
    ax.set_ylabel('Total Penjualan')
    return fig

st.subheader("📈 Jumlah Pesanan Harian")
st.pyplot(plot_daily_orders(filtered_df))

st.markdown("### 🗓️ Rincian Order per Hari")
order_summary = plot_order_detail(filtered_df)
order_summary.columns = ['Tanggal', 'Kategori Produk', 'Jumlah Pesanan']
st.dataframe(order_summary)

st.subheader("🏆 Kategori Produk Terlaris")
st.table(plot_top_categories(filtered_df))

st.subheader("📅 Penjualan per Bulan")
st.pyplot(plot_monthly_sales(filtered_df))

st.subheader("💳 Distribusi Metode Pembayaran")
st.pyplot(plot_payment_distribution(filtered_df))

st.subheader("📊 Cicilan dan Nilai Transaksi")
st.pyplot(plot_installments_vs_value(filtered_df))

st.subheader("🖼️ Pengaruh Foto dan Deskripsi Produk")
st.pyplot(plot_product_description_sales(filtered_df))

st.caption('Copyright (c) Sirly Ziadatul Mustafidah 2025')
