import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Bike Sharing Analysis Dashboard",
    page_icon="🚲",
    layout="wide"
)

sns.set_style("white")

@st.cache_data
def load_data():
    day_df = pd.read_csv("data/day.csv")
    hour_df = pd.read_csv("data/hour.csv")

    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

    season_map = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    day_df['season_label'] = day_df['season'].map(season_map)
    hour_df['season_label'] = hour_df['season'].map(season_map)
    
    day_df['year_label'] = day_df['yr'].map({0: '2011', 1: '2012'})
    
    return day_df, hour_df

day_df, hour_df = load_data()

with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/bicycle.png")
    st.title("Filter Analisis")

    min_date = day_df['dteday'].min()
    max_date = day_df['dteday'].max()
    
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                 (day_df["dteday"] <= str(end_date))]

main_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                       (hour_df["dteday"] <= str(end_date))]

st.title("🚲 Proyek Analisis Data: Bike Sharing")
st.markdown(f"Periode Data: **{start_date}** s/d **{end_date}**")

col1, col2, col3 = st.columns(3)
with col1:
    total_rent = main_df['cnt'].sum()
    st.metric("Total Penyewaan", value=f"{total_rent:,}")
with col2:
    avg_daily = main_df['cnt'].mean()
    st.metric("Rata-rata Harian", value=f"{avg_daily:.0f}")
with col3:
    registered_pct = (main_df['registered'].sum() / total_rent) * 100
    st.metric("Persentase Pengguna Terdaftar", value=f"{registered_pct:.1f}%")

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Rata-rata Penyewaan per Musim")
    season_avg = main_df.groupby('season_label')['cnt'].mean().sort_values(ascending=False).reset_index()

    colors = ["#1f77b4" if (x == season_avg['cnt'].max()) else "#D3D3D3" for x in season_avg['cnt']]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='cnt', y='season_label', data=season_avg, palette=colors, ax=ax)
    ax.set_title("Summer Menjadi Musim Paling Populer", loc="left", fontsize=14)
    ax.set_xlabel("Rata-rata Penyewaan Harian")
    ax.set_ylabel(None)
    st.pyplot(fig)
    st.caption("Visualisasi menyoroti Musim Summer (Gugur/Panas) sebagai kontributor utama.")

with col_right:
    st.subheader("Distribusi Tipe Pengguna")
    user_data = [main_df['casual'].sum(), main_df['registered'].sum()]
    labels = ['Casual', 'Registered']
   
    fig, ax = plt.subplots(figsize=(10, 7.3))
    ax.pie(user_data, labels=labels, autopct='%1.1f%%', startangle=90, 
           colors=['#D3D3D3', '#1f77b4'], explode=(0, 0.05))
    ax.set_title("Mayoritas Pengguna Adalah Member Terdaftar", fontsize=14)
    st.pyplot(fig)

st.divider()

st.subheader("Pola Penyewaan Berdasarkan Jam (Working Day vs Holiday)")
hour_pattern = main_hour_df.groupby(['workingday', 'hr'])['cnt'].mean().reset_index()
hour_pattern['status'] = hour_pattern['workingday'].map({1: 'Hari Kerja', 0: 'Hari Libur'})

fig, ax = plt.subplots(figsize=(15, 6))

sns.lineplot(data=hour_pattern, x='hr', y='cnt', hue='status', palette=['#D3D3D3', '#1f77b4'], linewidth=3, ax=ax)

ax.axvspan(7, 9, color='orange', alpha=0.1, label='Peak Morning')
ax.axvspan(16, 18, color='orange', alpha=0.1, label='Peak Afternoon')

ax.set_title("Puncak Penyewaan Terjadi pada Jam Komuter (Berangkat & Pulang Kerja)", loc="left", fontsize=16)
ax.set_xticks(range(0, 24))
ax.set_xlabel("Jam (0-23)")
ax.set_ylabel("Rata-rata Jumlah Sepeda")
ax.legend(title="Tipe Hari")
ax.grid(axis='y', linestyle='--', alpha=0.5)

st.pyplot(fig)

st.subheader("📌 Kesimpulan Utama")
with st.expander("Lihat Detail Analisis"):
    st.markdown("""
    1.  **Prioritas Musim:** Musim **Summer** memiliki performa tertinggi. Tim operasional harus memastikan ketersediaan sepeda maksimal pada periode ini.
    2.  **Segmen Pengguna:** **81.2%** pengguna adalah pelanggan terdaftar. Fokus strategi pemasaran harus tetap pada retensi member, namun ada peluang besar untuk mengonversi pengguna kasual di akhir pekan.
    3.  **Efisiensi Logistik:** Puncak permintaan terjadi secara konsisten pada pukul **08:00** dan **17:00**. Distribusi ulang sepeda (re-balancing) ke stasiun-stasiun padat harus dilakukan sebelum jam tersebut.
    """)

st.write("\n")
st.write("---")
st.caption("Dibuat oleh: **Kadek Aditya Gimas Tangkas Kori Agung** | Proyek Analisis Data Dashboard")