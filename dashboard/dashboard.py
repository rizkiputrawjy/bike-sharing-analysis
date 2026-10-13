import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

file_path = os.path.join(os.path.dirname(__file__), "day.csv")
df = pd.read_csv(file_path)

st.title("Bike Sharing Analysis Dashboard")
st.write(
    """
    Dashboard ini menampilkan analisis jumlah penyewaan sepeda berdasarkan
    kondisi cuaca serta perbedaan pola penyewaan antara hari kerja dan hari libur.
    """
)

st.sidebar.header("Filter Data")

weather_option = st.sidebar.multiselect(
    "Pilih kondisi cuaca:",
    options=sorted(df["weathersit"].unique()),
    default=sorted(df["weathersit"].unique())
)

filtered_df = df[df["weathersit"].isin(weather_option)]

st.subheader("Dataset Preview")
st.dataframe(filtered_df.head())

st.subheader("Jumlah Penyewaan Berdasarkan Kondisi Cuaca")

fig, ax = plt.subplots(figsize=(8, 5))

sns.boxplot(
    data=filtered_df,
    x="weathersit",
    y="cnt",
    ax=ax
)

ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Penyewaan")

st.pyplot(fig)

st.subheader("Hari Kerja vs Hari Libur")
workingday_df = (
    filtered_df
    .groupby("workingday")["cnt"]
    .mean()
    .reset_index()
)
fig, ax = plt.subplots(figsize=(6, 4))

sns.barplot(
    data=workingday_df,
    x="workingday",
    y="cnt",
    ax=ax
)
ax.set_xlabel("Kategori Hari")
ax.set_ylabel("Rata-rata Penyewaan")

st.pyplot(fig)
st.subheader("Insight")

st.write(
    """
    - Kondisi cuaca memiliki hubungan dengan jumlah penyewaan sepeda.
    - Pengguna cenderung melakukan lebih banyak penyewaan pada kondisi cuaca yang lebih mendukung.
    - Pola penyewaan berbeda antara hari kerja dan hari libur.
    - Gunakan filter kondisi cuaca pada sidebar untuk melihat perubahan hasil visualisasi.
    """
)
