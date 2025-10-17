import os
import pandas as pd
import streamlit as st
import plotly.express as px
from test_preprocess import preprocess_raw  # fungsi preprocess dari file lain
import plotly.io as pio

# -------------------- Konfigurasi Halaman --------------------
st.set_page_config(page_title="Dashboard Izin Multi-Kategori", layout="wide")

# -------------------- Path Data --------------------
DATA_PATH = "data/latest.xlsx"

if not os.path.exists(DATA_PATH):
    st.error("❌ Data belum tersedia. Silakan unggah melalui halaman admin.")
    st.stop()

# -------------------- Load Data --------------------
try:
    df = preprocess_raw(DATA_PATH)
except Exception as e:
    st.error(f"Terjadi kesalahan saat memproses data: {e}")
    st.stop()

import datetime

# Ambil waktu terakhir file di-update
last_update_time = datetime.datetime.fromtimestamp(os.path.getmtime(DATA_PATH))
last_update_str = last_update_time.strftime("%d %B %Y • %H:%M WIB")

# -------------------- Urutan Bulan --------------------
MONTH_ORDER_ID = [
    "JANUARI", "FEBRUARI", "MARET", "APRIL", "MEI", "JUNI",
    "JULI", "AGUSTUS", "SEPTEMBER", "OKTOBER", "NOVEMBER", "DESEMBER"
]

# -------------------- Tema Warna --------------------
pio.templates.default = "plotly_white"
px.colors.qualitative.Plotly[0] = "#0021B1"  # biru Sleman

pio.templates["sleman_theme"] = pio.templates["plotly_white"]
pio.templates["sleman_theme"].layout.colorway = px.colors.qualitative.Plotly
pio.templates.default = "sleman_theme"

# -------------------- Sidebar --------------------
with st.sidebar:
    st.header("⚙️ Filter Data")

    sektor_opts = sorted(df["SEKTOR"].dropna().unique().tolist())
    jenis_opts = sorted(df["JENIS IZIN"].dropna().unique().tolist())
    bulan_opts = [m for m in MONTH_ORDER_ID if m in df["BULAN"].unique().tolist()]

    with st.expander("Sektor", expanded=True):
        all_sektor = st.checkbox("Pilih Semua Sektor", value=True)
        sel_sektor = st.multiselect("Cari / pilih sektor", sektor_opts, default=(sektor_opts if all_sektor else []))

    with st.expander("Jenis Izin", expanded=True):
        all_jenis = st.checkbox("Pilih Semua Jenis Izin", value=True)
        sel_jenis = st.multiselect("Cari / pilih jenis izin", jenis_opts, default=(jenis_opts if all_jenis else []))

    with st.expander("Bulan", expanded=True):
        all_bulan = st.checkbox("Pilih Semua Bulan", value=True)
        sel_bulan = st.multiselect("Cari / pilih bulan", bulan_opts, default=(bulan_opts if all_bulan else []))

# -------------------- Main Page --------------------
# -------------------- Header Dashboard --------------------
# -------------------- Header Dashboard --------------------
col_title, col_update = st.columns([2, 1])

with col_title:
    st.markdown(
        "<h2 style='margin-bottom:0px;'>📊 Dashboard Izin Multi-Kategori</h2>",
        unsafe_allow_html=True
    )

with col_update:
    st.markdown(
        f"""
        <div style='text-align:right; font-size:15px; color:gray; margin-top:8px;'>
            🕒 <b>Data terakhir diperbarui:</b><br>{last_update_str}
        </div>
        """,
        unsafe_allow_html=True
    )

kategori_order = ["JUMLAH IZIN", "JUMLAH BERKAS DICABUT", "JUMLAH PENOLAKAN", "JUMLAH IZIN TERBIT"]
kategori_opts = [k for k in kategori_order if k in df["KATEGORI"].unique()]
kategori_pilih = st.radio("Pilih Kategori", kategori_opts, horizontal=True)

# Filter data
dff = df[
    (df["KATEGORI"] == kategori_pilih) &
    (df["SEKTOR"].isin(sel_sektor)) &
    (df["JENIS IZIN"].isin(sel_jenis)) &
    (df["BULAN"].isin(sel_bulan))
].copy()

# -------------------- KPI Section --------------------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total", f"{int(dff['JUMLAH'].sum()):,}".replace(",", "."))
with c2:
    st.metric("Jumlah Sektor", dff["SEKTOR"].nunique())

