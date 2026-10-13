import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


st.set_page_config(
    page_title="Bike Sharing Analysis Dashboard",
    layout="wide"
)


base_path = os.path.dirname(__file__)


day_df = pd.read_csv(
    os.path.join(base_path, "day.csv")
)


hour_df = pd.read_csv(
    os.path.join(base_path, "hour.csv")
)



weather_mapping = {
    1: "Cerah",
    2: "Berawan",
    3: "Hujan Ringan",
    4: "Cuaca Buruk"
}


# DAY DATA (Q1)

day_df["weather_label"] = (
    day_df["weathersit"]
    .map(weather_mapping)
)



# HOUR DATA (Q2)

hour_df["workingday_label"] = (
    hour_df["workingday"]
    .replace({
        1: "Hari Kerja",
        0: "Hari Libur"
    })
)



st.title(
    "Bike Sharing Analysis Dashboard"
)


st.write(
"""
Dashboard ini menampilkan analisis pengaruh kondisi cuaca
terhadap penyewaan sepeda serta pola penggunaan sepeda
berdasarkan waktu pada hari kerja dan hari libur.
"""
)



st.sidebar.header(
    "Filter"
)


weather_filter = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=day_df["weather_label"].unique(),
    default=day_df["weather_label"].unique()
)


working_filter = st.sidebar.multiselect(
    "Pilih Jenis Hari",
    options=hour_df["workingday_label"].unique(),
    default=hour_df["workingday_label"].unique()
)



filtered_day = day_df[
    day_df["weather_label"].isin(weather_filter)
]


filtered_hour = hour_df[
    hour_df["workingday_label"].isin(working_filter)
]



col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Penyewaan",
        f"{filtered_day['cnt'].sum():,.0f}"
    )


with col2:

    st.metric(
        "Rata-rata Penyewaan Harian",
        f"{filtered_day['cnt'].mean():,.2f}"
    )


with col3:

    best_weather = (
        filtered_day
        .groupby("weather_label")["cnt"]
        .mean()
        .idxmax()
    )

    st.metric(
        "Cuaca Terbaik",
        best_weather
    )


st.header(
    "1. Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda"
)



weather_analysis = (
    filtered_day
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

- Kondisi cuaca cerah memiliki rata-rata penyewaan tertinggi.
- Kondisi cuaca kurang mendukung berkaitan dengan penurunan jumlah penyewaan.
- Informasi cuaca dapat digunakan sebagai pertimbangan pengelolaan armada.
"""
)


st.header(
    "2. Pola Penyewaan Hari Kerja dan Hari Libur Berdasarkan Jam"
)


hour_pattern = (
    filtered_hour
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
    data=hour_pattern,
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

- Hari kerja menunjukkan dua peningkatan utama pada pagi dan sore hari.
- Pola tersebut menunjukkan karakteristik penggunaan untuk aktivitas komuter.
- Hari libur memiliki peningkatan penggunaan terutama pada periode siang hari.
"""
)
