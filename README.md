# Bike Sharing Dashboard

Dashboard ini dibangun menggunakan **Streamlit** dan menampilkan analisis sederhana dari dataset Bike Sharing.

## 📦 Struktur Folder

- `dashboard/` - berisi file aplikasi Streamlit (`dashboard.py`) dan dataset (`day.csv`, `hour.csv`).
- `data/` - salinan dataset (tidak digunakan langsung oleh aplikasi saat dijalankan dari `dashboard/`).

## ✅ Prasyarat

- Python 3.10+ 
- `pip` 

## 🚀 Menjalankan Dashboard

1) **Masuk ke folder dashboard** (agar file data ditemukan secara relatif):

```powershell
cd dashboard
```

2) **Instal dependensi** (jalankan sekali saja):

```powershell
pip install -r ../requirements.txt
```

3) **Jalankan aplikasi Streamlit**:

```powershell
streamlit run dashboard.py
```

4) Buka browser apabila tidak otomatis terbuka:

```
http://localhost:8501
```

## 📝 Catatan

- Aplikasi membaca `day.csv` dan `hour.csv` dari folder tempat `dashboard.py` dijalankan. Pastikan kedua file tersebut ada di folder `dashboard/`.
- Jika kamu ingin menggunakan dataset versi lain, ganti file CSV di folder `dashboard/`.

---
