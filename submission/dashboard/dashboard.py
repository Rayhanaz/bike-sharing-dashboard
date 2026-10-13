import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide"
)

# Path file main_data.csv dinamis (relatif terhadap tempat dashboard.py berada)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(CURRENT_DIR, "main_data.csv")


@st.cache_data
def load_data():
  df = pd.read_csv(DATA_PATH)
  df["dteday"] = pd.to_datetime(df["dteday"])
  return df


df = load_data()

# Header Dashboard
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown(
    "Dashboard interaktif untuk memantau performa dan pola penyewaan sepeda"
    " harian."
)

# Sidebar Filter
st.sidebar.header("Filter Data")
year_option = st.sidebar.selectbox(
    "Pilih Tahun:", options=["Semua Tahun", "2011", "2012"]
)
season_option = st.sidebar.multiselect(
    "Pilih Musim:",
    options=df["season_label"].unique(),
    default=df["season_label"].unique(),
)

filtered_df = df.copy()

if year_option == "2011":
  filtered_df = filtered_df[filtered_df["yr"] == 0]
elif year_option == "2012":
  filtered_df = filtered_df[filtered_df["yr"] == 1]

filtered_df = filtered_df[filtered_df["season_label"].isin(season_option)]

# Pengecekan jika user menghapus semua pilihan pada filter (mencegah ValueError / NaN)
if filtered_df.empty:
  st.warning(
      "⚠️ Tidak ada data yang sesuai dengan filter. Silakan pilih minimal satu"
      " Musim di sidebar!"
  )
else:
  # Ringkasan Metrik
  col1, col2, col3 = st.columns(3)
  col1.metric("Total Penyewaan", f"{filtered_df['cnt'].sum():,}")
  col2.metric(
      "Rata-rata Penyewaan/Hari", f"{int(filtered_df['cnt'].mean()):,} unit"
  )
  col3.metric("Hari Terdaftar", f"{len(filtered_df)} hari")

  st.divider()

  # Visualisasi 1: Bar Chart Rata-rata Penyewaan per Musim & Tipe Hari
  st.subheader("📊 Rata-rata Penyewaan Sepeda per Musim & Tipe Hari")
  fig1, ax1 = plt.subplots(figsize=(10, 4))
  sns.barplot(
      data=filtered_df,
      x="season_label",
      y="cnt",
      hue="workingday_label",
      palette="Set2",
      errorbar=None,
      ax=ax1,
  )
  ax1.set_xlabel("Musim")
  ax1.set_ylabel("Rata-rata Penyewaan Harian")
  ax1.grid(axis="y", linestyle="--", alpha=0.5)

  # Pindahkan legend ke luar grafik di sebelah kanan
  ax1.legend(
      title="Tipe Hari",
      bbox_to_anchor=(1.02, 1),
      loc="upper left",
      borderaxespad=0,
  )

  plt.tight_layout()
  st.pyplot(fig1)

  # Visualisasi 2: Boxplot Penyewaan Berdasarkan Kategori Suhu
  st.subheader("🌡️ Distribusi Penyewaan Berdasarkan Kategori Suhu")
  bins = [0, 0.3, 0.6, 1.0]
  labels = ["Dingin", "Sedang", "Panas"]
  filtered_df["temp_category"] = pd.cut(
      filtered_df["temp"], bins=bins, labels=labels
  )

  fig2, ax2 = plt.subplots(figsize=(8, 4))
  sns.boxplot(
      data=filtered_df, x="temp_category", y="cnt", palette="coolwarm", ax=ax2
  )
  ax2.set_xlabel("Kategori Suhu Udara")
  ax2.set_ylabel("Total Penyewaan Harian")
  ax2.grid(axis="y", linestyle="--", alpha=0.5)

  plt.tight_layout()
  st.pyplot(fig2)
