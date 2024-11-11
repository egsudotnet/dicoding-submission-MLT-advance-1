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

"""# Memuat Data"""

!pip install kaggle

from google.colab import files
files.upload()

import os
os.environ['KAGGLE_CONFIG_DIR'] = '/content'

!kaggle datasets download -d rishidamarla/costs-for-cancer-treatment

!unzip costs-for-cancer-treatment.zip

"""# Memuat dataset dan eksplorasi awal

###Muat dataset
"""

url = 'DowloadableDataFull_2011.01.12.csv'
data = pd.read_csv(url, skiprows=2)
data.columns = data.iloc[0]
data = data[1:]

"""###Ubah kolom menjadi numerik"""

data['Year'] = pd.to_numeric(data['Year'], errors='coerce')
data['Total Costs'] = pd.to_numeric(data['Total Costs'], errors='coerce')

"""Tampilkan 5 baris pertama untuk inspeksi awal"""

print(data.head())

"""## Deskripsi Variabel

### Tampilkan nama kolom dan tipe data
"""

print("Tipe Data dan Nilai Null:\n", data.info())
print("Statistik Ringkas:\n", data.describe())

"""###Plot diagram batang untuk 'Cancer Site'"""

plt.figure(figsize=(12, 6))
sns.countplot(x='Cancer Site', data=data)

plt.title('Distribusi Kasus Berdasarkan Cancer Site')
plt.xlabel('Cancer Site')
plt.ylabel('Jumlah Kasus')

plt.xticks(rotation=45)

plt.show()

"""###Diagram Batang untuk Total Costs berdasarkan Cancer Site"""

plt.figure(figsize=(12, 6))
sns.barplot(x='Cancer Site', y='Total Costs', data=data, estimator='mean')

plt.title('Rata-rata Total Costs Berdasarkan Cancer Site')
plt.xlabel('Cancer Site')
plt.ylabel('Rata-rata Total Costs')

plt.xticks(rotation=45)

plt.show()

"""###diagram batang untuk Total Costs berdasarkan Cancer Site dan Sex"""

plt.figure(figsize=(12, 6))
sns.barplot(x='Cancer Site', y='Total Costs', hue='Sex', data=data)

plt.title('Rata-rata Total Costs Berdasarkan Cancer Site dan Sex')
plt.xlabel('Cancer Site')
plt.ylabel('Rata-rata Total Costs')

plt.xticks(rotation=45)

plt.show()

"""# Persiapan Data

###Menghapus simbol '%' pada kolom 'Annual Cost Increase' dan mengonversinya menjadi float
"""

data['Annual Cost Increase (applied to initial and last phases)'] = (
    data['Annual Cost Increase (applied to initial and last phases)']
    .replace('%', '', regex=True)
    .astype(float) / 100
)

"""###One-Hot Encoding untuk kolom kategorikal"""

data_encoded = pd.get_dummies(data, columns=['Cancer Site', 'Sex', 'Age', 'Incidence and Survival Assumptions'], drop_first=True)

"""###Tampilkan 5 baris pertama untuk inspeksi awal"""

print(data.head())

"""###Tentukan fitur dan target"""

fitur = data_encoded.drop(columns=['Total Costs'])  # Gantilah dengan nama kolom target jika berbeda
target = data_encoded['Total Costs']

"""###Pisahkan data menjadi set pelatihan dan pengujian"""

X_train, X_test, y_train, y_test = train_test_split(fitur, target, test_size=0.2, random_state=42)

"""###Cek ukuran sampel"""

print("Jumlah sampel pelatihan:", len(X_train))
print("Jumlah sampel pengujian:", len(X_test))

"""###Standarisasi fitur"""

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("Rata-rata X_train:", X_train.mean(axis=0))
print("Deviasi standar X_train:", X_train.std(axis=0))

"""# Pengembangan Model

###DataFrame untuk perbandingan model
"""

hasil_model = pd.DataFrame(columns=['Model', 'MSE', 'RMSE', 'R2'])

"""##Random Forest Regressor

###Tahap pertama dengan parameter default
"""

rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
rmse_rf = np.sqrt(mse_rf)
r2_rf = r2_score(y_test, y_pred_rf)

"""### Tambahkan hasil Random Forest dengan parameter default ke dalam hasil_model"""

hasil_model = pd.concat([hasil_model, pd.DataFrame({'Model': ['Random Forest (default)'], 'MSE': [mse_rf], 'RMSE': [rmse_rf], 'R2': [r2_rf]})], ignore_index=True)

"""###Hyperparameter Tuning yang lebih cepat untuk Random Forest"""

param_grid_quick = {
    'n_estimators': [100, 150],  # Mengurangi jumlah opsi untuk n_estimators
    'max_depth': [10, 20, None],  # Membatasi kedalaman pohon
    'min_samples_split': [2, 5],  # Mengurangi jumlah opsi untuk pembagian
    'min_samples_leaf': [1, 2]    # Mengurangi jumlah opsi untuk jumlah sampel minimum di daun
}
grid_search_rf_quick = GridSearchCV(
    estimator=RandomForestRegressor(random_state=42),
    param_grid=param_grid_quick,
    cv=2,  # Mengurangi jumlah lipatan untuk mempercepat
    scoring='neg_mean_squared_error',
    verbose=1,  # Mengurangi level verbosity
    n_jobs=-1
)
grid_search_rf_quick.fit(X_train, y_train)

