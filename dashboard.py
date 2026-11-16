import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Setup tema seaborn
sns.set_theme(style="darkgrid")

# Load data
df = pd.read_csv("main_data.csv")
df['datetime'] = pd.to_datetime(df['datetime'])

# Menyiapkan rentang tanggal untuk filter
min_date = df["datetime"].min().date()
max_date = df["datetime"].max().date()

# --- SIDEBAR (Fitur Interaktif 1) ---
with st.sidebar:
    st.title("Air Quality Analyzer")
    st.write("Gunakan filter di bawah ini untuk mengeksplorasi data.")
    
    # Menambahkan Date Input
    try:
        start_date, end_date = st.date_input(
            label='Pilih Rentang Waktu:',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
    except ValueError:
        st.error("Silakan pilih rentang tanggal yang lengkap (Tanggal Mulai dan Tanggal Selesai).")
        st.stop()

# Filter data utama berdasarkan rentang waktu yang dipilih
main_df = df[(df["datetime"].dt.date >= start_date) & 
             (df["datetime"].dt.date <= end_date)]

# --- HEADER ---
st.header('Air Quality Dashboard 🌤️')
st.write("Dashboard ini menampilkan analisis kualitas udara dari stasiun pengamatan berdasarkan rentang waktu yang Anda pilih.")

# --- VISUALISASI 1: Tren PM2.5 ---
st.subheader('Tren Rata-rata PM2.5 Bulanan')

main_df['year'] = main_df['datetime'].dt.year
main_df['month'] = main_df['datetime'].dt.month
df_monthly = main_df.groupby(['station', 'year', 'month'])['PM2.5'].mean().reset_index()
df_monthly['period'] = df_monthly['year'].astype(str) + '-' + df_monthly['month'].astype(str).str.zfill(2)

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=df_monthly, x='period', y='PM2.5', hue='station', marker='o', palette='Set1', ax=ax)
ax.set_xlabel('Tahun-Bulan')
ax.set_ylabel('Rata-rata PM2.5 (µg/m³)')
plt.xticks(rotation=45)
st.pyplot(fig)

# --- VISUALISASI 2: Binning/Clustering Kualitas Udara ---
st.subheader('Proporsi Kategori Kualitas Udara (PM2.5)')

# Resample ke harian berdasarkan data yang sudah difilter
main_df['date'] = main_df['datetime'].dt.date
df_daily = main_df.groupby(['station', 'date'])['PM2.5'].mean().reset_index()

bins = [0, 35, 75, 115, 150, 250, 9999]
labels = ['Good', 'Moderate', 'Unhealthy for Sensitive', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
df_daily['aqi_category'] = pd.cut(df_daily['PM2.5'], bins=bins, labels=labels)

# --- Fitur Interaktif 2: Selectbox untuk Stasiun ---
selected_station = st.selectbox(
    label="Pilih Stasiun untuk melihat Kategori Kualitas Udara:",
    options=df_daily['station'].unique()
)

# Filter by station
df_daily_station = df_daily[df_daily['station'] == selected_station]
category_counts = df_daily_station['aqi_category'].value_counts(normalize=True) * 100

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x=category_counts.values, y=category_counts.index, palette='rocket', ax=ax2)
ax2.set_xlabel('Persentase Hari (%)')
ax2.set_ylabel('Kategori Kualitas Udara')
ax2.set_title(f"Proporsi Kategori AQI di {selected_station}")
st.pyplot(fig2)
