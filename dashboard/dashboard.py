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
    hour_df['year_label'] = hour_df['yr'].map({0: '2011', 1: '2012'})
    
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

    year_options = day_df['year_label'].unique()
    selected_years = st.multiselect("Pilih Tahun", options=year_options, default=year_options)

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                 (day_df["dteday"] <= str(end_date)) &
                 (day_df["year_label"].isin(selected_years))]

main_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                       (hour_df["dteday"] <= str(end_date)) &
                       (hour_df["year_label"].isin(selected_years))]

st.title("🚲 Proyek Analisis Data: Bike Sharing")
st.markdown(f"Periode Data: **{start_date}** s/d **{end_date}**")

col1, col2, col3 = st.columns(3)
with col1:
    total_rent = main_df['cnt'].sum()
    st.metric("Total Penyewaan", value=f"{total_rent:,}")
with col2:
    avg_daily = main_df['cnt'].mean()
    st.metric("Rata-rata Harian", value=f"{avg_daily:.0f}" if not pd.isna(avg_daily) else "0")
with col3:
    if total_rent > 0:
        registered_pct = (main_df['registered'].sum() / total_rent) * 100
    else:
        registered_pct = 0
    st.metric("Persentase Pengguna Terdaftar", value=f"{registered_pct:.1f}%")

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Pertumbuhan Penyewaan per Tahun")
    yearly_avg = main_df.groupby('year_label')['cnt'].mean().reset_index()
    colors_yr = ["#1f77b4" if (x == yearly_avg['cnt'].max()) else "#D3D3D3" for x in yearly_avg['cnt']]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='year_label', y='cnt', data=yearly_avg, palette=colors_yr, ax=ax)
    ax.set_title("Rata-rata Penyewaan Harian: 2011 vs 2012", loc="left")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_xlabel(None)
    st.pyplot(fig)

with col_b:
    st.subheader("Rata-rata Penyewaan per Musim")
    season_avg = main_df.groupby('season_label')['cnt'].mean().sort_values(ascending=False).reset_index()
    colors_sn = ["#1f77b4" if (x == season_avg['cnt'].max()) else "#D3D3D3" for x in season_avg['cnt']]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='cnt', y='season_label', data=season_avg, palette=colors_sn, ax=ax)
    ax.set_title("Summer Memiliki Performa Tertinggi", loc="left")
    ax.set_xlabel("Rata-rata Penyewaan Harian")
    ax.set_ylabel(None)
    st.pyplot(fig)

st.divider()

col_c, col_d = st.columns([1, 2])

with col_c:
    st.subheader("Profil Pengguna")
    user_data = [main_df['casual'].sum(), main_df['registered'].sum()]
    labels = ['Casual', 'Registered']
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(user_data, labels=labels, autopct='%1.1f%%', startangle=90, 
           colors=['#D3D3D3', '#1f77b4'], explode=(0, 0.05))
    ax.set_title("Dominasi Pengguna Terdaftar", fontsize=14)
    st.pyplot(fig)

with col_d:
    st.subheader("Pola Jam Sibuk (Working Day vs Holiday)")
    hour_pattern = main_hour_df.groupby(['workingday', 'hr'])['cnt'].mean().reset_index()
    hour_pattern['status'] = hour_pattern['workingday'].map({1: 'Hari Kerja', 0: 'Hari Libur'})

    fig, ax = plt.subplots(figsize=(12, 6.5))
    sns.lineplot(data=hour_pattern, x='hr', y='cnt', hue='status', palette=['#D3D3D3', '#1f77b4'], linewidth=3, ax=ax)
    
    ax.axvspan(7, 9, color='orange', alpha=0.1, label='Peak Morning')
    ax.axvspan(16, 18, color='orange', alpha=0.1, label='Peak Afternoon')
    
    ax.set_title("Tren Komuter pada Jam Berangkat & Pulang Kerja", loc="left")
    ax.set_xticks(range(0, 24))
    ax.set_xlabel("Jam (0-23)")
    ax.set_ylabel("Rerata Penyewaan")
    ax.legend(title="Tipe Hari", loc='upper left')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    st.pyplot(fig)

st.subheader("📌 Kesimpulan Utama")
with st.expander("Klik untuk melihat detail analisis"):
    st.markdown("""
    1.  **Analisis Pertumbuhan:** Tahun 2012 menunjukkan peningkatan signifikan dibandingkan 2011, mengindikasikan ekspansi pasar yang sukses.
    2.  **Faktor Musim:** Musim **Summer** secara konsisten menjadi puncak penyewaan. Strategi perawatan armada sebaiknya ditingkatkan pada musim Winter untuk mempersiapkan lonjakan di Spring dan Summer.
    3.  **Target Market:** Dengan **81.2%** pengguna terdaftar, program loyalitas pelanggan menjadi kunci. Namun, promosi khusus pada hari libur dapat menyasar pengguna **Casual** yang memiliki pola rekreasi di siang hari.
    4.  **Optimasi Operasional:** Adanya *Peak Hours* pada jam 08:00 dan 17:00 mengisyaratkan bahwa sepeda harus tersedia dalam jumlah maksimal di titik-titik transportasi publik pada jam-jam tersebut.
    """)

st.write("\n")
st.write("---")
st.caption("Dibuat oleh: **Kadek Aditya Gimas Tangkas Kori Agung** | Proyek Analisis Data Dashboard")