"""###Model terbaik setelah tuning cepat"""

best_rf_model_quick = grid_search_rf_quick.best_estimator_
y_pred_rf_quick = best_rf_model_quick.predict(X_test)
mse_rf_quick = mean_squared_error(y_test, y_pred_rf_quick)
rmse_rf_quick = np.sqrt(mse_rf_quick)
r2_rf_quick = r2_score(y_test, y_pred_rf_quick)

print("Hasil Hyperparameter Tuning Cepat untuk Random Forest:")
print(f"MSE: {mse_rf_quick:.2f}")
print(f"RMSE: {rmse_rf_quick:.2f}")
print(f"R²: {r2_rf_quick:.2f}")

"""## Linear Regression"""

lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)
mse_lr = mean_squared_error(y_test, y_pred_lr)
rmse_lr = np.sqrt(mse_lr)
r2_lr = r2_score(y_test, y_pred_lr)

"""###Tambahkan hasil Linear Regression ke dalam hasil_model"""

hasil_model = pd.concat([hasil_model, pd.DataFrame({'Model': ['Linear Regression'], 'MSE': [mse_lr], 'RMSE': [rmse_lr], 'R2': [r2_lr]})], ignore_index=True)

"""# Evaluasi Model

###Tampilkan hasil evaluasi model
"""

print("\nHasil Evaluasi Model:\n", hasil_model)

fig, ax = plt.subplots(figsize=(10, 6))
hasil_model.set_index('Model')[['MSE', 'RMSE', 'R2']].plot(kind='bar', ax=ax)
plt.title("Perbandingan Kinerja Model")
plt.ylabel("Metrik")
plt.show()

"""###Prediksi dan pengujian dengan model Linear Regression"""

y_pred_lr_test = lr_model.predict(X_test)

"""###Menghitung metrik evaluasi untuk Linear Regression pada data uji"""

mse_lr_test = mean_squared_error(y_test, y_pred_lr_test)
rmse_lr_test = np.sqrt(mse_lr_test)
r2_lr_test = r2_score(y_test, y_pred_lr_test)

print("Model Linear Regression - Evaluasi Set Pengujian")
print(f"MSE: {mse_lr_test:.2f}")
print(f"RMSE: {rmse_lr_test:.2f}")
print(f"R²: {r2_lr_test:.2f}")
print("\n")

"""###Prediksi dan pengujian dengan model Random Forest Regressor"""

y_pred_rf_test = rf_model.predict(X_test)

"""###Menghitung metrik evaluasi untuk Random Forest pada data uji"""

mse_rf_test = mean_squared_error(y_test, y_pred_rf_test)
rmse_rf_test = np.sqrt(mse_rf_test)
r2_rf_test = r2_score(y_test, y_pred_rf_test)

print("Model Random Forest - Evaluasi Set Pengujian")
print(f"MSE: {mse_rf_test:.2f}")
print(f"RMSE: {rmse_rf_test:.2f}")
print(f"R²: {r2_rf_test:.2f}")

"""# Inferensi

###Membuat data prediksi sesuai dengan kolom fitur yang ada pada data pelatihan
"""

data_prediksi = pd.DataFrame({
    'Year': [2024],  # Tahun saat prediksi
    'Annual Cost Increase (applied to initial and last phases)': [0.02],  # Angka kenaikan biaya tahunan
    'Initial Year After Diagnosis Cost': [10000],  # Biaya untuk tahun pertama setelah diagnosis
    'Continuing Phase Cost': [5000],  # Biaya untuk fase lanjutan
    'Last Year of Life Cost': [20000],  # Biaya pada tahun terakhir hidup
    'Cancer Site_Bladder': [0],
    'Cancer Site_Brain': [0],
    'Cancer Site_Breast': [0],
    'Cancer Site_Cervix': [1],  # Kanker serviks
    'Cancer Site_Colorectal': [0],
    'Cancer Site_Esophagus': [0],
    'Cancer Site_Head_Neck': [0],
    'Cancer Site_Kidney': [0],
    'Cancer Site_Leukemia': [0],
    'Cancer Site_Lung': [0],
    'Cancer Site_Lymphoma': [0],
    'Cancer Site_Melanoma': [0],
    'Cancer Site_Other': [0],
    'Cancer Site_Ovary': [0],
    'Cancer Site_Pancreas': [0],
    'Cancer Site_Prostate': [0],
    'Cancer Site_Stomach': [0],
    'Cancer Site_Uterus': [0],
    'Sex_Females': [1],  # Pasien perempuan
    'Sex_Males': [0],
    'Incidence and Survival Assumptions_Incidence, Survival at constant rate': [0],
    'Incidence and Survival Assumptions_Incidence, Survival follow recent trends': [0],
    'Incidence and Survival Assumptions_Survival follows recent trend, Incidence constant': [1],
})

"""###Standarisasi data prediksi menggunakan scaler yang sudah dilatih"""

data_prediksi_scaled = scaler.transform(data_prediksi)

"""###Menggunakan model Random Forest terbaik untuk prediksi"""

prediksi_total_cost = best_rf_model_quick.predict(data_prediksi_scaled)

"""###Menampilkan hasil prediksi"""

print("Hasil Prediksi Total Biaya Perawatan:")
print(f"Total Costs (predicted): {prediksi_total_cost[0]:,.2f}")