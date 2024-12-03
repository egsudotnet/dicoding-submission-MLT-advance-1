# -*- coding: utf-8 -*-
"""dicoding-mlt-1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OlKhUODS55QFxCaJroSpEA3sWOgfSNsW

# Impor pustaka yang diperlukan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

"""Mengimpor pustaka yang akan digunakan: pandas dan numpy untuk manipulasi data, matplotlib dan seaborn untuk visualisasi, dan beberapa modul dari sklearn untuk pengembangan dan evaluasi model.

# Memuat Data
"""

!pip install kaggle

from google.colab import files
files.upload()

import os
os.environ['KAGGLE_CONFIG_DIR'] = '/content'

!kaggle datasets download -d rishidamarla/costs-for-cancer-treatment

!unzip costs-for-cancer-treatment.zip

"""Mengunduh dataset dari Kaggle dan mengekstrak data.

# Memuat dataset dan eksplorasi awal

### Muat dataset
"""

url = 'DowloadableDataFull_2011.01.12.csv'

"""Menyimpan nama atau path dari file CSV ke dalam variabel url."""

data = pd.read_csv(url, skiprows=2)

""" Membaca file CSV dengan pandas dan menyimpannya dalam data. Parameter skiprows=2 melewati dua baris pertama, sehingga data dimulai dari baris ketiga. Ini berguna jika file CSV berisi header tambahan atau keterangan di baris awal."""

data.columns = data.iloc[0]

"""Mengambil baris pertama data yang dimuat (setelah melewati dua baris awal) dan menggunakannya sebagai nama kolom. Ini dilakukan agar nama kolom sesuai dengan data yang dimuat."""

data = data[1:]

"""Menghapus baris pertama data (yang sekarang menjadi nama kolom) dari dataset, sehingga data hanya berisi data aktual tanpa pengulangan header.

### Ubah kolom menjadi numerik
"""

data['Year'] = pd.to_numeric(data['Year'], errors='coerce')

"""- Mengonversi kolom 'Year' ke dalam tipe numerik menggunakan pd.to_numeric().
- Parameter errors='coerce' digunakan untuk menangani nilai yang tidak dapat diubah ke angka. Nilai-nilai tersebut akan diubah menjadi NaN (Not a Number), yang menandakan data tidak valid untuk keperluan numerik.
"""

data['Total Costs'] = pd.to_numeric(data['Total Costs'], errors='coerce')

"""- Sama seperti sebelumnya, namun diterapkan pada kolom 'Total Costs'.
- Kolom ini diubah ke tipe numerik agar dapat digunakan dalam operasi matematis seperti penjumlahan, rata-rata, atau analisis lainnya.
"""

print(data.head())

"""## Deskripsi Variabel

### Tampilkan nama kolom dan tipe data
"""

print("Tipe Data dan Nilai Null:\n", data.info())
print("Statistik Ringkas:\n", data.describe())

"""### Memeriksa apakah ada nilai yang hilang pada kolom-kolom dalam dataset."""

print("Pemeriksaan Missing Values:")
print(data.isnull().sum())

"""### Memeriksa apakah ada duplikasi data."""

print("\nPemeriksaan Duplikat:")
print(f"Jumlah baris duplikat: {data.duplicated().sum()}")

"""### Plot diagram batang untuk 'Cancer Site'"""

plt.figure(figsize=(12, 6))
sns.countplot(x='Cancer Site', data=data)

plt.title('Distribusi Kasus Berdasarkan Cancer Site')
plt.xlabel('Cancer Site')
plt.ylabel('Jumlah Kasus')

plt.xticks(rotation=45)

plt.show()

"""Diagram menunjukan jumlah kasus sama masning 66 kasus.

### Diagram Batang untuk Total Costs berdasarkan Cancer Site
"""

plt.figure(figsize=(12, 6))
sns.barplot(x='Cancer Site', y='Total Costs', data=data, estimator='mean')

plt.title('Rata-rata Total Costs Berdasarkan Cancer Site')
plt.xlabel('Cancer Site')
plt.ylabel('Rata-rata Total Costs')

plt.xticks(rotation=45)

plt.show()

"""diagram menunjukan biaya terbesar secara berurut yaitu all sites, other , breast, colorectal, lymphoma

### diagram batang untuk Total Costs berdasarkan Cancer Site dan Sex
"""

plt.figure(figsize=(12, 6))
sns.barplot(x='Cancer Site', y='Total Costs', hue='Sex', data=data)

plt.title('Rata-rata Total Costs Berdasarkan Cancer Site dan Sex')
plt.xlabel('Cancer Site')
plt.ylabel('Rata-rata Total Costs')

plt.xticks(rotation=45)

plt.show()

"""diagram menunjukan yang paling banyak untuk wanita yaitu breast dan yang paling banyak untuk pria yaitu prostat.

# Persiapan Data

### Menghapus simbol '%' pada kolom 'Annual Cost Increase' dan mengonversinya menjadi float
"""

data['Annual Cost Increase (applied to initial and last phases)'] = (
    data['Annual Cost Increase (applied to initial and last phases)']
    .replace('%', '', regex=True)
    .astype(float) / 100
)

"""Proses ini dilakukan untuk membersihkan dan mengonversi data dari format string ke format numerik (float). Simbol '%' dihapus agar kolom tersebut dapat dikonversi menjadi nilai float dan diubah menjadi bentuk desimal dengan membagi 10

### One-Hot Encoding untuk kolom kategorikal
"""

data_encoded = pd.get_dummies(data, columns=['Cancer Site', 'Sex', 'Age', 'Incidence and Survival Assumptions'], drop_first=True)

