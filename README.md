# 🛍️ Mall Customer Segmentation Dashboard

Sebuah aplikasi web interaktif berbasis **Streamlit** yang mengelompokkan pelanggan pusat perbelanjaan (mal) menggunakan algoritma pembelajaran mesin **K-Means Clustering**. 

Aplikasi ini bertujuan untuk membantu tim pemasaran memahami karakteristik setiap pelanggan berdasarkan pendapatan tahunan (*Annual Income*) dan skor pengeluaran (*Spending Score*) mereka, sehingga strategi promosi dapat dilakukan secara lebih efektif dan tepat sasaran.

## ✨ Fitur Utama

- **Antarmuka Modern (Tabbed UI):** Desain layar lebar (*wide-layout*) yang dipisah menjadi dua bagian utama: Prediksi Pelanggan dan Dashboard Analisis.
- **Prediksi Segmen Baru:** Pengguna dapat memasukkan data pendapatan dan pengeluaran melalui *slider* dan model akan memprediksi secara instan ke dalam klaster mana pelanggan tersebut masuk.
- **Visualisasi Interaktif (Altair):** Menampilkan pemetaan keseluruhan data pelanggan dalam bentuk grafik *scatter plot* yang interaktif (mendukung fitur *hover* untuk melihat detail data). Titik pelanggan baru juga akan otomatis ditandai (X) di dalam grafik.
- **Informasi Model & Metrik:** Menampilkan metrik utama dari algoritma seperti *Silhouette Score* untuk mengevaluasi kualitas klaster secara langsung.

## 🗂️ Dataset

Dataset yang digunakan bersumber dari Kaggle: **[Customer Segmentation Tutorial in Python](https://www.kaggle.com/datasets/vjchoudhary7/customer-segmentation-tutorial-in-python/data)** (berupa file `Mall_Customers.csv`), yang berisi atribut berikut:
- **Age**: Umur pelanggan
- **Annual Income (k$)**: Pendapatan pelanggan per tahun dalam ribuan dolar.
- **Spending Score (1-100)**: Skor perilaku pengeluaran pelanggan berdasarkan riwayat belanja mereka (skala 1-100).

## 🚀 Cara Menjalankan Aplikasi

1. Pastikan Anda telah menginstal **[uv](https://github.com/astral-sh/uv)** di komputer Anda.
2. Buka terminal/command prompt dan navigasikan ke folder proyek ini.
3. Buat dan aktifkan *virtual environment* menggunakan `uv` (opsional namun disarankan):
   ```bash
   uv venv
   ```
   *(Kemudian aktifkan venv sesuai OS Anda, misalnya `\.venv\Scripts\activate` di Windows).*
4. Instal pustaka yang diperlukan dengan menjalankan perintah:
   ```bash
   uv pip install streamlit pandas scikit-learn altair
   ```
5. Jalankan aplikasi menggunakan perintah berikut:
   ```bash
   uv run streamlit run app.py
   ```
6. Aplikasi akan terbuka otomatis di browser default Anda pada alamat `http://localhost:8501`.

## 🧠 Karakteristik Segmen (5 Klaster)

- 🔹 **Kelas Menengah (Average)**: Pendapatan sedang, pengeluaran sedang.
- 💎 **Target Utama (Target)**: Pendapatan tinggi, pengeluaran tinggi (Sangat konsumtif dan royal).
- 🔥 **Suka Jajan (Careless)**: Pendapatan rendah, pengeluaran tinggi (Boros).
- 🛡️ **Super Hemat (Careful)**: Pendapatan tinggi, pengeluaran rendah (Berhati-hati dan rajin menabung).
- 📉 **Konservatif (Sensible)**: Pendapatan rendah, pengeluaran rendah (Fokus pada kebutuhan pokok).
