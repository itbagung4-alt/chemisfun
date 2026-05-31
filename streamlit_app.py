import streamlit as st
from chempy import balance_stoichiometry

# Pengaturan dasar halaman web
st.set_page_config(page_title="Penyetaraan Reaksi Metatesis", page_icon="🧪", layout="centered")

# Judul dan deskripsi
st.title("🧪 Kalkulator Reaksi Metatesis")
st.markdown("""
Aplikasi web sederhana ini akan membantu Anda menyetarakan reaksi kimia, khususnya **Reaksi Metatesis (Pertukaran Ganda)**, 
sekaligus memberikan penjelasan singkat mengenai prosesnya.
""")

st.divider()

# Form input reaktan dan produk
st.subheader("Masukkan Senyawa Kimia")
st.info("Gunakan format kimia standar dan perhatikan huruf besar/kecil (contoh: AgNO3, NaCl, BaCl2). Pisahkan setiap senyawa dengan tanda koma.")

col1, col2 = st.columns(2)

with col1:
    # Input reaktan dari user
    reaktan_input = st.text_input("Reaktan (Kiri)", "AgNO3, NaCl")

with col2:
    # Input produk dari user
    produk_input = st.text_input("Produk (Kanan)", "AgCl, NaNO3")

# Tombol untuk mengeksekusi penyetaraan
if st.button("Setarakan Reaksi", type="primary"):
    try:
        # Membersihkan spasi dan memisahkan input berdasarkan koma
        reaktan_list = {x.strip() for x in reaktan_input.split(',')}
        produk_list = {x.strip() for x in produk_input.split(',')}
        
        # Proses penyetaraan menggunakan chempy
        reaktan_setara, produk_setara = balance_stoichiometry(reaktan_list, produk_list)
        
        st.success("✅ Reaksi Berhasil Disetarakan!")
        
        # Fungsi untuk merapikan tampilan angka koefisien
        def format_reaksi(senyawa_dict):
            hasil = []
            for senyawa, koefisien in senyawa_dict.items():
                if koefisien == 1:
                    hasil.append(f"{senyawa}")
                else:
                    hasil.append(f"{koefisien}{senyawa}")
            return " + ".join(hasil)
            
        reaksi_kiri = format_reaksi(reaktan_setara)
        reaksi_kanan = format_reaksi(produk_setara)
        
        # Menampilkan hasil
        st.markdown(f"### Hasil Reaksi:\n**{reaksi_kiri} ➔ {reaksi_kanan}**")
        
        st.divider()
        
        # Penjelasan konsep metatesis
        st.subheader("💡 Penjelasan Reaksi Metatesis")
        st.markdown("""
        Reaksi yang Anda masukkan adalah contoh dari **Reaksi Metatesis** (atau reaksi pertukaran ganda). 
        Dalam reaksi ini, kation (ion positif) dan anion (ion negatif) dari dua senyawa reaktan saling bertukar pasangan untuk membentuk dua senyawa produk yang baru.
        
        **Pola Umum Reaksi:**
        """)
        
        st.latex(r"AB + CD \rightarrow AD + CB")
        
        st.markdown("""
        **Langkah Penyetaraan:**
        Koefisien (angka di depan senyawa kimia) yang ditambahkan di atas berfungsi agar jumlah atom pada reaktan (kiri) sama persis dengan jumlah atom pada produk (kanan). Hal ini wajib dilakukan untuk memenuhi **Hukum Kekekalan Massa**.
        """)
        
    except Exception as e:
        # Menampilkan pesan error jika rumus kimia salah ketik atau tidak masuk akal
        st.error(f"❌ Terjadi kesalahan! Pastikan rumus kimia yang Anda masukkan benar, perhatikan huruf besar/kecil, dan reaksi tersebut secara teori bisa disetarakan.")
