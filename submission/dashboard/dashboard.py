import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Dashboard interaktif untuk memantau performa dan pola penyewaan sepeda harian.")

# Sidebar Filter
st.sidebar.header("Filter Data")
year_option = st.sidebar.selectbox("Pilih Tahun:", options=["Semua Tahun", "2011", "2012"])
season_option = st.sidebar.multiselect("Pilih Musim:", options=df['season_label'].unique(), default=df['season_label'].unique())

filtered_df = df.copy()

if year_option == "2011":
    filtered_df = filtered_df[filtered_df['yr'] == 0]
elif year_option == "2012":
    filtered_df = filtered_df[filtered_df['yr'] == 1]

filtered_df = filtered_df[filtered_df['season_label'].isin(season_option)]

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", f"{filtered_df['cnt'].sum():,}")
col2.metric("Rata-rata Penyewaan/Hari", f"{int(filtered_df['cnt'].mean()):,} unit")
col3.metric("Hari Terdaftar", f"{len(filtered_df)} hari")

st.divider()

# Charts
st.subheader("📊 Rata-rata Penyewaan Sepeda per Musim & Tipe Hari")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.barplot(
    data=filtered_df,
    x='season_label',
    y='cnt',
    hue='workingday_label',
    palette='Set2',
    errorbar=None,
    ax=ax1
)
ax1.set_xlabel("Musim")
ax1.set_ylabel("Rata-rata Penyewaan Harian")
ax1.grid(axis='y', linestyle='--', alpha=0.5)
st.pyplot(fig1)

st.subheader("🌡️ Distribusi Penyewaan Berdasarkan Kategori Suhu")
bins = [0, 0.3, 0.6, 1.0]
labels = ['Dingin', 'Sedang', 'Panas']
filtered_df['temp_category'] = pd.cut(filtered_df['temp'], bins=bins, labels=labels)

fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.boxplot(
    data=filtered_df,
    x='temp_category',
    y='cnt',
    palette='coolwarm',
    ax=ax2
)
ax2.set_xlabel("Kategori Suhu Udara")
ax2.set_ylabel("Total Penyewaan Harian")
ax2.grid(axis='y', linestyle='--', alpha=0.5)
st.pyplot(fig2)
