import streamlit as st
import os
from test_preprocess import preprocess_raw

st.set_page_config(page_title="Admin Upload Data", page_icon="🧑‍💼", layout="centered")

# -------------------- Konfigurasi --------------------
ADMIN_PASSWORD = st.secrets["admin"]["password"]
DATA_DIR = "data"
LATEST_FILE = os.path.join(DATA_DIR, "latest.xlsx")

# -------------------- Tampilan Awal --------------------
st.title("🧑‍💼 Halaman Admin - Upload Data Excel")
pwd = st.text_input("Masukkan password:", type="password")

if pwd == ADMIN_PASSWORD:
    st.success("Akses diterima ✅")

    # pastikan folder data ada
    os.makedirs(DATA_DIR, exist_ok=True)

    # tampilkan info file lama
    if os.path.exists(LATEST_FILE):
        st.info(f"📁 File aktif saat ini: `{os.path.basename(LATEST_FILE)}`")
    else:
        st.warning("Belum ada file aktif yang tersimpan.")

    # uploader
    uploaded = st.file_uploader("Unggah file Excel (.xlsx)", type=["xlsx"])
    if uploaded:
        try:
            # Hapus file lama dulu (biar bersih)
            if os.path.exists(LATEST_FILE):
                os.remove(LATEST_FILE)
                st.info("🧹 File lama berhasil dihapus.")

            # Simpan file baru langsung sebagai latest.xlsx
            with open(LATEST_FILE, "wb") as f:
                f.write(uploaded.getbuffer())

            st.success(f"✅ File '{uploaded.name}' berhasil diunggah dan disimpan sebagai data aktif.")

            # Preview hasil preprocess
            try:
                df_preview = preprocess_raw(LATEST_FILE)
                st.dataframe(df_preview.head())
                st.caption(f"Data berisi {len(df_preview)} baris.")
            except Exception as e:
                st.error(f"Gagal membaca file Excel: {e}")

        except PermissionError:
            st.error("⚠️ Tidak bisa menulis file — pastikan file Excel tidak sedang dibuka di aplikasi lain.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

else:
    st.warning("Masukkan password admin untuk melanjutkan.")
