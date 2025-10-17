### ✅ File 1: README.md

```markdown
# 📊 Dashboard Izin Multi-Kategori Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu, Kab Sleman

Dashboard interaktif berbasis **Streamlit** untuk menampilkan tren dan komposisi berbagai jenis izin per sektor, kategori, dan bulan.  
Dilengkapi halaman admin untuk upload data Excel terbaru secara mudah.


## 🚀 Fitur Utama

- ✅ Upload & update data Excel melalui halaman admin  
- 📈 Visualisasi interaktif (bar chart, donut chart, KPI, dsb.)  
- 🗓️ Filter berdasarkan sektor, jenis izin, dan bulan  
- 💾 Preprocessing otomatis untuk data mentah  

## 🧩 Struktur Project


📦 izin-dashboard
┣ 📂 data/                # Folder penyimpanan data terbaru
┣ 📄 app_dashboard.py     # Dashboard utama
┣ 📄 app_admin.py         # Halaman admin (upload data)
┣ 📄 test_preprocess.py   # Fungsi preprocessing data Excel
┣ 📄 requirements.txt     # Dependensi Python
┣ 📄 .gitignore           # File yang diabaikan Git
┣ 📄 LICENSE              # Lisensi open-source
┗ 📄 README.md            # Dokumentasi project


## 🧠 Teknologi yang Digunakan

* [Streamlit](https://streamlit.io/)
* [Pandas](https://pandas.pydata.org/)
* [Plotly Express](https://plotly.com/python/plotly-express/)
* [NumPy](https://numpy.org/)

## 📜 Lisensi

Project ini dirilis di bawah lisensi [MIT License](LICENSE).

---

## 👤 Pembuat

Dito Zada Luthfir Rahman
💼 Data Analyst | BI & Dashboard Developer
📧 [ditozada@gmail.com]
🌐 [LinkedIn](https://linkedin.com/in/ditozada)

````

### ✅ File 2: .gitignore
```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.db
*.sqlite3

# Streamlit
.streamlit/secrets.toml

# Data
data/*
!data/.gitkeep

# Jupyter / IDE
.ipynb_checkpoints/
.vscode/
.idea/
*.DS_Store
.env
````

---

### ✅ File 3: LICENSE

```text
MIT License

Copyright (c) 2025 Dito

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

### ✅ File 4: requirements.txt

```text
streamlit
pandas
numpy
plotly
openpyxl
```
