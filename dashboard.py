import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Setup tema seaborn
sns.set_theme(style="darkgrid")

# Load data
df = pd.read_csv("main_data.csv")
df['datetime'] = pd.to_datetime(df['datetime'])

# Header Dashboard
st.header('Air Quality Dashboard 🌤️')

# Sidebar
st.sidebar.title("Air Quality Analyzer")
st.sidebar.write("Dashboard ini menampilkan analisis kualitas udara dari stasiun Aotizhongxin dan Changping (2014-2015).")

# --- Visualisasi 1: Tren PM2.5 ---
st.subheader('Tren Rata-rata PM2.5 Bulanan (2014-2015)')
df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df_trend = df[df['year'].isin([2014, 2015])]
df_monthly = df_trend.groupby(['station', 'year', 'month'])['PM2.5'].mean().reset_index()
df_monthly['period'] = df_monthly['year'].astype(str) + '-' + df_monthly['month'].astype(str).str.zfill(2)

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=df_monthly, x='period', y='PM2.5', hue='station', marker='o', palette='Set1', ax=ax)
ax.set_xlabel('Tahun-Bulan')
ax.set_ylabel('Rata-rata PM2.5 (µg/m³)')
plt.xticks(rotation=45)
st.pyplot(fig)

# --- Visualisasi 2: Binning/Clustering Kualitas Udara ---
st.subheader('Proporsi Kategori Kualitas Udara (PM2.5) - Aotizhongxin 2015')
df_aoti_2015 = df[(df['station'] == 'Aotizhongxin') & (df['year'] == 2015)]
df_daily_aoti = df_aoti_2015.set_index('datetime').resample('D')['PM2.5'].mean().reset_index()

bins = [0, 35, 75, 115, 150, 250, 9999]
labels = ['Good', 'Moderate', 'Unhealthy for Sensitive', 'Unhealthy', 'Very Unhealthy', 'Hazardous']
df_daily_aoti['aqi_category'] = pd.cut(df_daily_aoti['PM2.5'], bins=bins, labels=labels)

category_counts = df_daily_aoti['aqi_category'].value_counts(normalize=True) * 100

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x=category_counts.values, y=category_counts.index, palette='rocket', ax=ax2)
ax2.set_xlabel('Persentase Hari (%)')
ax2.set_ylabel('Kategori Kualitas Udara')
st.pyplot(fig2)