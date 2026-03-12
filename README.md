# Bike Sharing Dashboard 🚲📊

Dashboard ini dibuat menggunakan **Streamlit** untuk menampilkan analisis sederhana dari dataset **Bike Sharing**.  
Aplikasi ini memvisualisasikan data penyewaan sepeda berdasarkan dataset `day.csv` dan `hour.csv`.

---

## 📁 Struktur Folder
```
project-folder/
│
├── dashboard/
│   ├── dashboard.py
│   ├── day.csv
│   └── hour.csv
│
├── data/
│   ├── day.csv
│   └── hour.csv
│
├── requirements.txt
└── README.md
```

Keterangan:
- **dashboard/** : berisi aplikasi Streamlit (`dashboard.py`) dan dataset yang digunakan saat menjalankan aplikasi.
- **data/** : salinan dataset (tidak digunakan langsung oleh aplikasi).
- **requirements.txt** : daftar library Python yang dibutuhkan.

---

# Setup Environment

## Setup Environment - Virtual Environment
```
python -m venv .venv
```

### Aktivasi Virtual Environment

**Windows (PowerShell)**
```
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```
source .venv/bin/activate
```

### Install Dependencies
```
pip install -r requirements.txt
```

---

# Run Streamlit App

Jalankan aplikasi Streamlit:

```
streamlit run dashboard/dashboard.py
```
---

## 📝 Catatan
- Aplikasi membaca dataset **`day.csv`** dan **`hour.csv`** dari folder **dashboard/**.
- Pastikan kedua file CSV tersebut berada di folder yang sama dengan **dashboard.py**.
- Jika ingin menggunakan dataset lain, cukup mengganti file CSV pada folder **dashboard/**.