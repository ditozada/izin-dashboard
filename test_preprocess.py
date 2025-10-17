import os
import io
import pandas as pd
import numpy as np
import streamlit as st   


# -------------------- Konstanta --------------------
REQUIRED_COLS = ["SEKTOR", "JENIS IZIN", "KATEGORI", "BULAN", "JUMLAH"]
MONTH_ORDER_ID = [
    "JANUARI", "FEBRUARI", "MARET", "APRIL", "MEI", "JUNI",
    "JULI", "AGUSTUS", "SEPTEMBER", "OKTOBER", "NOVEMBER", "DESEMBER"
]

# -------------------- Fungsi Preprocessing --------------------
@st.cache_data(show_spinner=True)
def preprocess_raw(file):
    df = pd.read_excel(file, header=None, dtype=object)

    # Step sesuai preprocesing.py
    if df.shape[0] >= 5:
        df = df.drop(index=4).reset_index(drop=True)
    to_drop = []
    if df.shape[0] >= 1:
        to_drop.append(0)
    if df.shape[0] >= 76:
        to_drop.append(75)
    if to_drop:
        df = df.drop(index=to_drop).reset_index(drop=True)

    if df.shape[0] >= 1:
        df = df.drop(index=0).reset_index(drop=True)

    df = df[df.index < 72].reset_index(drop=True)
    df = df.T
    df = df[df.index < 56].reset_index(drop=True)
    df.iloc[:, 0] = df.iloc[:, 0].ffill()
    df.iloc[:, 0] = df.iloc[:, 0].astype(str) + ',' + df.iloc[:, 1].astype(str)
    df = df.drop(df.columns[1], axis=1)
    df = df.T.reset_index(drop=True)
    df.columns = df.iloc[0]
    df = df.drop(0).reset_index(drop=True)

    # drop kolom tidak perlu
    cols_to_drop = [
        col for col in df.columns
        if isinstance(col, str) and (
            "JUMLAH DI FO" in col.upper() or
            "KETERANGAN" in col.upper() or
            col.upper().endswith("JUMLAH")
        )
    ]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)

    df = df.fillna(0).infer_objects(copy=False)

    # melt
    id_vars = [col for col in df.columns if str(col).startswith(("NO", "SEKTOR", "JENIS IZIN"))]
    df_melted = df.melt(id_vars=id_vars, var_name="KATEGORI", value_name="JUMLAH")
    df_melted[['KATEGORI', 'BULAN']] = df_melted['KATEGORI'].str.split(',', expand=True)

    # urutkan & tipe data
    df_melted["BULAN"] = df_melted["BULAN"].astype(str).str.upper().str.strip()
    df_melted["BULAN"] = pd.Categorical(df_melted["BULAN"], categories=MONTH_ORDER_ID, ordered=True)
    df_melted = df_melted.sort_values("BULAN")
    df_melted["JUMLAH"] = pd.to_numeric(df_melted["JUMLAH"], errors="coerce").fillna(0).astype(int)
    df_melted.columns = df_melted.columns.map(lambda x: str(x).replace(",nan", "").strip())


    return df_melted
