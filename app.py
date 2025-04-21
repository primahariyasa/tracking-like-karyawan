import streamlit as st
import pandas as pd
from datetime import date

# Dummy database karyawan
df_karyawan = pd.DataFrame([
    {"Nama": "Andi Pratama", "Divisi": "Marketing", "WhatsApp": "6281234567890"},
    {"Nama": "Siti Nurhaliza", "Divisi": "HRD", "WhatsApp": "6289876543210"},
    {"Nama": "Budi Santoso", "Divisi": "Finance", "WhatsApp": "6281112223344"},
])

# Dummy tracking like (admin input / hasil verifikasi internal)
df_tracking = pd.DataFrame([
    {"Tanggal": "2025-04-20", "Platform": "Instagram", "Link": "https://instagram.com/p/abc", "Nama": "Andi Pratama", "Status Like": "✔"},
    {"Tanggal": "2025-04-20", "Platform": "Instagram", "Link": "https://instagram.com/p/abc", "Nama": "Siti Nurhaliza", "Status Like": "❌"},
    {"Tanggal": "2025-04-20", "Platform": "TikTok",    "Link": "https://tiktok.com/@brand/video/xyz", "Nama": "Budi Santoso", "Status Like": "❌"},
])

# UI Header
st.set_page_config(page_title="Tracking Like Sosmed + Reminder", layout="wide")
st.title("📱 Tracking Like Sosial Media & Reminder WhatsApp")

# Filter by rentang tanggal & platform
st.sidebar.header("🎯 Filter Review")
tanggal_awal = st.sidebar.date_input("Dari Tanggal", date(2025, 4, 20))
tanggal_akhir = st.sidebar.date_input("Sampai Tanggal", date(2025, 4, 20))
platform = st.sidebar.selectbox("Pilih Platform", ["Instagram", "Facebook", "TikTok"])

# Filter data tracking
filtered = df_tracking[
    (df_tracking["Platform"] == platform) &
    (pd.to_datetime(df_tracking["Tanggal"]) >= pd.to_datetime(tanggal_awal)) &
    (pd.to_datetime(df_tracking["Tanggal"]) <= pd.to_datetime(tanggal_akhir))
]

# Gabung dengan database karyawan (biar dapet nomor WA)
filtered = filtered.merge(df_karyawan, on="Nama", how="left")

st.subheader(f"Hasil Review: Belum Like di {platform} dari {tanggal_awal} s.d {tanggal_akhir}")

# Hanya tampilkan yang belum like
belum_like = filtered[filtered["Status Like"] == "❌"]

# Generate link WhatsApp persuasif
def generate_reminder(row):
    pesan = f"Halo {row['Nama']}! Yuk bantu support dengan like postingan terbaru kami di {row['Platform']} 😊\n{row['Link']}"
    wa_link = f"https://wa.me/{row['WhatsApp']}?text={pesan.replace(' ', '%20')}"
    return f"[Kirim Reminder WA]({wa_link})"

if not belum_like.empty:
    belum_like["Reminder WA"] = belum_like.apply(generate_reminder, axis=1)
    st.write(belum_like[["Tanggal", "Nama", "Divisi", "Platform", "Link", "Reminder WA"]].to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.success("Semua karyawan sudah melakukan like pada periode dan platform ini! 🎉")

# Optional: Export tracking
st.subheader("📤 Export Data Tracking")
csv = df_tracking.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download CSV Tracking Like", csv, "tracking_like.csv", "text/csv")
