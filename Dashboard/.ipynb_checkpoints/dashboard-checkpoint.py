import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.header('Data Analysis Project: E-Commerce Public Dataset')

# Import data
df_all = pd.read_csv('df_all_processed.csv')

# Tambahkan input rentang tanggal
min_date = pd.to_datetime(df_all['order_purchase_timestamp']).min().date()
max_date = pd.to_datetime(df_all['order_purchase_timestamp']).max().date()

default_date = min_date + (max_date - min_date) // 2

start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=default_date)
end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_df = df_all[(df_all['order_purchase_timestamp'] >= str(start_date)) & (df_all['order_purchase_timestamp'] <= str(end_date))]

# Konversi kolom order_purchase_timestamp menjadi datetime
filtered_df['order_purchase_timestamp'] = pd.to_datetime(filtered_df['order_purchase_timestamp'])

# Visualisasi untuk tren penjualan di Olist
st.header('Data Visualization & Explanatory Analysis')
st.subheader('Perkembangan tren penjualan di Olist')

# Plot total pesanan bulanan
fig, ax = plt.subplots(figsize=(12, 6))
monthly_orders = filtered_df.groupby(filtered_df['order_purchase_timestamp'].dt.to_period('M')).size()
monthly_orders.index = monthly_orders.index.to_timestamp()  # Konversi indeks ke tipe data datetime
sns.lineplot(data=monthly_orders, marker='o', linestyle='-')
plt.title('Total Pesanan Bulanan')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Pesanan')
plt.xticks(rotation=45)
st.pyplot(fig)

# Plot total pesanan tahunan
fig, ax = plt.subplots(figsize=(12, 6))
yearly_orders = filtered_df.groupby(filtered_df['order_purchase_timestamp'].dt.to_period('Y')).size()
yearly_orders.index = yearly_orders.index.to_timestamp()  # Konversi indeks ke tipe data datetime
sns.lineplot(data=yearly_orders, marker='o', linestyle='-')
plt.title('Total Pesanan Tahunan')
plt.xlabel('Tahun')
plt.ylabel('Jumlah Pesanan')
st.pyplot(fig)

# Plot penjualan bulanan
fig, ax = plt.subplots(figsize=(12, 6))
monthly_sales = filtered_df.groupby(filtered_df['order_purchase_timestamp'].dt.to_period('M'))['price'].sum()
sns.lineplot(x=monthly_sales.index.astype(str), y=monthly_sales.values, marker='o', linestyle='-')
plt.title('Total Penjualan Bulanan (BRL)')
plt.xlabel('Bulan')
plt.ylabel('Total Penjualan')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(fig)

# Plot penjualan tahunan
fig, ax = plt.subplots(figsize=(12, 6))
yearly_sales = filtered_df.groupby(filtered_df['order_purchase_timestamp'].dt.to_period('Y'))['price'].sum()
sns.lineplot(x=yearly_sales.index.astype(str), y=yearly_sales.values, marker='o', linestyle='-')
plt.title('Total Penjualan Tahunan (BRL)')
plt.xlabel('Tahun')
plt.ylabel('Total Penjualan')
plt.grid(True)
st.pyplot(fig)

# Visualisasi untuk kategori produk dengan penjualan terbanyak
st.subheader('Kategori produk yang memiliki penjualan terbanyak')

# Membuat DataFrame untuk total penjualan semua kategori
category_sales_df = filtered_df.groupby('product_category_name')['price'].sum().reset_index()
category_sales_df.columns = ['product_category_name', 'total_sales']

# Memilih hanya 5 kategori teratas
top_5_categories_df = category_sales_df.nlargest(5, 'total_sales')

# Plot bar total penjualan untuk semua kategori
fig = px.bar(category_sales_df, x='product_category_name', y='total_sales', 
             title='Total Penjualan untuk Seluruh Kategori Produk',
             labels={'product_category_name': 'Kategori Produk', 'total_sales': 'Total Penjualan'})
st.plotly_chart(fig)

# Plot bar total penjualan untuk 5 kategori teratas
fig = px.bar(top_5_categories_df, x='product_category_name', y='total_sales', 
             title='Total Penjualan untuk 5 Kategori Teratas',
             labels={'product_category_name': 'Kategori Produk', 'total_sales': 'Total Penjualan'})
st.plotly_chart(fig)
