import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


st.set_page_config(
    page_title="Bike Sharing Analysis Dashboard",
    layout="wide"
)


file_path = os.path.join(
    os.path.dirname(__file__),
    "main_data.csv"
)

df = pd.read_csv(file_path)


weather_mapping = {
    1: "Cerah",
    2: "Berawan",
    3: "Hujan Ringan",
    4: "Cuaca Buruk"
}


df["weather_label"] = (
    df["weathersit"]
    .map(weather_mapping)
)


df["workingday_label"] = (
    df["workingday"]
    .replace({
        1: "Hari Kerja",
        0: "Hari Libur"
    })
)



st.title("Bike Sharing Analysis Dashboard")


st.write(
"""
Dashboard ini menampilkan analisis penyewaan sepeda berdasarkan
kondisi cuaca serta pola penggunaan berdasarkan waktu antara
hari kerja dan hari libur.
"""
)



st.sidebar.header("Filter")


weather_filter = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=df["weather_label"].unique(),
    default=df["weather_label"].unique()
)


workingday_filter = st.sidebar.multiselect(
    "Pilih Jenis Hari",
    options=df["workingday_label"].unique(),
    default=df["workingday_label"].unique()
)



filtered_df = df[
    (df["weather_label"].isin(weather_filter)) &
    (df["workingday_label"].isin(workingday_filter))
]



col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Total Penyewaan",
        f"{filtered_df['cnt'].sum():,.0f}"
    )


with col2:
    st.metric(
        "Rata-rata Penyewaan",
        f"{filtered_df['cnt'].mean():,.2f}"
    )


with col3:

    best_weather = (
        filtered_df
        .groupby("weather_label")["cnt"]
        .mean()
        .idxmax()
    )

    st.metric(
        "Cuaca dengan Penyewaan Tertinggi",
        best_weather
    )



st.header(
    "1. Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda"
)


weather_analysis = (
    filtered_df
    .groupby("weather_label")["cnt"]
    .mean()
    .reset_index()
)



fig, ax = plt.subplots(
    figsize=(8,5)
)


sns.barplot(
    data=weather_analysis,
    x="weather_label",
    y="cnt",
    ax=ax
)


ax.set_title(
    "Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca"
)

ax.set_xlabel(
    "Kondisi Cuaca"
)

ax.set_ylabel(
    "Rata-rata Penyewaan"
)


st.pyplot(fig)



st.write(
"""
**Insight:**

- Kondisi cuaca cerah memiliki rata-rata jumlah penyewaan tertinggi.
- Kondisi cuaca kurang mendukung menunjukkan penurunan aktivitas penyewaan.
- Informasi cuaca dapat digunakan untuk membantu pengelolaan armada.
"""
)


st.header(
    "2. Pola Penyewaan Hari Kerja dan Hari Libur Berdasarkan Jam"
)



hour_analysis = (
    filtered_df
    .groupby(
        [
            "hr",
            "workingday_label"
        ]
    )["cnt"]
    .mean()
    .reset_index()
)



fig, ax = plt.subplots(
    figsize=(12,6)
)


sns.lineplot(
    data=hour_analysis,
    x="hr",
    y="cnt",
    hue="workingday_label",
    marker="o",
    ax=ax
)


ax.set_title(
    "Pola Rata-rata Penyewaan Berdasarkan Jam"
)

ax.set_xlabel(
    "Jam (0-23)"
)

ax.set_ylabel(
    "Rata-rata Penyewaan"
)


ax.set_xticks(
    range(0,24)
)


ax.grid(True)


st.pyplot(fig)



st.write(
"""
**Insight:**

- Hari kerja menunjukkan peningkatan penyewaan pada jam sibuk pagi dan sore.
- Pola tersebut menunjukkan karakteristik penggunaan untuk aktivitas komuter.
- Hari libur memiliki pola penggunaan lebih stabil dengan peningkatan pada periode siang hari.
"""
)