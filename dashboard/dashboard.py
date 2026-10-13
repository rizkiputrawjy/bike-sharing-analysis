import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

file_path = os.path.join(os.path.dirname(__file__), "day.csv")

df = pd.read_csv(file_path)

st.title("Bike Sharing Analysis Dashboard")

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Jumlah Penyewaan Berdasarkan Cuaca")

fig, ax = plt.subplots(figsize=(8,5))

sns.boxplot(
    data=df,
    x="weathersit",
    y="cnt",
    ax=ax
)

ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Penyewaan")

st.pyplot(fig)

st.subheader("Hari Kerja vs Hari Libur")

workingday_df = df.groupby("workingday")["cnt"].mean().reset_index()


fig, ax = plt.subplots(figsize=(6,4))

sns.barplot(
    data=workingday_df,
    x="workingday",
    y="cnt",
    ax=ax
)

ax.set_xlabel("Kategori Hari")
ax.set_ylabel("Rata-rata Penyewaan")

st.pyplot(fig)


st.write("""
### Insight

- Kondisi cuaca memengaruhi jumlah penyewaan sepeda.
- Pola penyewaan berbeda antara hari kerja dan hari libur.
""")
