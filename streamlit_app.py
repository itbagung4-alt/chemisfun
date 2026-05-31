import streamlit as st

# Pengaturan halaman
st.set_page_config(page_title="Penyetaraan Metatesis", page_icon="🧪", layout="centered")

# Header
st.title("🧪 Penyetaraan Reaksi Metatesis")
st.markdown("Web ini menjelaskan proses penyetaraan reaksi pertukaran ganda (metatesis) secara langkah demi langkah.")

st.divider()

# Reaksi awal
st.subheader("Reaksi yang Belum Setara")
st.markdown("Reaksi antara Perak Nitrat dan Barium Klorida:")
st.latex(r"AgNO_3(aq) + BaCl_2(aq) \rightarrow AgCl(s) + Ba(NO_3)_2(aq)")

# Tombol interaktif
if st.button("Setarakan Reaksi", type="primary"):
    
    # Reaksi akhir
    st.success("Reaksi berhasil disetarakan!")
    st.latex(r"2AgNO_3(aq) + BaCl_2(aq) \rightarrow 2AgCl(s) + Ba(NO_3)_2(aq)")
    
    st.divider()
    
    # Penjelasan langkah-langkah
    st.subheader("📖 Penjelasan Penyetaraan:")
    st.markdown("""
    Reaksi metatesis terjadi ketika ion-ion dari dua senyawa saling bertukar pasangan. Untuk memenuhi Hukum Kekekalan Massa, jumlah atom di reaktan (kiri) harus sama dengan di produk (kanan).
    
    **Langkah-langkahnya:**
    1. **Cek Klorida (Cl):** Di sebelah kiri ada 2 atom Cl pada $BaCl_2$, tapi di kanan hanya ada 1 Cl pada $AgCl$. Tambahkan koefisien **2** di depan $AgCl$.
    2. **Cek Perak (Ag):** Karena sekarang ada 2 atom Ag di kanan ($2AgCl$), kita harus menambahkan koefisien **2** di depan $AgNO_3$ di sebelah kiri.
    3. **Cek Ion Nitrat ($NO_3$):** Di kiri sekarang ada 2 ion nitrat ($2AgNO_3$). Angka ini kebetulan sudah sama dengan jumlah nitrat di sebelah kanan pada $Ba(NO_3)_2$.
    4. **Cek Barium (Ba):** Jumlah Ba sudah seimbang, yaitu 1 atom di kiri dan 1 atom di kanan.
    """)

st.divider()

# Footer identitas
st.caption("Dibuat oleh: Agung Nugraha (NIM 2560557)")