"""One-Hot Encoding digunakan untuk mengubah data kategorikal menjadi format numerik dengan cara membuat kolom biner (0 dan 1) untuk setiap kategori yang ada.

### Tampilkan 5 baris pertama untuk inspeksi awal
"""

print(data.head())

"""### Tentukan fitur dan target"""

fitur = data_encoded.drop(columns=['Total Costs'])  # Gantilah dengan nama kolom target jika berbeda
target = data_encoded['Total Costs']

"""Proses ini memisahkan variabel independen (fitur) dari variabel dependen (target) yang akan diprediksi.

### Pisahkan data menjadi set pelatihan dan pengujian
"""

X_train, X_test, y_train, y_test = train_test_split(fitur, target, test_size=0.2, random_state=42)

"""Data dibagi menjadi set pelatihan (80%) dan set pengujian (20%). random_state=42 digunakan untuk memastikan hasil pembagian yang konsisten di setiap eksekusi.

### Cek ukuran sampel
"""

print("Jumlah sampel pelatihan:", len(X_train))
print("Jumlah sampel pengujian:", len(X_test))

"""### Standarisasi fitur"""

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("Rata-rata X_train:", X_train.mean(axis=0))
print("Deviasi standar X_train:", X_train.std(axis=0))

"""Standarisasi dilakukan untuk menyelaraskan skala fitur-fitur dalam dataset agar memiliki distribusi yang sama (mean 0 dan standar deviasi 1).

# Pengembangan Model

### DataFrame untuk perbandingan model
"""

hasil_model = pd.DataFrame(columns=['Model', 'MSE', 'RMSE', 'R2'])

"""Membuat DataFrame kosong untuk menyimpan hasil evaluasi model.

## Random Forest Regressor

### Tahap pertama dengan parameter default
"""

rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
rmse_rf = np.sqrt(mse_rf)
r2_rf = r2_score(y_test, y_pred_rf)

"""Kode ini melatih model Random Forest Regressor dengan data pelatihan, kemudian menggunakan model tersebut untuk memprediksi target pada data uji.

### Tambahkan hasil Random Forest dengan parameter default ke dalam hasil_model
"""

hasil_model = pd.concat([hasil_model, pd.DataFrame({'Model': ['Random Forest (default)'], 'MSE': [mse_rf], 'RMSE': [rmse_rf], 'R2': [r2_rf]})], ignore_index=True)

"""Kode ini menambahkan hasil evaluasi model Random Forest ke dalam DataFrame hasil_model untuk membandingkan kinerja berbagai model.

## Linear Regression
"""

lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)
mse_lr = mean_squared_error(y_test, y_pred_lr)
rmse_lr = np.sqrt(mse_lr)
r2_lr = r2_score(y_test, y_pred_lr)

"""Kode ini melatih model Linear Regression pada data pelatihan untuk memprediksi biaya pengobatan pada data pengujian, kemudian menghitung metrik evaluasi: MSE, RMSE, dan R².

### Tambahkan hasil Linear Regression ke dalam hasil_model
"""

hasil_model = pd.concat([hasil_model, pd.DataFrame({'Model': ['Linear Regression'], 'MSE': [mse_lr], 'RMSE': [rmse_lr], 'R2': [r2_lr]})], ignore_index=True)

"""Kode ini menambahkan hasil evaluasi model Linear Regression ke dalam DataFrame hasil_model untuk membandingkan kinerja model yang berbeda.

# Evaluasi Model

### Tampilkan hasil evaluasi model
"""

print("\nHasil Evaluasi Model:\n", hasil_model)

fig, ax = plt.subplots(figsize=(10, 6))
hasil_model.set_index('Model')[['MSE', 'RMSE', 'R2']].plot(kind='bar', ax=ax)
plt.title("Perbandingan Kinerja Model")
plt.ylabel("Metrik")
plt.show()

"""Membuat visualisasi perbandingan kinerja model berdasarkan MSE, RMSE, dan R².

### Prediksi dan pengujian dengan model Linear Regression
"""

y_pred_lr_test = lr_model.predict(X_test)

"""Model Linear Regression digunakan untuk membuat prediksi berdasarkan data uji (X_test). Hasil prediksi disimpan dalam y_pred_lr_test.

### Menghitung metrik evaluasi untuk Linear Regression pada data uji
"""

mse_lr_test = mean_squared_error(y_test, y_pred_lr_test)
rmse_lr_test = np.sqrt(mse_lr_test)
r2_lr_test = r2_score(y_test, y_pred_lr_test)

"""Metrik evaluasi yang sama seperti di atas (MSE, RMSE, dan R²) dihitung untuk model Linear Regression."""

print("Model Linear Regression - Evaluasi Set Pengujian")
print(f"MSE: {mse_lr_test:.2f}")
print(f"RMSE: {rmse_lr_test:.2f}")
print(f"R²: {r2_lr_test:.2f}")
print("\n")

"""### Prediksi dan pengujian dengan model Random Forest Regressor"""

y_pred_rf_test = rf_model.predict(X_test)

"""Model Random Forest Regressor digunakan untuk membuat prediksi berdasarkan data uji (X_test). Hasil prediksi disimpan dalam y_pred_rf_test.

### Menghitung metrik evaluasi untuk Random Forest pada data uji
"""

mse_rf_test = mean_squared_error(y_test, y_pred_rf_test)
rmse_rf_test = np.sqrt(mse_rf_test)
r2_rf_test = r2_score(y_test, y_pred_rf_test)

"""Metrik evaluasi yang sama seperti di atas (MSE, RMSE, dan R²) dihitung untuk model Random Forest Regressor."""

print("Model Random Forest - Evaluasi Set Pengujian")
print(f"MSE: {mse_rf_test:.2f}")
print(f"RMSE: {rmse_rf_test:.2f}")
print(f"R²: {r2_rf_test:.2f}")