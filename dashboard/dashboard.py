import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Bike Sharing Insights", 
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
    weather_map = {1: 'Clear', 2: 'Mist/Cloudy', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
    
    day_df['season'] = day_df['season'].map(season_map)
    hour_df['season'] = hour_df['season'].map(season_map)
    day_df['weathersit'] = day_df['weathersit'].map(weather_map)
    hour_df['weathersit'] = hour_df['weathersit'].map(weather_map)
    
    day_df['day_type'] = day_df['workingday'].map({1: 'Working Day', 0: 'Holiday/Weekend'})
    hour_df['day_type'] = hour_df['workingday'].map({1: 'Working Day', 0: 'Holiday/Weekend'})

    return day_df, hour_df

day_df, hour_df = load_data()

with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/bicycle.png")
    st.title("Navigation & Filter")
    
    min_date = day_df['dteday'].min()
    max_date = day_df['dteday'].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                 (day_df["dteday"] <= str(end_date))]

main_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                       (hour_df["dteday"] <= str(end_date))]

st.title("🚲 Bike Sharing Dashboard")
st.markdown(f"Periode Analisis: **{start_date}** sampai **{end_date}**")

col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = main_df['cnt'].sum()
    st.metric("Total Penyewaan", value=f"{total_rentals:,}")
with col2:
    avg_rentals = round(main_df['cnt'].mean(), 2) if not main_df.empty else 0
    st.metric("Rata-rata Harian", value=f"{avg_rentals:,}") 
with col3:
    if total_rentals > 0:
        reg_ratio = (main_df['registered'].sum() / total_rentals) * 100
    else: 
        reg_ratio = 0
    st.metric("Pengguna Terdaftar", value=f"{reg_ratio:.1f}%")

st.divider()

tab1, tab2, tab3 = st.tabs(["📊 Pola Waktu", "☁️ Faktor Lingkungan", "👥 Profil Pengguna"])

with tab1:
    st.subheader("Analisis Waktu: Kapan Orang Bersepeda?")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("**Tren Penyewaan per Jam (Hari Kerja vs Libur)**")
        hour_daytype = main_hour_df.groupby(['day_type', 'hr'])['cnt'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 6))
       
        sns.lineplot(data=hour_daytype, x='hr', y='cnt', hue='day_type', 
                     palette=['#D3D3D3', '#1f77b4'], linewidth=3, ax=ax)
       
        ax.axvspan(7, 9, color='orange', alpha=0.1)
        ax.axvspan(16, 18, color='orange', alpha=0.1)
        ax.set_title("Pola Komuter vs Pola Rekreasi", loc="left")
        ax.set_xticks(range(0, 24))
        st.pyplot(fig)
    
    with col_b:
        st.write("**Distribusi Rata-rata per Jam (Highlight Peak)**")
        hourly_mean = main_hour_df.groupby('hr')['cnt'].mean().reset_index()
        
        colors_hr = ["#1f77b4" if (x == hourly_mean['cnt'].max()) else "#D3D3D3" for x in hourly_mean['cnt']]
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='hr', y='cnt', data=hourly_mean, palette=colors_hr, ax=ax)
        ax.set_title("Identifikasi Jam Sibuk Utama", loc="left")
        st.pyplot(fig)

with tab2:
    st.subheader("Pengaruh Faktor Eksternal")
    col_c, col_d = st.columns(2)
    
    with col_c:
        st.write("**Rata-rata per Musim**")
        season_summary = main_df.groupby('season')['cnt'].mean().sort_values(ascending=False).reset_index()
       
        colors_s = ["#1f77b4" if (x == season_summary['cnt'].max()) else "#D3D3D3" for x in season_summary['cnt']]
        fig, ax = plt.subplots()
        sns.barplot(x='cnt', y='season', data=season_summary, palette=colors_s, ax=ax)
        ax.set_xlabel("Rerata Penyewaan")
        ax.set_ylabel(None)
        st.pyplot(fig)
        
    with col_d:
        st.write("**Kondisi Cuaca**")
        weather_summary = main_df.groupby('weathersit')['cnt'].mean().sort_values(ascending=False).reset_index()
       
        colors_w = ["#1f77b4" if (x == weather_summary['cnt'].max()) else "#D3D3D3" for x in weather_summary['cnt']]
        fig, ax = plt.subplots()
        sns.barplot(x='cnt', y='weathersit', data=weather_summary, palette=colors_w, ax=ax)
        ax.set_xlabel("Rerata Penyewaan")
        ax.set_ylabel(None)
        st.pyplot(fig)

with tab3:
    st.subheader("Siapa yang Menggunakan Layanan Kita?")
    col_e, col_f = st.columns([1, 1])
    
    with col_e:
        user_total = [main_df['casual'].sum(), main_df['registered'].sum()]
        labels = ['Casual', 'Registered']
        fig, ax = plt.subplots(figsize=(6, 4))

        ax.pie(user_total, labels=labels, autopct='%1.1f%%', startangle=140, 
               colors=['#D3D3D3', '#1f77b4'], explode=(0, 0.1))
        ax.axis('equal') 
        st.pyplot(fig)
    
    with col_f:
        st.info("""
        **💡 Strategic Insights:**
        1. **Integritas Data:** Warna Biru secara konsisten menunjukkan performa tertinggi atau segmen utama.
        2. **Kebutuhan Armada:** Fokus pada jam 08:00 & 17:00 (Area Oranye) karena lonjakan permintaan sangat tajam di hari kerja.
        3. **Faktor Cuaca:** Cuaca 'Clear' (Cerah) mendominasi penggunaan, namun strategi promosi saat mendung (Mist) bisa meningkatkan volume harian.
        """)

st.markdown("---")
st.caption(f"Dashboard developed by: **Kadek Aditya Gimas Tangkas Kori Agung** | Data Source: Bike Sharing Dataset")