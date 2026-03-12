import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Bike Sharing Insights",  
    layout="wide"
)

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
st.markdown(f"Menampilkan data dari **{start_date}** sampai **{end_date}**")

col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = main_df['cnt'].sum()
    st.metric("Total Penyewaan", value=f"{total_rentals:,}")
with col2:
    avg_rentals = round(main_df['cnt'].mean(), 2)
    st.metric("Rata-rata Harian", value=avg_rentals)
with col3:
    registered_ratio = (main_df['registered'].sum() / total_rentals) * 100
    st.metric("Pengguna Terdaftar", value=f"{registered_ratio:.1f}%")

st.divider()

tab1, tab2, tab3 = st.tabs(["Pola Waktu", "Faktor Lingkungan", "Profil Pengguna"])

with tab1:
    st.subheader("Analisis Waktu: Kapan Orang Bersepeda?")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("**Tren Penyewaan per Jam (Hari Kerja vs Libur)**")
        hour_daytype = main_hour_df.groupby(['day_type', 'hr'])['cnt'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=hour_daytype, x='hr', y='cnt', hue='day_type', palette="Set2", linewidth=2.5, ax=ax)
        ax.set_title("Peak Hours Analysis")
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)
    
    with col_b:
        st.write("**Rata-rata Penyewaan per Jam (Total)**")
        hourly_mean = main_hour_df.groupby('hr')['cnt'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='hr', y='cnt', data=hourly_mean, color="skyblue", ax=ax)
        ax.set_title("Hourly Distribution")
        st.pyplot(fig)

with tab2:
    st.subheader("Pengaruh Musim & Cuaca")
    
    col_c, col_d = st.columns(2)
    
    with col_c:
        season_summary = main_df.groupby('season')['cnt'].mean().reset_index()
        fig, ax = plt.subplots()
        sns.barplot(x='season', y='cnt', data=season_summary, palette="viridis", ax=ax)
        ax.set_ylabel("Rata-rata Penyewaan")
        st.pyplot(fig)
        
    with col_d:
        weather_summary = main_df.groupby('weathersit')['cnt'].mean().reset_index()
        fig, ax = plt.subplots()
        sns.barplot(x='weathersit', y='cnt', data=weather_summary, palette="magma", ax=ax)
        ax.set_ylabel("Rata-rata Penyewaan")
        st.pyplot(fig)

with tab3:
    st.subheader("Siapa yang Menggunakan Layanan Kita?")
    
    user_total = [main_df['casual'].sum(), main_df['registered'].sum()]
    labels = ['Casual', 'Registered']
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(user_total, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff'], explode=(0.1, 0))
    ax.axis('equal') 
    st.pyplot(fig)
    
    st.info("""
    **Insight Utama:**
    - Pengguna Terdaftar adalah tulang punggung bisnis.
    - Lonjakan pada jam kerja (08:00 & 17:00) menunjukkan sepeda digunakan sebagai alat transportasi utama ke kantor.
    - Strategi promo bisa diarahkan pada pengguna Kasual di akhir pekan.
    """)

st.markdown("---")
st.caption(f"Dashboard developed by: **Kadek Aditya Gimas Tangkas Kori Agung** | Data Source: Bike Sharing Dataset")