top_izin = dff.groupby("JENIS IZIN")["JUMLAH"].sum().sort_values(ascending=False).reset_index()
izin_top = top_izin.iloc[0] if not top_izin.empty else None
delta_izin = f"Top: {izin_top['JENIS IZIN']}" if izin_top is not None else "-"
with c3:
    st.metric("Jenis Izin", dff["JENIS IZIN"].nunique(), delta=delta_izin)

if not dff.empty:
    bulan_group = dff.groupby("BULAN", as_index=False)["JUMLAH"].sum()
    bulan_peak = bulan_group.loc[bulan_group["JUMLAH"].idxmax()]

    total_all = int(dff["JUMLAH"].sum())
    bulan_val = int(bulan_peak["JUMLAH"])
    persen_peak = (bulan_val / total_all * 100) if total_all > 0 else 0

    with c4:
        st.metric(
            "Puncak Bulan",
            str(bulan_peak["BULAN"]),
            delta=f"{bulan_val:,} izin ({persen_peak:.1f}%)".replace(",", ".")
        )
else:
    with c4:
        st.metric("Puncak Bulan", "-", delta="-")

st.divider()

# -------------------- Grafik --------------------
# Total per bulan
g1 = dff.groupby("BULAN", as_index=False)["JUMLAH"].sum()
kategori_summary = (
    df.groupby("KATEGORI", as_index=False)["JUMLAH"]
    .sum()
    .sort_values("JUMLAH", ascending=False)
)
total_all = kategori_summary["JUMLAH"].sum()
kategori_summary["PERSENTASE"] = (kategori_summary["JUMLAH"] / total_all * 100).round(1)

header_col1, header_col2 = st.columns([2, 1])
with header_col1:
    st.markdown("### Total per Bulan")
with header_col2:
    st.markdown("### Komposisi Kategori")

col1, col2 = st.columns([2, 1])

# Bar chart
with col1:
    g1_nonzero = g1[g1["JUMLAH"] > 0]
    fig1 = px.bar(
        g1_nonzero, x="BULAN", y="JUMLAH", text="JUMLAH",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig1.update_traces(texttemplate='%{text}', textposition='outside')
    fig1.update_layout(
        yaxis_title="Jumlah", xaxis_title="Bulan",
        height=550, margin=dict(t=20, b=20, l=10, r=10)
    )
    st.plotly_chart(fig1, use_container_width=True)

# Donut chart
with col2:
    kategori_summary["LABEL"] = kategori_summary.apply(
        lambda x: f"{x['KATEGORI']}<br>{x['JUMLAH']:,} ({x['PERSENTASE']}%)", axis=1
    )

    fig_donut = px.pie(
        kategori_summary,
        names="LABEL",
        values="JUMLAH",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    fig_donut.update_traces(
        textinfo="label",
        textposition="auto",
        showlegend=False,
        hovertemplate="<b>%{label}</b><extra></extra>",
        marker=dict(line=dict(color="white", width=2))
    )

    total_izin = kategori_summary["JUMLAH"].sum()
    fig_donut.add_annotation(
        text=f"<b>{total_izin:,}</b><br>Total Izin",
        x=0.5, y=0.5,
        font=dict(size=18, color="#0A1931"),
        showarrow=False
    )

    fig_donut.update_layout(
        height=420,
        margin=dict(t=30, b=10, l=40, r=40)
    )

    st.plotly_chart(fig_donut, use_container_width=True)

# -------------------- Komposisi Jenis Izin --------------------
st.markdown("### Komposisi Jenis Izin per Bulan")
bulan_for_bar_home = st.selectbox("Pilih Bulan", options=MONTH_ORDER_ID)

dcomp_home = (
    dff[dff["BULAN"] == bulan_for_bar_home]
    .groupby("JENIS IZIN", as_index=False)["JUMLAH"].sum()
    .sort_values("JUMLAH", ascending=False)
)

fig_home = px.bar(
    dcomp_home.head(7), x="JUMLAH", y="JENIS IZIN",
    orientation="h", text="JUMLAH",
    color="JENIS IZIN",
    color_discrete_sequence=px.colors.qualitative.Plotly
)
fig_home.update_traces(texttemplate='%{text}', textposition='outside')
fig_home.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    xaxis_title="Jumlah", yaxis_title="Jenis Izin",
    height=500,
    margin=dict(t=30, b=30, l=40, r=20)
)
st.plotly_chart(fig_home, use_container_width=True)
